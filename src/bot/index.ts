import { Bot } from "grammy";
import { config } from "../config/index.js";
import { registerOnboardingHandlers } from "./handlers/onboarding.js";
import { registerBriefingHandlers } from "./handlers/briefing.js";
import { registerSettingsHandlers } from "./handlers/settings.js";
import { registerAuthHandlers } from "./handlers/auth.js";
import { registerResumeHandlers } from "./handlers/resume.js";
import { registerMessageHandlers } from "./handlers/message.js";

/**
 * Registers the Telegram slash commands menu with Telegram servers.
 * Makes `/briefing`, `/agenda`, `/settings`, `/start` popup automatically when user types `/`.
 */
export async function setBotCommands(bot: Bot): Promise<void> {
  try {
    await bot.api.setMyCommands([
      { command: "briefing", description: "📊 Daily market intelligence digest" },
      { command: "jobs", description: "💼 Live job postings matching your resume" },
      { command: "target_companies", description: "🎯 Manage dream target companies for job alerts" },
      { command: "resume", description: "📄 Upload your resume PDF" },
      { command: "agenda", description: "📅 Today's meetings & company prep" },
      { command: "login", description: "🔐 Connect your Google Calendar" },
      { command: "settings", description: "⚙️ Watchlist, industry & briefing time" },
      { command: "start", description: "👋 Welcome & onboarding setup" },
    ]);
    console.log("✅ Telegram command menu registered (/briefing, /agenda, /settings, /start)");
  } catch (err) {
    console.warn("⚠️ Failed to set Telegram bot commands menu:", err);
  }
}

/** Create and configure the grammY bot instance. */
export function createBot(): Bot {
  const bot = new Bot(config.TELEGRAM_BOT_TOKEN);

  // Global error handler
  bot.catch((err) => {
    console.error("❌ Bot error:", err.error);
  });

  // Register handlers in order (commands first, then generic message handler)
  registerOnboardingHandlers(bot);
  registerBriefingHandlers(bot);
  registerSettingsHandlers(bot);
  registerAuthHandlers(bot);
  registerResumeHandlers(bot);
  registerMessageHandlers(bot); // Must be last — catches all non-command messages

  return bot;
}
