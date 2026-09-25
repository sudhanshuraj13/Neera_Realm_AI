# 🤖 Telegram Bot Gateway Documentation — Neera Realm AI
**Document Version:** 1.0.0  
**Framework:** Node.js, TypeScript, grammY framework  
**Database Client:** Prisma ORM connecting to Neon PostgreSQL  
**Location:** `src/`  

---

## 1. Bot Gateway Architecture

The Telegram Bot acts as the high-retention **Daily Companion & Real-Time Alert Channel** for Neera Realm AI. It runs in Node.js, polling via grammY in development and ready for webhook routing in production.

### Operational Philosophy:
- **Fast First Response:** Native typing indicators (`await ctx.replyWithChatAction('typing')`) triggered before all DB or AI network hops.
- **Strict Telegram HTML Only:** All responses use Telegram-compliant HTML tags (`<b>`, `<i>`, `<code>`, `<a href="...">`). Raw markdown is strictly prohibited.
- **Sanitized Outputs:** All dynamic strings from external APIs pass through `escapeHtml()` to avoid parsing exceptions.

---

## 2. Command Registry & Handlers

| Command | Handler File | Functional Role | Output Format |
| :--- | :--- | :--- | :--- |
| `/start` | `src/bot/handlers/onboarding.ts` | Greets user, checks account link token (`/start link_<token>`), initiates onboarding if new. | HTML Welcome Card + Inline Keyboards |
| `/resume` | `src/bot/handlers/resume.ts` | Prompts for PDF resume upload, extracts text with `pdf-parse`, parses via FastAPI `/api/v1/resume/parse`. | Profile confirmation card + Target roles |
| `/jobs` | `src/bot/handlers/jobs.ts` | Live ATS job discovery across target companies and open startup job feeds. | Top 5 job cards with apply links |
| `/target_companies` | `src/bot/handlers/targetCompanies.ts` | Manage custom dream company ATS watchlist (Greenhouse/Lever/Ashby). | List of active companies + Add/Remove buttons |
| `/briefing` | `src/bot/handlers/briefing.ts` | Instant manual trigger for morning financial ticker + calendar agenda + job matches. | Daily Intelligence Digest |
| `/agenda` | `src/bot/handlers/agenda.ts` | Fetches Google Calendar meetings for the day via OAuth tokens. | Chronological meeting summary |
| `/help` | `src/bot/handlers/help.ts` | Displays full command list and web platform link. | Formatted help menu |

---

## 3. Directory Structure (`src/`)

```
src/
├── index.ts                # Application bootstrapper, process shields, bot startup
├── server.ts               # Express HTTP server (:3000) for health checks, OAuth callbacks & webhooks
├── bot/
│   ├── index.ts            # grammY bot instance creation & command registration
│   ├── handlers/           # Thin command handlers (onboarding, resume, jobs, briefing, etc.)
│   ├── keyboards/          # Inline keyboards (Experience level, track, action buttons)
│   └── middlewares/        # User session injector, error boundary, typing indicators
├── services/               # Reusable business logic
│   ├── authService.ts      # Google OAuth2 URL generation & callback token exchange
│   ├── calendarService.ts  # Google Calendar API event fetching & sync
│   ├── briefingService.ts  # Multi-source briefing synthesizer
│   ├── atsService.ts       # ATS API clients (Greenhouse, Lever, Ashby)
│   └── fundingService.ts   # Startup funding RSS radar
├── db/
│   ├── prisma.ts           # Shared PrismaClient singleton instance
│   └── userRepository.ts   # Database CRUD queries scoped strictly by userId/telegramId
├── jobs/
│   └── briefingCron.ts     # node-cron scheduled background job for proactive morning briefings
├── utils/
│   ├── htmlEscaper.ts      # Sanitizes < and > characters for Telegram HTML
│   ├── messageSender.ts    # Safe message delivery with 4,000 char chunking & 429 backoff
│   └── httpClient.ts       # Axios instance with 60s timeout & 3x exponential retry
└── config/
    └── index.ts            # Zod-validated environment variable loader
```

---

## 4. Cross-Channel Account Pairing Protocol

When a user links their web account to Telegram:
1. Web platform generates a single-use cryptographically random token: `https://t.me/NeeraRealmBot?start=link_<token>`.
2. User taps the link on mobile, initiating `/start link_<token>`.
3. Handler in `src/bot/handlers/onboarding.ts`:
   - Validates that `telegramLinkToken === <token>` and `telegramLinkExpires > new Date()`.
   - Binds `user.telegramId = ctx.from.id`.
   - Clears `telegramLinkToken` and `telegramLinkExpires`.
   - Sends confirmation: *"🎉 Your account is linked! You will now receive daily morning briefings and high-priority ATS job alerts here."*

---

## 5. Defensive Telegram Reliability Laws
1. **Never Block Event Loops:** Heavy processing (ATS parsing, AI orchestration) must run asynchronously; never block the main thread.
2. **Chunking Law:** Any response exceeding 4,000 characters must be partitioned via `sendSafeTelegramMessage()` to avoid Telegram `MESSAGE_TOO_LONG` errors.
3. **Typing Heartbeat:** If an external service takes longer than 5 seconds, renew `sendChatAction('typing')` every 4 seconds.
