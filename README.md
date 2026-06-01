<h1 align="center">
  <br />
  ⚡ Sports EL
  <br />
</h1>

<h3 align="center">Non-Invasive Wearable Motion Analyzer Using Entropy-Based Signal Processing</h3>

<p align="center">
  Early detection of athletic fatigue through entropy-driven analysis of IMU motion signals — before performance declines.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3b82f6?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-22c55e?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18+-06b6d4?style=flat-square&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/TimescaleDB-PostgreSQL_15-8b5cf6?style=flat-square&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Firmware-ESP32%2FArduino-f97316?style=flat-square&logo=arduino&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-94a3b8?style=flat-square" />
</p>

---

## 📖 Overview

**Sports EL** is a wearable-integrated platform that detects the **early onset of athletic fatigue** using entropy-based analysis of motion signals. By leveraging Inertial Measurement Units (IMUs) worn by athletes, the system continuously monitors biomechanical movement, processes the signal stream, and computes entropy metrics — detecting fatigue-induced changes in neuromuscular control *before any visible performance decline*.

> **Core Insight:** Fatigue alters the complexity and regularity of movement. This is captured through **Approximate Entropy (ApEn)** and **Sample Entropy (SampEn)** computed on real-time IMU signal segments.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                  │
│         React (Vite) Dashboard — port 3000            │
└───────────────────────┬──────────────────────────────┘
                        │  REST API + WebSocket
┌───────────────────────▼──────────────────────────────┐
│                  APPLICATION LAYER                    │
│         FastAPI (Python 3.11) — port 8000             │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│              SIGNAL PROCESSING ENGINE                 │
│   Butterworth Filter → Segmentation → ApEn/SampEn    │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│                    DATA LAYER                         │
│  PostgreSQL + TimescaleDB (time-series) + Redis       │
└───────────────────────┬──────────────────────────────┘
                        │  BLE 5.0
┌───────────────────────▼──────────────────────────────┐
│                  HARDWARE LAYER                       │
│        ESP32 + MPU-6050 IMU — 100 Hz sampling        │
└──────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
Non-Invasive-Wearable-Motion-Analyzer/
├── firmware/               # ESP32 firmware (PlatformIO / Arduino)
│   ├── src/
│   │   ├── main.cpp
│   │   ├── imu_driver.cpp
│   │   ├── ble_handler.cpp
│   │   └── data_buffer.cpp
│   └── platformio.ini
│
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── api/            # Route handlers
│   │   ├── core/           # Config, DB, Security
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── processing/     # Signal processing engine
│   │   ├── hardware/       # BLE gateway
│   │   └── websocket/      # Real-time streaming
│   ├── migrations/         # Alembic migrations
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React + Vite dashboard
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Screen definitions
│   │   ├── hooks/          # Custom React hooks
│   │   └── api/            # API client
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docs/                   # Project documentation
│   ├── PRD.md
│   ├── TRD.md
│   ├── Backend_Schema.md
│   ├── UIUX_Design_Documentation.md
│   └── Webflow.md
│
├── docker-compose.yml      # Development stack
├── docker-compose.prod.yml # Production overrides
├── .env.example            # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend build |
| Docker + Compose | Latest | Database services |
| PlatformIO | Latest | Firmware compilation |
| Git | 2.x | Version control |

### 1. Clone & Configure

```bash
git clone https://github.com/dreamybear66/Non-Invasive-Wearable-Motion-Analyzer-Using-Entropy-Based-Signal-Processing.git
cd Non-Invasive-Wearable-Motion-Analyzer-Using-Entropy-Based-Signal-Processing

# Copy environment template
cp .env.example .env
# Edit .env with your values (DB password, secret keys, etc.)
```

### 2. Start Infrastructure

```bash
docker-compose up -d db redis
# Wait ~10 seconds for TimescaleDB to initialize
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

Backend available at: `http://localhost:8000`  
API docs at: `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:5173`

### 5. Full Stack (Docker)

```bash
docker-compose up --build
```

All services start together:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- TimescaleDB: `localhost:5432`
- Redis: `localhost:6379`

---

## 🧬 Signal Processing Pipeline

```
Raw IMU Signal (100 Hz)
        │
        ▼
1. Calibration Correction    (remove sensor bias offset)
        │
        ▼
2. Butterworth Low-Pass Filter  (4th order, 20 Hz cutoff)
        │
        ▼
3. Z-score Normalization     (60-second rolling window)
        │
        ▼
4. Artifact Detection        (flag |z| > 5σ samples)
        │
        ▼
5. Time-Window Segmentation  (5s windows, 50% overlap)
        │
        ▼
6. Entropy Computation
   ├── Approximate Entropy (ApEn)   — m=2, r=0.2×std
   ├── Sample Entropy (SampEn)      — m=2, r=0.2×std
   └── Permutation Entropy (PermEn) — order=3 (fast mode)
        │
        ▼
7. Fatigue Index Score (FIS 0–100)
        │
        ▼
8. State Classification
   ├── Normal        (FIS 0–20)  🟢
   ├── Early Fatigue (FIS 21–40) 🟡
   ├── Moderate      (FIS 41–65) 🟠
   └── High Fatigue  (FIS 66–100)🔴
```

---

## 🔌 API Reference

Full interactive docs: `http://localhost:8000/docs`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate, receive JWT |
| `POST` | `/api/v1/sessions` | Start a new monitoring session |
| `PATCH` | `/api/v1/sessions/{id}/end` | End an active session |
| `POST` | `/api/v1/sessions/{id}/raw-data` | Upload IMU data batch |
| `GET` | `/api/v1/sessions/{id}/entropy` | Get entropy time series |
| `GET` | `/api/v1/sessions/{id}/fatigue-index` | Get FIS over time |
| `GET` | `/api/v1/sessions/{id}/alerts` | Get fatigue event log |
| `GET` | `/api/v1/athletes` | List all athletes |
| `GET` | `/api/v1/sessions/{id}/report` | Export session report |
| `WSS` | `/ws/sessions/{id}/live` | Real-time streaming |

---

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app --cov-report=term-missing

# Frontend tests
cd frontend
npm run test
```

---

## 🌿 Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable releases only |
| `dev` | Integration branch — all features merge here first |
| `feature/*` | Individual feature development |
| `fix/*` | Bug fixes |
| `release/*` | Release preparation |

---

## 📚 Documentation

| Document | Description |
|---|---|
| [PRD](docs/PRD.md) | Product Requirements Document |
| [TRD](docs/TRD.md) | Technical Requirements Document |
| [Backend Schema](docs/Backend_Schema.md) | Database schema & TimescaleDB setup |
| [UI/UX Design](docs/UIUX_Design_Documentation.md) | Full design system documentation |
| [Webflow](docs/Webflow.md) | Screen layouts & navigation spec |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Firmware | ESP32 · MPU-6050 · NimBLE · PlatformIO |
| Backend | Python 3.11 · FastAPI · SQLAlchemy · Alembic |
| Signal Processing | NumPy · SciPy · antropy |
| Database | PostgreSQL 15 · TimescaleDB · Redis 7 |
| Frontend | React 18 · Vite · Recharts · GSAP |
| DevOps | Docker · Docker Compose · GitHub Actions |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built by <a href="https://github.com/dreamybear66">@dreamybear66</a> · Sports EL v1.0
</p>
