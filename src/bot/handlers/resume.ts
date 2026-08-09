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
import axios from "axios";
import { PDFParse } from "pdf-parse";
import { config } from "../../config/index.js";
import { getOrCreateUser } from "../../db/userRepository.js";
import { prisma } from "../../db/client.js";
import { sendSafeTelegramMessage } from "../../utils/telegram.js";
import {
  parseResume,
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
      await sendSafeTelegramMessage(
        ctx,
        "✅ Resume processed successfully. Your high-fidelity career profile is saved."
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
