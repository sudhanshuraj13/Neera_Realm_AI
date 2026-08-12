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
import {
  getOrCreateUser,
  getSentFundingAlertIds,
  recordSentFundingAlerts,
} from "../../db/userRepository.js";
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

      // 4. Send to Python FastAPI for raw skill/project extraction
      const result = await parseResume(user.id, rawText);
      const profile = (result.profile as Record<string, unknown>) || {};
      const extractedTargetRoles = Array.isArray(profile["target_roles"])
        ? (profile["target_roles"] as string[])
        : [];

      // 5. Save raw extracted profile + targetRoles to DB
      await prisma.user.update({
        where: { id: user.id },
        data: {
          resumeJson: JSON.parse(JSON.stringify(result.profile)) as object,
          targetRoles: extractedTargetRoles,
        },
      });

      // 6. Step 1 of Wellfound-Style Stateful Onboarding: Interactive Primary Role Confirmation
      const aiGuess = (profile["primary_role"] as string) || "General Professional";

      const roleConfirmKeyboard = new InlineKeyboard()
        .text(`✅ Confirm: ${aiGuess}`, "action:confirm_ai_role")
        .row()
        .text("✏️ Set Custom Target Role", "action:prompt_custom_role");

      await sendSafeTelegramMessage(
        ctx,
        [
          "✅ <b>Resume skills & profile extracted!</b>",
          "",
          "🤖 <b>AI Role Detection:</b>",
          `It looks like your primary role is: <b>${aiGuess}</b>`,
          "",
          "<i>Is this the exact primary role you want me to hunt jobs for?</i>",
        ].join("\n"),
        { reply_markup: roleConfirmKeyboard }
      );

      console.log(
        `📄 [Resume] Extracted for user ${user.id} (${from.first_name}) — ${rawText.length} chars`
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

  // Callback query handler for Confirming AI-detected Primary Role
  bot.callbackQuery("action:confirm_ai_role", async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      const profile = (user.resumeJson as Record<string, unknown>) || {};
      const aiGuess = (profile["primary_role"] as string) || "General Professional";

      await prisma.user.update({
        where: { id: user.id },
        data: {
          primaryRole: aiGuess,
          onboardingCompleted: true,
        },
      });

      await ctx.answerCallbackQuery({ text: `Confirmed primary role: ${aiGuess}` });

      const expKeyboard = new InlineKeyboard()
        .text("🎓 Fresher (0-1 yrs)", "action:set_exp:Fresher")
        .text("💻 Junior (1-3 yrs)", "action:set_exp:1-3 Years")
        .row()
        .text("🚀 Senior (3+ yrs)", "action:set_exp:Senior");

      await sendSafeTelegramMessage(
        ctx,
        [
          `🎯 <b>Confirmed Primary Role:</b> <code>${aiGuess}</code>`,
          "",
          "<b>Step 2/2: Experience Level Setup</b>",
          "What is your exact professional experience level?",
          "",
          "<i>Tap a button below to save your experience preference:</i>",
        ].join("\n"),
        { reply_markup: expKeyboard }
      );
    } catch (err) {
      console.error("❌ Confirm AI role action error:", err);
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Could not confirm primary role. Please try again."
      );
    }
  });

  // Callback query handler for Prompting Custom Target Role
  bot.callbackQuery("action:prompt_custom_role", async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      const profile = (user.resumeJson as Record<string, unknown>) || {};
      profile["_pendingCustomRolePrompt"] = true;

      await prisma.user.update({
        where: { id: user.id },
        data: {
          resumeJson: profile as object,
        },
      });

      await ctx.answerCallbackQuery({ text: "Type your target primary role" });

      await sendSafeTelegramMessage(
        ctx,
        [
          "✏️ <b>Set Your Custom Target Role</b>",
          "",
          "Please reply with your exact target primary role (e.g., <code>UI/UX Designer</code>, <code>Mechanical Engineer</code>, <code>Data Scientist</code>, or <code>DevOps Engineer</code>):",
        ].join("\n")
      );
    } catch (err) {
      console.error("❌ Prompt custom role error:", err);
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Could not initiate custom role prompt. Please try again."
      );
    }
  });

  // Text message listener for Custom Role Input when _pendingCustomRolePrompt is set
  bot.on("message:text", async (ctx, next) => {
    const text = ctx.message.text.trim();
    if (text.startsWith("/")) {
      return next();
    }

    const from = ctx.from;
    if (!from) return next();

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      const profile = (user.resumeJson as Record<string, unknown>) || {};
      if (profile["_pendingCustomRolePrompt"] === true) {
        const customRole = text;
        const updatedProfile = { ...profile };
        delete updatedProfile["_pendingCustomRolePrompt"];

        await prisma.user.update({
          where: { id: user.id },
          data: {
            primaryRole: customRole,
            onboardingCompleted: true,
            resumeJson: updatedProfile as object,
          },
        });

        const expKeyboard = new InlineKeyboard()
          .text("🎓 Fresher (0-1 yrs)", "action:set_exp:Fresher")
          .text("💻 Junior (1-3 yrs)", "action:set_exp:1-3 Years")
          .row()
          .text("🚀 Senior (3+ yrs)", "action:set_exp:Senior");

        await sendSafeTelegramMessage(
          ctx,
          [
            `🎯 <b>Target Primary Role Set to:</b> <code>${customRole}</code>`,
            "",
            "<b>Step 2/2: Experience Level Setup</b>",
            "What is your exact professional experience level?",
            "",
            "<i>Tap a button below to save your preference:</i>",
          ].join("\n"),
          { reply_markup: expKeyboard }
        );
        return;
      }
    } catch (err) {
      console.error("❌ Custom role text handling error:", err);
    }

    return next();
  });

  // Callback query handler for Deterministic Experience Level Selection (Step C)
  bot.callbackQuery(/^action:set_exp:(Fresher|1-3 Years|Senior)$/, async (ctx) => {
    const level = ctx.match[1];
    await ctx.answerCallbackQuery({ text: `Experience set to ${level}` });
    const from = ctx.from;
    if (!from) return;

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      await prisma.user.update({
        where: { id: user.id },
        data: { experienceLevel: level },
      });

      const jobKeyboard = new InlineKeyboard().text("💼 View Matching Jobs", "action:fetch_jobs");

      await sendSafeTelegramMessage(
        ctx,
        [
          "🎉 <b>Career Profile Setup Complete!</b>",
          "",
          user.primaryRole ? `<b>Primary Role:</b> <code>${user.primaryRole}</code>` : "",
          `<b>Experience Level:</b> <code>${level}</code>`,
          user.targetRoles.length > 0
            ? `<b>Target Roles:</b> ${user.targetRoles.map((r) => `<code>${r}</code>`).join(", ")}`
            : "",
          "",
          "Your deterministic profile is saved in Neon DB. Type <code>/jobs</code> or tap below to search matching postings!",
        ].filter(Boolean).join("\n"),
        { reply_markup: jobKeyboard }
      );
    } catch (err) {
      console.error("❌ Set experience action error:", err);
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Could not save experience level. Please try again."
      );
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
            "👉 Please upload your resume as a <b>PDF file</b> using <code>/resume</code> or tap the button below.",
          ].join("\n"),
          { reply_markup: uploadKeyboard }
        );
        return;
      }

      // Candidate has a stored resume profile! Fetch matching live jobs with deterministic DB filters
      const sentStartupIds = await getSentFundingAlertIds(user.id);
      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>,
        undefined,
        user.experienceLevel ?? undefined,
        user.targetRoles,
        user.locationPreference ?? undefined,
        user.primaryRole ?? undefined,
        sentStartupIds
      );

      if (result.sent_startup_ids && result.sent_startup_ids.length > 0) {
        await recordSentFundingAlerts(user.id, result.sent_startup_ids);
      }

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

      const sentStartupIds = await getSentFundingAlertIds(user.id);
      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>,
        undefined,
        user.experienceLevel ?? undefined,
        user.targetRoles,
        user.locationPreference ?? undefined,
        user.primaryRole ?? undefined,
        sentStartupIds
      );

      if (result.sent_startup_ids && result.sent_startup_ids.length > 0) {
        await recordSentFundingAlerts(user.id, result.sent_startup_ids);
      }

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

      const sentStartupIds = await getSentFundingAlertIds(user.id);
      const result = await matchJobs(
        user.id,
        user.resumeJson as Record<string, unknown>,
        undefined,
        level,
        user.targetRoles,
        user.locationPreference ?? undefined,
        user.primaryRole ?? undefined,
        sentStartupIds
      );

      if (result.sent_startup_ids && result.sent_startup_ids.length > 0) {
        await recordSentFundingAlerts(user.id, result.sent_startup_ids);
      }

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

  // Inline keyboard button callback: "💼 Jobs & Career Intelligence"
  bot.callbackQuery("action:career_prep", async (ctx) => {
    await ctx.answerCallbackQuery({ text: "Jobs & Careers ATS Matching" });
    await sendSafeTelegramMessage(
      ctx,
      [
        "<b>💼 Jobs & Career Intelligence & Job Matching</b>",
        "",
        "Neera AI dynamically scans global job boards & target company ATS feeds (Greenhouse, Lever, Ashby) to aggregate live job listings.",
        "",
        "To customize your target companies or start:",
        "• Type <code>/target_companies Google, Stripe, Razorpay</code> to set dream companies!",
        "• Click <b>📄 Upload Resume</b> or send your resume PDF to match jobs!",
      ].join("\n")
    );
  });

  // Command handler for /target_companies (or /dream_companies)
  bot.command(["target_companies", "dream_companies"], async (ctx) => {
    await ctx.replyWithChatAction("typing");
    const from = ctx.from;
    if (!from) return;

    try {
      const user = await getOrCreateUser(
        BigInt(from.id),
        from.first_name,
        from.username
      );

      const profile = (user.resumeJson as Record<string, unknown>) || {};
      const textArgs = ctx.match.trim();

      if (textArgs) {
        // User provided company list, e.g. "/target_companies Razorpay, Stripe, OpenAI"
        const newCompanies = textArgs
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean);

        const updatedProfile = {
          ...profile,
          target_companies: newCompanies,
        };

        await prisma.user.update({
          where: { id: user.id },
          data: { resumeJson: updatedProfile as object },
        });

        await sendSafeTelegramMessage(
          ctx,
          [
            "🎯 <b>Target Dream Companies Updated!</b>",
            "",
            `<b>Active Target Companies:</b> ${newCompanies.map((c) => `<code>${c}</code>`).join(", ")}`,
            "",
            "⚡ <i>Neera AI will now prioritize and scan these target companies for you! Type <code>/jobs</code> to view live matched openings.</i>",
          ].join("\n")
        );
        return;
      }

      // Display current target companies & instructions
      const existing = (profile["target_companies"] as string[]) || [];

      await sendSafeTelegramMessage(
        ctx,
        [
          "🎯 <b>Target Dream Companies Watchlist</b>",
          "",
          existing.length > 0
            ? `<b>Active Target Companies:</b> ${existing.map((c) => `<code>${c}</code>`).join(", ")}`
            : "<b>Active Target Companies:</b> <i>None set (scanning all global startup job boards)</i>",
          "",
          "<b>How to set your dream companies:</b>",
          "• Type <code>/target_companies Google, Stripe, Razorpay, OpenAI</code>",
          "• Or type <code>/jobs</code> anytime to browse live startup job feeds!",
        ].join("\n")
      );
    } catch (err) {
      console.error("❌ Target companies handler error:", err);
      await sendSafeTelegramMessage(
        ctx,
        "⚠️ Could not update target companies. Please try again."
      );
    }
  });
}
