# Product Vision Document — Neera Realm AI

## Executive Overview
**Neera Realm AI** is an AI-powered Career & Financial Intelligence SaaS platform. It combines a real-time Telegram Bot interface with a high-performance Python FastAPI multi-agent engine (LangGraph, Gemini 2.5) and a Node.js Gateway connected to Neon PostgreSQL.

## Core Mission
To empower software engineers, tech professionals, and freshers with automated career intelligence:
- Extracting career profiles from uploaded resume PDFs.
- Matching live ATS job openings across global tech leaders, startups, and open job boards.
- Monitoring market watchlists and financial news.
- Seamlessly managing daily meeting agendas and preparation.

## Target Audience
1. **Entry-Level Engineers & Freshers**: Seeking tailored entry-level, junior, and associate engineering opportunities without being flooded by senior job listings.
2. **Experienced Tech Professionals**: Seeking specialized backend, AI, frontend, cloud, or leadership roles at target dream companies.
3. **Productivity Enthusiasts & Investors**: Looking for automated morning briefing digests, stock price tracking, and calendar meeting sync.

## Core Pillars
1. **Deterministic User Profile & Control**: Explicit database fields (`experienceLevel`, `targetRoles`, `locationPreference`) eliminating fragile LLM guessing.
2. **Human-in-the-Loop (HITL) Agent Clarification**: Conversational LangGraph state machine asking for missing parameters (e.g. location preference) before executing queries.
3. **Live ATS & Global Startup Job Discovery**: Direct ATS queries (Greenhouse, Lever, Ashby) + global startup job boards (Remotive, Arbeitnow).
4. **Anti-Hallucination Quality Control**: Master Supervisor Agent auditing specialist agent outputs against ground-truth user context.
