# 🎪 CelebraTech AI — GenAI Celebration & Event Planner

[![Live Deployment](https://img.shields.io/badge/Live%20Demo-celebai.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://celebai.onrender.com/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Adityakarri12%2Fcelebai-blue?style=for-the-badge&logo=github)](https://github.com/Adityakarri12/celebai)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI%200.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20Modular-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Enterprise-Grade Celebration & Event Planning Platform** powered by **FastAPI**, **Pydantic**, **React 18**, and **Google GenAI**. Seamlessly orchestrate **Weddings**, **Birthdays**, and **Community Festivals** with automated budgets, dynamic What-If rebalancing simulators, dual-phase milestone timelines, live countdown timers, vendor lifecycle management, guest RSVP & dietary tracking, moodboard palettes, ready-to-use invitation suites, and interactive **3D flip-card ideas**.

---

## 🔗 Quick Navigation & Live Links

| Resource | URL | Description |
| :--- | :--- | :--- |
| 🌐 **Live Web Application** | **[https://celebai.onrender.com/](https://celebai.onrender.com/)** | Full interactive React single-page application hosted on Render |
| 💻 **GitHub Repository** | **[https://github.com/Adityakarri12/celebai](https://github.com/Adityakarri12/celebai)** | Source code, deployment manifests, tests, and version history |
| 📖 **Interactive Swagger UI** | **[https://celebai.onrender.com/docs](https://celebai.onrender.com/docs)** | Live OpenAPI documentation with interactive endpoint testing |
| 📑 **ReDoc Documentation** | **[https://celebai.onrender.com/redoc](https://celebai.onrender.com/redoc)** | Clean, human-readable API reference and schema explorer |
| 🩺 **System Health Check** | **[https://celebai.onrender.com/health](https://celebai.onrender.com/health)** | Live monitoring endpoint verifying uptime and AI provider status |

---

## 📑 Table of Contents

1. [Executive Summary & Problem Statement](#-executive-summary--problem-statement)
2. [End-to-End System Architecture](#-end-to-end-system-architecture)
3. [Deep-Dive: Core Modules & Working Mechanics](#-deep-dive-core-modules--working-mechanics)
   - [1. 3D Idea Flip Cards Engine](#1-interactive-3d-flip-card-ideas-engine)
   - [2. Budget Tracking & What-If Rebalancing Simulator](#2-budget-tracking--interactive-what-if-simulator)
   - [3. Dual-Phase Timelines & Live Countdown](#3-dual-phase-timelines--live-countdown-clock)
   - [4. Vendor Pipeline & Progress Checklist](#4-vendor-lifecycle--interactive-checklists)
   - [5. Guest RSVP & Dietary Manager](#5-guest-rsvp--dietary-requirements-manager)
   - [6. Theme Moodboards & Swatches](#6-theme-moodboard-palette--typography)
   - [7. Invitation & Toast Studio](#7-invitation-suite--toast-speech-studio)
   - [8. Conversational GenAI Director](#8-conversational-genai-director)
4. [Enterprise Security & OWASP Hardening](#-enterprise-security--owasp-hardening)
5. [Complete REST API Specification](#-complete-rest-api-specification)
6. [Repository Structure](#-repository-structure)
7. [Local Setup & Quick Start Guide](#-local-setup--quick-start-guide)
8. [Automated Testing Suite (100% Pass Rate)](#-automated-testing-suite)
9. [Production Deployment Guide](#-production-deployment-guide)

---

## 🌟 Executive Summary & Problem Statement

Event planning is traditionally chaotic: budgets spiral out of control, day-of schedules get lost in chat threads, dietary restrictions are overlooked, and creative concepts lack actionable execution details. 

**CelebraTech AI** solves this by consolidating the entire lifecycle into an intelligent, unified dashboard:

| Planning Challenge | CelebraTech AI Solution | Working Implementation |
| :--- | :--- | :--- |
| **Fragmented Event Types** | Tailored architectures for **Weddings**, **Birthdays**, and **Community Festivals**. | Pre-configured domain models with industry-accurate phases, vendors, and milestone templates. |
| **Budget Drift & Miscalculation** | Algorithmic percentage breakdown & live **What-If Rebalancing Slider**. | Real-time actual vs. estimated tracking, variance alerts, and live budget simulation ($2K to $100K). |
| **Execution Timing Gaps** | Dual-phase planning & **live ticking countdown**. | Phase 1: Planning milestones (months/weeks before). Phase 2: Minute-by-minute Day-of Run of Show. |
| **Vendor Miscommunication** | 6-stage contract pipeline & subtask meters. | Status pipeline: *Researching* ➔ *Contacted* ➔ *Quote Received* ➔ *Contract Signed* ➔ *Deposit Paid* ➔ *Fully Paid*. |
| **Dietary & Guest Confusion** | Seating assignments & dietary preference rosters. | Tracks Vegan, Halal, Nut Allergy, Gluten-Free headcounts and table numbers with instant confirmation filters. |
| **Superficial Pinterest Ideas** | Interactive **3D Flip Cards** with tactile audio feedback. | **Front**: High-level visual aesthetic & mood. **Back**: Step-by-step logistics, vendor pairings, and pro tips. |
| **Color Clashes** | 5-swatch palette with designated design roles. | Color roles (Primary Warmth, Secondary Foliage, Neutral Elegance, Metallic Accent, Contrast) with 1-click hex copy. |
| **Writer's Block (Invites & Speeches)** | Pre-written copy and speech blueprints. | One-click copy for formal wedding invitations, WhatsApp quick-RSVPs, and 3-minute toast templates. |

---

## 🏗 End-to-End System Architecture

The project employs a clean, asynchronous architecture where a **FastAPI ASGI application** serves both high-speed RESTful JSON APIs and the static **React 18 single-page application** assets.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER (UI / UX)                        │
│   React 18 Single-Page Application (Zero-Lag Local CDN Assets)         │
│   Interactive 3D Cards │ Budget Simulator │ Live Ticking Countdown     │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │ HTTP / JSON REST Calls
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       FASTAPI ASGI APPLICATION                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     SECURITY & HARDENING MIDDLEWARE              │  │
│  │  • OWASP Headers (CSP, X-Frame-Options, X-Content-Type-Options)  │  │
│  │  • In-Memory Sliding-Window IP Rate Limiter                      │  │
│  │  • XSS Input Sanitization with Safe Celebration Punctuation      │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     │                                  │
│         ┌───────────────────────────┴───────────────────────────┐      │
│         ▼                                                       ▼      │
│  ┌──────────────┐                                        ┌───────────┐ │
│  │ API ROUTERS  │                                        │  STATIC   │ │
│  │ /api/events  │                                        │  ASSETS   │ │
│  │ /api/ai      │                                        │  /static  │ │
│  └──────┬───────┘                                        └─────┬─────┘ │
└─────────┼──────────────────────────────────────────────────────┼───────┘
          │                                                      │
          ▼                                                      ▼
┌──────────────────────────────────┐               ┌────────────────────────┐
│      SERVICES & DOMAIN LOGIC     │               │   STATIC SPA FILES     │
│  • EventService (Thread-Safe DB) │               │   • index.html         │
│  • BudgetService (Calculations)  │               │   • css/styles.css     │
│  • ExportService (Markdown, CSV) │               │   • js/app.jsx         │
└─────────────────┬────────────────┘               │   • vendor/*.min.js    │
                  │                                └────────────────────────┘
                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     HYBRID INTELLIGENCE ENGINE                         │
│  Primary: Google Gemini API (gemini-2.5-flash via google-genai SDK)    │
│  Fallback: High-Fidelity Curated Knowledge Base (100% Uptime Engine)   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💡 Deep-Dive: Core Modules & Working Mechanics

### 1. Interactive 3D Flip Card Ideas Engine
- **How it Works**: Built using CSS 3D perspectives (`perspective: 1200px`, `transform-style: preserve-3d`, `backface-visibility: hidden`).
- **Tactile Interaction**: Clicking **anywhere** on the card smoothly executes a 180-degree flip accompanied by an ambient synthesized audio chime generated via the Web Audio API.
- **Double-Sided Intelligence**:
  - **Front Side**: Theme overview, aesthetic badge, inspirational photography concept, and bullet highlights.
  - **Back Side**: Actionable backstage blueprints including exact equipment lists, vendor coordination advice, audio/visual cues, and cost-saving pro tips.
- **Accessibility (WCAG 2.1 AA)**: Focusable via keyboard (`Tab`), with `aria-pressed` states, accessible screen-reader labels, and keyboard flip support (`Enter` or `Space`).

### 2. Budget Tracking & Interactive What-If Simulator
- **Proportional Allocation**: Dynamically calculates recommended starter allocations based on established industry benchmarks per event type (e.g. Wedding: 45% Venue/Catering, 15% Photo/Video, 12% Music/Band, 10% Decor/Flowers, 8% Attire/Beauty, 5% Invites, 5% Contingency).
- **Interactive What-If Rebalancing Slider**: Users can drag the budget slider anywhere from **$2,000 to $100,000**. The system recalculates recommended allocations in real time without overwriting entered actual costs.
- **Financial Health Indicators**: Visual progress bars display percentage spent, total actual cost vs. estimated budget, and trigger color-coded variance badges (*Under Budget*, *On Track*, *Over Budget*).

### 3. Dual-Phase Timelines & Live Countdown Clock
- **Two Distinct Phases**:
  1. **Planning Countdown**: Multi-month/week milestones (e.g. *12 Months Out: Book Venue*, *6 Months Out: Send Invitations*, *1 Month Out: Final Headcount*).
  2. **Day-of Run of Show**: Minute-by-minute execution schedule (e.g. *08:00 AM Vendor Access*, *03:30 PM Guest Seating*, *04:00 PM Ceremony Begins*).
- **Live Ticking Countdown Clock**: Real-time timer updating every second, displaying days, hours, minutes, and seconds until the celebration.

### 4. Vendor Lifecycle & Interactive Checklists
- **6-Stage Status Progression**: Tracks vendors through *Researching* ➔ *Contacted* ➔ *Quote Received* ➔ *Contract Signed* ➔ *Deposit Paid* ➔ *Fully Paid*.
- **Subtask Checklist**: Each vendor card has interactive sub-tasks (e.g., *Schedule food tasting*, *Review contract clauses*, *Confirm final headcount*).
- **Visual Progress Meters**: Shows task completion percentages alongside contact info, quotes, and deposit tracking.

### 5. Guest RSVP & Dietary Requirements Manager
- **RSVP Status Dashboard**: Instant count of *Confirmed*, *Pending*, and *Declined* attendees.
- **Dietary Breakdown**: Automatically calculates headcounts for specialized dietary requirements (*Vegan*, *Gluten-Free*, *Halal*, *Nut Allergy*, *Standard*).
- **Table Seating**: Assigns table numbers and logs contact emails/phone numbers with notes.

### 6. Theme Moodboard Palette & Typography
- **5-Swatch Palette**: Curated palettes with specific design roles:
  - `Primary Warmth`
  - `Secondary Foliage`
  - `Neutral Elegance`
  - `Metallic Accent`
  - `Formal Contrast`
- **One-Click Hex Copy**: Clicking any swatch copies its `#HEX` code to the clipboard with visual confirmation.
- **Lighting & Font Pairings**: Recommends harmonious typography pairings (e.g., *Playfair Display* + *Montserrat*) and ambient lighting setups (e.g., *2700K warm fairy lights with Edison bulbs*).

### 7. Invitation Suite & Toast Speech Studio
- **Formal Invitations**: Classical, polished wedding and gala wording ready for digital or printed stationery.
- **WhatsApp / SMS Quick RSVP**: Engaging, emoji-accented copy for casual milestone birthdays and community festivals.
- **Toast Speech Blueprint**: A structured 3-minute speech formula (Hook ➔ Childhood Anecdote ➔ Why They Complement Each Other ➔ Heartfelt Toast) allowing anyone to deliver a memorable speech without anxiety.

### 8. Conversational GenAI Director
- **Context-Aware Dialogue**: The AI Assistant maintains full contextual memory of the currently selected event (title, budget, guest count, vibe, timeline).
- **Hybrid Intelligence**:
  - When a `GEMINI_API_KEY` is provided, requests utilize Google Gemini (`gemini-2.5-flash`) for real-time generative responses.
  - When running offline or without an API key, the system seamlessly transitions to its built-in expert curated generative knowledge base with **zero downtime**.

---

## 🔒 Enterprise Security & OWASP Hardening

The application incorporates multiple layers of security:

1. **OWASP Security Headers**: Custom Starlette middleware injects:
   - `X-Content-Type-Options: nosniff` — Prevents MIME-type sniffing.
   - `X-Frame-Options: DENY` — Prevents clickjacking attacks.
   - `X-XSS-Protection: 1; mode=block` — Enforces browser XSS filtering.
   - `Referrer-Policy: strict-origin-when-cross-origin` — Protects user referrers.
   - `Content-Security-Policy` — Restricts script execution to safe and local origins.
2. **In-Memory Sliding-Window Rate Limiter**:
   - Limits client IPs to 180 requests per minute to prevent denial-of-service and automated scraping, while exempting static bundle assets.
3. **Smart Input Sanitization**:
   - Escapes dangerous HTML tags (`<script>`, `<iframe>`, `<img>`, `onload=`) while preserving natural celebration punctuation (e.g. ampersands and apostrophes: *Sofia & Julian's Wedding*).

---

## 📡 Complete REST API Specification

All endpoints are hosted live at `https://celebai.onrender.com` and locally at `http://127.0.0.1:8000`.

### System & Health Endpoints
| Method | Endpoint | Description | Sample Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Live system health and AI provider status | `{"status":"healthy","service":"CelebraTech AI...","version":"1.0.0"}` |
| `GET` | `/docs` | Interactive Swagger API Explorer | HTML / OpenAPI UI |
| `GET` | `/redoc` | ReDoc API Specification | HTML / ReDoc UI |

### Events Management Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/events` | List all celebrations (including seeded showcases for Weddings, Birthdays, and Community Festivals) |
| `POST` | `/api/events` | Create a new event (with optional automated GenAI plan generation) |
| `GET` | `/api/events/{id}` | Retrieve comprehensive event details (budget, timeline, vendors, guests, ideas, palette) |
| `DELETE` | `/api/events/{id}` | Delete an event and free memory |
| `GET` | `/api/events/{id}/export/{format}` | Export complete event packet as formatted `markdown` or structured `csv` |

### Budget, Vendors & Guests Sub-Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/events/{id}/budget` | Add a new budget expense item |
| `PUT` | `/api/events/{id}/budget/{item_id}` | Update actual costs or toggle paid status |
| `POST` | `/api/events/{id}/vendors` | Add a new vendor to the roster |
| `PATCH` | `/api/events/{id}/vendors/{vendor_id}/status` | Update vendor stage (*Researching* ➔ *Fully Paid*) |
| `PATCH` | `/api/events/{id}/vendors/{vendor_id}/tasks/{idx}` | Toggle vendor checklist sub-task completion |
| `POST` | `/api/events/{id}/guests` | Add a new guest with dietary preferences and table numbers |
| `PATCH` | `/api/events/{id}/guests/{guest_id}/rsvp` | Update guest RSVP status (*Confirmed*, *Pending*, *Declined*) |

### GenAI Planning Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/ai/plan` | Generate a full celebration plan bundle (budget, timeline, vendors, ideas) from a custom brief |
| `POST` | `/api/ai/chat` | Contextual conversation with the AI Event Planner Assistant |
| `POST` | `/api/ai/ideas` | Generate 6 personalized 3D flip-card ideas for a specific theme or vibe |

---

## 📂 Repository Structure

```
celebai/
├── app/                                 # FastAPI Backend Architecture
│   ├── __init__.py                      # Package descriptor
│   ├── config.py                        # Pydantic Settings & Dynamic $PORT Bindings
│   ├── main.py                          # Application factory, static mounting & middleware
│   ├── api/                             # REST API Routers
│   │   ├── __init__.py
│   │   ├── middleware.py                # OWASP Headers & Sliding-Window Rate Limiter
│   │   ├── routes_ai.py                 # GenAI Plan & Chat Endpoints
│   │   └── routes_events.py             # Event CRUD, Vendors, Guests, and Export Endpoints
│   ├── models/                          # Pydantic Schemas & Data Contracts
│   │   ├── __init__.py
│   │   ├── ai.py                        # AI Request & Response Bundles
│   │   └── event.py                     # Event, Budget, Vendor, Guest, & 3D Idea Models
│   └── services/                        # Business Logic & Algorithms
│       ├── __init__.py
│       ├── ai_planner.py                # Gemini API Integration + Offline Curated Knowledge Base
│       ├── budget_service.py            # Financial Calculations & Proportional Distributions
│       ├── event_service.py             # In-Memory Thread-Safe Event Data Store
│       └── export_service.py            # Markdown & CSV Exporters
│
├── static/                              # Frontend React 18 Single-Page Application
│   ├── index.html                       # HTML5 Root Entry Point
│   ├── css/
│   │   └── styles.css                   # Custom Luxury Dark-Mode Design System
│   ├── js/
│   │   ├── api.js                       # Asynchronous Backend Client
│   │   ├── app.js                       # Legacy React bridge
│   │   ├── app.jsx                      # Pure React 18 Modular Components & View Controller
│   │   ├── confetti.js                  # Lightweight celebratory canvas confetti engine
│   │   └── components/                  # Modular Component Partials
│   │       ├── aiAssistant.js           # Conversational AI Tab
│   │       ├── budgetTracker.js         # Interactive Budget Simulator & Slider
│   │       ├── flipCards.js             # 3D Flip Card Component Logic
│   │       ├── guestManager.js          # Guest RSVP & Dietary Roster
│   │       ├── invitationStudio.js      # Invitations & Toast Speech Studio
│   │       ├── moodboardPalette.js      # 5-Swatch Palette & Typography Spec
│   │       ├── timelineView.js          # Dual-Phase Timeline & Live Countdown
│   │       └── vendorChecklist.js       # 6-Stage Vendor Progression Checklist
│   └── vendor/                          # Offline-Resilient Frontend Libraries
│       ├── babel.min.js                 # In-browser JSX Transpiler
│       ├── react.production.min.js      # React 18 Core
│       └── react-dom.production.min.js  # React 18 DOM
│
├── tests/                               # Comprehensive Automated Test Suite
│   ├── __init__.py
│   ├── test_ai_planner.py               # AI Generation & Curated Engine Validation
│   ├── test_api_events.py               # API Integration Tests (Starlette TestClient)
│   ├── test_budget_service.py           # Financial Math & Proportional Distributions
│   ├── test_frontend.py                 # Static Bundle & SPA Asset Integrity
│   ├── test_models.py                   # Pydantic Validation & XSS Sanitization Tests
│   ├── test_security.py                 # OWASP Headers & Rate Limiter Tests
│   └── test_vendors_and_guests.py       # Vendor Lifecycle & Guest Dietary Tests
│
├── .gitignore                           # Git ignore rules (.venv, caches, binaries)
├── Dockerfile                           # Production Python 3.12-slim Container Definition
├── Procfile                             # Process file for Render / Railway / Heroku
├── render.yaml                          # Render Blueprint Auto-Deployment Specification
├── requirements.txt                     # Pinned Python Dependencies
├── run.py                               # Local ASGI Runner Script
└── README.md                            # Comprehensive Documentation
```

---

## 🚀 Local Setup & Quick Start Guide

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- `git`

### 1. Clone the Repository
```bash
git clone https://github.com/Adityakarri12/celebai.git
cd celebai
```

### 2. Create Virtual Environment & Install Dependencies
Using `uv` (recommended for speed):
```bash
uv venv
uv pip install -r requirements.txt
```
Or using standard `pip`:
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the Server
```bash
python run.py
```
Open your browser at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

---

## 🧪 Automated Testing Suite

The repository includes a comprehensive automated test suite verifying data models, calculations, REST endpoints, XSS protection, and security headers:

```bash
python -m pytest -v
```

### Verified Test Coverage:
- `tests/test_models.py`: Pydantic field validation, enum mappings, and XSS string escaping.
- `tests/test_budget_service.py`: Benchmark percentage allocations, actual cost calculations, and variance alerts.
- `tests/test_ai_planner.py`: Generative bundle completeness across Weddings, Birthdays, and Community events.
- `tests/test_api_events.py`: Full REST lifecycle, status updates, guest rosters, and CSV/Markdown exports.
- `tests/test_security.py`: OWASP security headers injection and sliding-window rate limiter enforcement.
- `tests/test_vendors_and_guests.py`: Vendor stage progression and dietary requirement aggregation.
- `tests/test_frontend.py`: Verifies static assets and React vendor bundles.

---

## ☁️ Production Deployment Guide

### Deploying to Render (Connected to GitHub)
1. Fork or push changes to your GitHub repository: `https://github.com/Adityakarri12/celebai`.
2. In the [Render Dashboard](https://dashboard.render.com/), click **+ New** ➔ **Web Service**.
3. Select `celebai`. Render automatically detects [`render.yaml`](render.yaml):
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
4. Click **Deploy Web Service**. Every push to `main` will automatically build and re-deploy!

### Deploying via Docker
You can build and run the production image anywhere:
```bash
# Build Docker image
docker build -t celebai .

# Run container on port 8000
docker run -d -p 8000:8000 --name celebai-app celebai
```
Visit `http://localhost:8000`.

---

## 📄 License
This project is licensed under the **MIT License**. Free to use, modify, and distribute for personal and commercial projects.
