import type { Bot } from "grammy";
import { InlineKeyboard } from "grammy";
import { getOrCreateUser, updateUserPreferences } from "../../db/userRepository.js";
import { sendSafeTelegramMessage } from "../../utils/telegram.js";

/** Callback data constants to avoid magic strings. */
const CALLBACK = {
  INDUSTRY_FINANCE: "onboard:industry:finance",
  INDUSTRY_TECH: "onboard:industry:tech",
  SKIP: "onboard:skip",
} as const;

/** Register the /start command and onboarding callback handlers. */
export function registerOnboardingHandlers(bot: Bot): void {
  bot.command("start", async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    // Upsert user in database (thin handler — delegates to repository)
    const user = await getOrCreateUser(
      BigInt(from.id),
      from.first_name,
      from.username
    );

    // Build greeting with inline keyboard
    const greeting = [
      `<b>👋 Welcome to Neera AI, ${user.firstName}!</b>`,
      "",
      "I'm your personal market intelligence assistant.",
      "Let's set up your preferences so I can deliver briefings tailored to you.",
      "",
      "<i>Which industry do you follow?</i>",
    ].join("\n");

    const keyboard = new InlineKeyboard()
      .text("📈 Finance & Markets", CALLBACK.INDUSTRY_FINANCE)
      .row()
      .text("🚀 Tech & Startups", CALLBACK.INDUSTRY_TECH)
      .row()
      .text("⏩ Skip Onboarding", CALLBACK.SKIP);

    await sendSafeTelegramMessage(ctx, greeting, {
      reply_markup: keyboard,
    });
  });

  // --- Callback query handlers ---

  bot.callbackQuery(CALLBACK.INDUSTRY_FINANCE, async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    const user = await getOrCreateUser(
      BigInt(from.id),
      from.first_name,
      from.username
    );

    await updateUserPreferences(user.id, {
      industries: ["Finance"],
      watchlist: ["AAPL", "NVDA", "TSLA"],
      onboardingDone: true,
    });

    const stockKeyboard = new InlineKeyboard()
      .text("🍎 AAPL", "action:query:AAPL")
      .text("🟢 NVDA", "action:query:NVDA")
      .row()
      .text("⚡ TSLA", "action:query:TSLA")
      .text("🛍️ BABA", "action:query:BABA");

    await ctx.editMessageText(
      [
        "<b>📈 Finance & Markets Suite Ready!</b>",
        "",
        "Preferences updated for <b>Finance & Markets</b>.",
        "",
        "• <b>Industries:</b> Finance",
        "• <b>Watchlist:</b> AAPL, NVDA, TSLA",
        "• <b>Briefing Time:</b> 08:00 UTC",
        "",
        "👇 <b>Tap a stock below for an instant briefing, or type any ticker:</b>",
      ].join("\n"),
      {
        parse_mode: "HTML",
        reply_markup: stockKeyboard,
      }
    );

    await ctx.answerCallbackQuery({ text: "Selected: 📈 Finance & Markets" });
  });

  bot.callbackQuery(CALLBACK.INDUSTRY_TECH, async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    const user = await getOrCreateUser(
      BigInt(from.id),
      from.first_name,
      from.username
    );

    await updateUserPreferences(user.id, {
      industries: ["Tech", "Startups"],
      watchlist: ["NVDA", "TSLA", "MSFT"],
      onboardingDone: true,
    });

    const techKeyboard = new InlineKeyboard()
      .text("📄 Upload Resume", "action:upload_resume")
      .row()
      .text("🟢 NVDA", "action:query:NVDA")
      .text("⚡ TSLA", "action:query:TSLA")
      .row()
      .text("💻 Tech Career Intelligence", "action:career_prep");

    await ctx.editMessageText(
      [
        "<b>🚀 Tech & Startups Hub Ready!</b>",
        "",
        "Welcome to your Tech & Career Intelligence Suite.",
        "",
        "• <b>Focus:</b> Tech, Startups & Career Intelligence",
        "• <b>Watchlist:</b> NVDA, TSLA, MSFT",
        "• <b>Briefing Time:</b> 08:00 UTC",
        "",
        "💼 <b>Career Intelligence & ATS Matching:</b>",
        "Upload your resume to extract skills, experience & target roles for automated job matching.",
        "",
        "👇 <b>Tap '📄 Upload Resume' below to upload your resume PDF!</b>",
      ].join("\n"),
      {
        parse_mode: "HTML",
        reply_markup: techKeyboard,
      }
    );

    await ctx.answerCallbackQuery({ text: "Selected: 🚀 Tech & Startups" });
  });

  bot.callbackQuery(CALLBACK.SKIP, async (ctx) => {
    const from = ctx.from;
    if (!from) return;

    const user = await getOrCreateUser(
      BigInt(from.id),
      from.first_name,
      from.username
    );

    await updateUserPreferences(user.id, { onboardingDone: true });

    const defaultKeyboard = new InlineKeyboard()
      .text("📄 Upload Resume", "action:upload_resume")
      .row()
      .text("🍎 AAPL", "action:query:AAPL")
      .text("🟢 NVDA", "action:query:NVDA")
      .row()
      .text("⚡ TSLA", "action:query:TSLA")
      .text("🛍️ BABA", "action:query:BABA");

    await ctx.editMessageText(
      [
        "<b>⏩ Onboarding skipped!</b>",
        "",
        "No worries — you can update your preferences anytime with <code>/settings</code>.",
        "",
        "I've set you up with defaults:",
        "• <b>Industries:</b> Finance",
        "• <b>Watchlist:</b> AAPL, NVDA, TSLA",
        "• <b>Briefing Time:</b> 08:00 UTC",
        "",
        "👇 <b>Tap a stock for a briefing, or tap '📄 Upload Resume' to upload your PDF:</b>",
      ].join("\n"),
      {
        parse_mode: "HTML",
        reply_markup: defaultKeyboard,
      }
    );

    await ctx.answerCallbackQuery({ text: "Onboarding skipped" });
  });
}

