/**
 * Telegram Resume Upload Handler.
 *
 * Handles the /resume command and PDF document uploads:
 *   1. Downloads the PDF file via grammY's ctx.getFile()
 *   2. Extracts raw text using pdf-parse
 *   3. Sends text to Python FastAPI for LLM-powered structured extraction
 *   4. Saves the structured ResumeProfile to user.resumeJson in Neon via Prisma
 */

import type { Bot } from "grammy";
import { InlineKeyboard } from "grammy";
import axios from "axios";
import { PDFParse } from "pdf-parse";
import { config } from "../../config/index.js";
import { getOrCreateUser } from "../../db/userRepository.js";
import { prisma } from "../../db/client.js";
import { sendSafeTelegramMessage } from "../../utils/telegram.js";
import {
  parseResume,
  matchJobs,
  isAiServiceError,
} from "../../services/aiService.js";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/** Maximum PDF file size in bytes (10 MB). */
const MAX_FILE_SIZE = 10 * 1024 * 1024;

/** Allowed MIME types for resume uploads. */
const ALLOWED_MIME_TYPES = new Set([
  "application/pdf",
]);

// ---------------------------------------------------------------------------
// Handler Registration
// ---------------------------------------------------------------------------

/** Register the /resume command and document upload handler. */
export function registerResumeHandlers(bot: Bot): void {
  // /resume command — instructs the user to send a PDF
  bot.command("resume", async (ctx) => {
    await sendSafeTelegramMessage(
      ctx,
      [
        "<b>📄 Resume Upload</b>",
        "",
        "Send me your resume as a <b>PDF file</b> and I'll extract your career profile.",
        "",
        "I'll analyze your skills, experience, projects, and target roles to power personalized career intelligence.",
        "",
        "<i>Just drag and drop or attach your PDF here.</i>",
      ].join("\n")
    );
  });

  // Document upload handler — processes PDF files
  bot.on("message:document", async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    const doc = ctx.message.document;

    // --- Guard: Check MIME type ---
    if (!doc.mime_type || !ALLOWED_MIME_TYPES.has(doc.mime_type)) {
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Please send a <b>PDF file</b>. Other file formats are not supported for resume parsing."
      );
      return;
    }

    // --- Guard: Check file size ---
    if (doc.file_size && doc.file_size > MAX_FILE_SIZE) {
      await sendSafeTelegramMessage(
        ctx,
        `⚠️ File too large (${(doc.file_size / 1024 / 1024).toFixed(1)} MB). Maximum allowed size is 10 MB.`
      );
      return;
    }

    // Show typing indicator
    await ctx.replyWithChatAction("typing");

    try {
      // 1. Upsert user in database
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      // 2. Download the PDF file via Telegram Bot API
      const file = await ctx.getFile();
      const filePath = file.file_path;
      if (!filePath) {
        await sendSafeTelegramMessage(ctx, "⚠️ Could not retrieve the file from Telegram. Please try again.");
        return;
      }

      const fileUrl = `https://api.telegram.org/file/bot${config.TELEGRAM_BOT_TOKEN}/${filePath}`;

      const response = await axios.get(fileUrl, {
        responseType: "arraybuffer",
        timeout: 15_000,
      });

      const pdfBuffer = Buffer.from(response.data as ArrayBuffer);

      // 3. Extract raw text from PDF
      const parser = new PDFParse({ data: new Uint8Array(pdfBuffer) });
      const pdfData = await parser.getText();
      const rawText = pdfData.text?.trim();

      // Clean up parser resources
      await parser.destroy().catch(() => {});

      if (!rawText || rawText.length < 50) {
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Could not extract enough text from this PDF. Please ensure it's a valid, text-based resume (not a scanned image)."
        );
        return;
      }

      // Refresh typing indicator for the LLM call
      await ctx.replyWithChatAction("typing");

      // 4. Send to Python FastAPI for LLM-powered structured extraction
      const result = await parseResume(user.id, rawText);

      // 5. Save the structured profile to the database
      // Cast through JSON serialization to satisfy Prisma's InputJsonValue type
      await prisma.user.update({
        where: { id: user.id },
        data: { resumeJson: JSON.parse(JSON.stringify(result.profile)) as object },
      });

      // 6. Reply with success
      const jobKeyboard = new InlineKeyboard().text(
        "💼 View Matching Jobs",
        "action:fetch_jobs"
      );

      await sendSafeTelegramMessage(
        ctx,
        [
          "✅ <b>Resume processed successfully!</b>",
          "",
          "Your high-fidelity career profile has been saved.",
          "",
          "👉 Type <code>/jobs</code> or tap the button below to view live job matches from top tech companies!",
        ].join("\n"),
        { reply_markup: jobKeyboard }
      );

      console.log(
        `📄 [Resume] Processed for user ${user.id} (${from.first_name}) — ${rawText.length} chars extracted`
      );
    } catch (err) {
      if (isAiServiceError(err)) {
        console.error(`❌ [Resume] AI service error: ${err.code} — ${err.message}`);
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ The AI engine is temporarily unavailable. Please try uploading your resume again in a moment."
        );
      } else {
        console.error("❌ [Resume] Processing error:", err);
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Something went wrong while processing your resume. Please try again."
        );
      }
    }
  });

  // /jobs or /job command — fetches live ATS job postings matching the candidate's stored resume profile
  bot.command(["jobs", "job"], async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    await ctx.replyWithChatAction("typing");

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      // Guard: check if user has uploaded a resume
      if (!user.resumeJson) {
        const uploadKeyboard = new InlineKeyboard().text(
          "📄 Upload Resume",
          "action:upload_resume"
        );

        await sendSafeTelegramMessage(
          ctx,
          [
            "<b>💼 Job Matcher — No Resume Found</b>",
            "",
            "You haven't uploaded a resume yet!",
            "",
            "To get personalized, live job matches from top tech companies (Stripe, OpenAI, Vercel, Notion, etc.):",
            "",
            "👉 Please upload your resume as a <b>PDF file</b> using <code>/resume</code> or tap the button below.",
          ].join("\n"),
          { reply_markup: uploadKeyboard }
        );
        return;
      }

      // Candidate has a stored resume profile! Fetch matching live jobs
      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>
      );

      const expFilterKeyboard = new InlineKeyboard()
        .text("🎓 Fresher (0–1 yrs)", "action:exp_filter:fresher")
        .text("💻 Junior (1–3 yrs)", "action:exp_filter:junior")
        .row()
        .text("🚀 Senior (3+ yrs)", "action:exp_filter:senior");

      await sendSafeTelegramMessage(ctx, result.formatted_html, {
        reply_markup: expFilterKeyboard,
      });
    } catch (err) {
      if (isAiServiceError(err)) {
        console.error(`❌ [Jobs] AI service error: ${err.code} — ${err.message}`);
        const hint =
          err.code === "AI_SERVICE_TIMEOUT"
            ? "⏳ <b>AI Engine Initializing:</b> The Python microservice is waking up on Render or scanning live ATS job feeds. Please wait 10 seconds and type <code>/jobs</code> again!"
            : `⚠️ <b>AI Service Unreachable (${err.code}):</b> Please check that <code>AI_SERVICE_URL</code> is set correctly in your Render Web Service environment variables.`;
        await sendSafeTelegramMessage(ctx, hint);
      } else {
        console.error("❌ [Jobs] Processing error:", err);
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Something went wrong while fetching job postings. Please try again."
        );
      }
    }
  });

  // Callback query for "💼 View Matching Jobs" button
  bot.callbackQuery("action:fetch_jobs", async (ctx) => {
    await ctx.answerCallbackQuery({ text: "Fetching live job matches..." });
    const from = ctx.from;
    if (!from) return;

    await ctx.replyWithChatAction("typing");

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      if (!user.resumeJson) {
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Please upload your resume using <code>/resume</code> first!"
        );
        return;
      }

      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>
      );

      const expFilterKeyboard = new InlineKeyboard()
        .text("🎓 Fresher (0–1 yrs)", "action:exp_filter:fresher")
        .text("💻 Junior (1–3 yrs)", "action:exp_filter:junior")
        .row()
        .text("🚀 Senior (3+ yrs)", "action:exp_filter:senior");

      await sendSafeTelegramMessage(ctx, result.formatted_html, {
        reply_markup: expFilterKeyboard,
      });
    } catch (err) {
      console.error("❌ Action fetch jobs error:", err);
      if (isAiServiceError(err)) {
        const hint =
          err.code === "AI_SERVICE_TIMEOUT"
            ? "⏳ <b>AI Engine Initializing:</b> Service is warming up. Please tap <b>💼 View Matching Jobs</b> again in 10 seconds!"
            : `⚠️ Could not reach AI service: ${err.message}`;
        await sendSafeTelegramMessage(ctx, hint);
      } else {
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Could not fetch job matches right now. Please try again."
        );
      }
    }
  });

  // Callback query for experience level filter buttons: action:exp_filter:fresher, action:exp_filter:junior, action:exp_filter:senior
  bot.callbackQuery(/^action:exp_filter:(fresher|junior|senior)$/, async (ctx) => {
    const level = ctx.match[1];
    const label = level === "fresher" ? "Fresher (0-1 yrs)" : (level === "junior" ? "Junior (1-3 yrs)" : "Senior (3+ yrs)");
    await ctx.answerCallbackQuery({ text: `Filtering jobs: ${label}` });

    const from = ctx.from;
    if (!from) return;

    await ctx.replyWithChatAction("typing");

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      if (!user.resumeJson) {
        await sendSafeTelegramMessage(
          ctx,
          "⚠️ Please upload your resume using <code>/resume</code> first!"
        );
        return;
      }

      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>,
        undefined,
        level
      );

      const expFilterKeyboard = new InlineKeyboard()
        .text(level === "fresher" ? "✅ Fresher (0–1 yrs)" : "🎓 Fresher (0–1 yrs)", "action:exp_filter:fresher")
        .text(level === "junior" ? "✅ Junior (1–3 yrs)" : "💻 Junior (1–3 yrs)", "action:exp_filter:junior")
        .row()
        .text(level === "senior" ? "✅ Senior (3+ yrs)" : "🚀 Senior (3+ yrs)", "action:exp_filter:senior");

      await sendSafeTelegramMessage(ctx, result.formatted_html, {
        reply_markup: expFilterKeyboard,
      });
    } catch (err) {
      console.error("❌ Exp filter action error:", err);
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Could not refresh job filter right now. Please try again."
      );
    }
  });

  // Inline keyboard button callback: "📄 Upload Resume"
  bot.callbackQuery("action:upload_resume", async (ctx) => {
    await ctx.answerCallbackQuery({ text: "Attach your PDF resume below" });
    await sendSafeTelegramMessage(
      ctx,
      [
        "<b>📄 Resume Upload Instructions</b>",
        "",
        "Please send your resume as a <b>PDF file</b> directly in this chat.",
        "",
        "1️⃣ Click the 📎 <b>Attachment icon</b> (or drag & drop your PDF file).",
        "2️⃣ Select your <b>Resume PDF</b>.",
        "3️⃣ Hit send!",
        "",
        "<i>Our AI engine will instantly extract your skills, experience, projects, and match target job roles for you.</i>",
      ].join("\n")
    );
  });

  // Inline keyboard button callback: "💻 Tech Career Intelligence"
  bot.callbackQuery("action:career_prep", async (ctx) => {
    await ctx.answerCallbackQuery({ text: "Tech Career & ATS Matching" });
    await sendSafeTelegramMessage(
      ctx,
      [
        "<b>💻 Tech Career Intelligence & ATS Matching</b>",
        "",
        "Neera AI syncs directly with public ATS endpoints (Greenhouse, Lever, Ashby) to aggregate live job listings from tech giants & high-growth startups (Stripe, OpenAI, Vercel, Notion, etc.).",
        "",
        "To get personalized job recommendations:",
        "👉 Click <b>📄 Upload Resume</b> or send your resume PDF to start!",
      ].join("\n")
    );
  });
}
