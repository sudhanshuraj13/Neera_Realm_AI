# Database Schema Document — Neera Realm AI

## Database Technology
- **Database Engine**: Neon PostgreSQL (Serverless Cloud PostgreSQL)
- **ORM**: Prisma v6.19

---

## Entity Relationship & Schema Details

### 1. `users` Table
Stores user accounts, OAuth tokens, and career preferences.

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | String (UUID) | `@id`, Primary Key | Internal user ID |
| `telegramId` | BigInt | `@unique` | Telegram Chat / User ID |
| `firstName` | String | Required | Telegram first name |
| `username` | String | Optional | Telegram username handle |
| `googleId` | String | `@unique`, Optional | Google OAuth account ID |
| `accessToken` | Text | Optional | Google Calendar OAuth access token |
| `refreshToken` | Text | Optional | Google Calendar OAuth refresh token |
| `tokenExpiry` | DateTime | Optional | Access token expiration timestamp |
| `webhookChannelId` | String | Optional | Google Calendar webhook channel ID |
| `calendarSyncToken` | String | Optional | Google Calendar incremental sync token |
| `resumeJson` | JsonB | Optional | Extracted raw skills, experience, projects JSON |
| `isPro` | Boolean | Default: `false` | Pro monetization subscription status |
| `experienceLevel` | String | Optional | Deterministic level: `"Fresher"`, `"1-3 Years"`, `"Senior"` |
| `targetRoles` | String[] | Default: `[]` | Deterministic target roles, e.g. `["Backend", "AI"]` |
| `locationPreference` | String | Optional | Deterministic location: `"Remote"`, `"India"`, `"Bangalore"` |
| `createdAt` | DateTime | Default: `now()` | Record creation timestamp |
| `updatedAt` | DateTime | `@updatedAt` | Record update timestamp |

---

### 2. `user_preferences` Table
Stores watchlist tickers and daily briefing preferences.

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | String (UUID) | `@id`, Primary Key | Internal preference ID |
| `userId` | String | `@unique`, Foreign Key | Foreign key to `users.id` (Cascade Delete) |
| `industries` | String[] | Default: `["Finance"]` | Preferred news industries |
| `watchlist` | String[] | Default: `["AAPL", "NVDA", "TSLA"]` | Stock tickers watchlist |
| `briefingTime` | String | Default: `"08:00"` | Daily briefing UTC schedule |
| `onboardingDone` | Boolean | Default: `false` | Whether initial setup is complete |
| `createdAt` | DateTime | Default: `now()` | Record creation timestamp |
| `updatedAt` | DateTime | `@updatedAt` | Record update timestamp |

---

### 3. `messages` Table
Stores message history for multi-turn conversations.

| Field Name | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | String (UUID) | `@id`, Primary Key | Internal message ID |
| `userId` | String | Foreign Key | Foreign key to `users.id` (Cascade Delete) |
| `role` | Enum (`user`, `assistant`) | Required | Message sender role |
| `content` | Text | Required | Message body content |
| `createdAt` | DateTime | Default: `now()` | Timestamp (indexed with `userId`) |
