# Installation Guide — Neera Realm AI

## Prerequisites
- **Node.js**: v18+ or v20+
- **Python**: v3.10+ or v3.11+
- **Database**: Neon PostgreSQL connection URI
- **API Keys**: Telegram Bot Token (`TELEGRAM_BOT_TOKEN`), Google Gemini API Key (`GEMINI_API_KEY`)

---

## Local Development Setup

### Step 1: Clone Repository & Install Node.js Dependencies
```bash
git clone https://github.com/sudhanshuraj13/Neera_Realm_AI.git
cd Neera_Realm_AI
npm install
```

### Step 2: Configure Node.js Environment
Create `.env` in project root:
```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
DATABASE_URL="postgresql://user:pass@ep-ep-xxx.neon.tech/neondb?sslmode=require"
AI_SERVICE_URL="http://localhost:8000"
```

### Step 3: Sync Prisma Database Schema
```bash
npx prisma db push
```

### Step 4: Setup Python AI Microservice
```bash
cd ai_service
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

Create `ai_service/.env`:
```env
GEMINI_API_KEY="your_gemini_api_key"
PORT=8000
```

### Step 5: Start Local Services
1. **Start Python AI Microservice**:
   ```bash
   npm run dev:ai
   # Runs: cd ai_service && python main.py
   ```
2. **Start Node.js Telegram Bot Gateway**:
   ```bash
   npm run dev
   ```

---

## Render Production Deployment Guide

### Deploying Python AI Service on Render
1. Create a **New Web Service** on Render connected to `sudhanshuraj13/Neera_Realm_AI`.
2. **Root Directory**: `ai_service`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python main.py` or `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**: Set `GEMINI_API_KEY`.
6. Copy the deployed Python Web Service URL (e.g. `https://neera-ai-service.onrender.com`).

### Deploying Node.js Bot Gateway on Render
1. Create a **New Web Service** on Render.
2. **Root Directory**: `.` (project root)
3. **Build Command**: `npm install && npx prisma db push`
4. **Start Command**: `npm start`
5. **Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`
   - `DATABASE_URL`
   - `AI_SERVICE_URL` = `https://neera-ai-service.onrender.com` (your Python Render service URL).
