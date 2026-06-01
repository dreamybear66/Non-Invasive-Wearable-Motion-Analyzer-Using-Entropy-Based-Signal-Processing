# 🔧 Technical Requirements Document (TRD)
## Sports EL — Entropy-Based Athletic Fatigue Detection System
**Version:** 1.0  
**Date:** June 2026  
**Status:** Draft

---

## 1. System Architecture Overview

The Sports EL platform follows a **modular, layered architecture** with four primary layers:

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│          Web Dashboard (React/Vite + Chart.js)          │
└────────────────────────┬────────────────────────────────┘
                         │ REST API / WebSocket
┌────────────────────────▼────────────────────────────────┐
│                    APPLICATION LAYER                     │
│         FastAPI Backend (Python) + WebSocket Server      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│               SIGNAL PROCESSING ENGINE                   │
│   Preprocessing → Segmentation → Entropy Computation    │
│          (Python: NumPy, SciPy, custom ApEn/SampEn)     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   DATA LAYER                             │
│   PostgreSQL (structured) + TimescaleDB (time-series)   │
│            + Redis (real-time caching)                   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   HARDWARE LAYER                         │
│      IMU Wearable (MPU-6050/ICM-42688) + BLE/Wi-Fi      │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Hardware Specifications

### 2.1 IMU Sensor Requirements
| Parameter | Specification |
|---|---|
| Sensor Model | MPU-6050 / ICM-42688-P (recommended) |
| Axes | 6-DOF (3-axis accel + 3-axis gyro) |
| Accelerometer Range | ±2g / ±4g / ±8g / ±16g (configurable) |
| Gyroscope Range | ±250 / ±500 / ±1000 / ±2000 °/s |
| Sampling Rate | 50–200 Hz (configurable, default: 100 Hz) |
| Interface | I²C / SPI to microcontroller |
| Output Format | 16-bit raw ADC values |

### 2.2 Microcontroller / BLE Module
| Parameter | Specification |
|---|---|
| MCU | ESP32 / Nordic nRF52840 |
| Connectivity | Bluetooth Low Energy 5.0 + Wi-Fi 802.11 b/g/n |
| Flash | ≥ 4 MB (local data buffering) |
| RAM | ≥ 512 KB |
| Battery | 3.7V LiPo, ≥ 500 mAh (≥ 4 hr operation) |
| Form Factor | ≤ 30g, IP54 water resistance |
| Charging | USB-C, ≥ 1C charge rate |

### 2.3 Sensor Placement Protocol
```
Primary Sites:
  - L4/L5 lumbar (lower back) — trunk motion analysis
  - Dominant wrist — arm swing analysis
  - Right ankle — gait pattern analysis

Attachment Method:
  - Elastic band / medical-grade adhesive
  - Calibration required before each session
```

---

## 3. Data Acquisition Specifications

### 3.1 BLE Data Protocol
```json
// BLE Characteristic: IMU Data Packet (20 bytes)
{
  "packet_id": "uint16",      // 2 bytes — rolling counter
  "timestamp_ms": "uint32",   // 4 bytes — ms since session start
  "acc_x": "int16",           // 2 bytes — raw accel X (scale: 1/1000 g)
  "acc_y": "int16",           // 2 bytes — raw accel Y
  "acc_z": "int16",           // 2 bytes — raw accel Z
  "gyro_x": "int16",          // 2 bytes — raw gyro X (scale: 1/100 °/s)
  "gyro_y": "int16",          // 2 bytes — raw gyro Y
  "gyro_z": "int16",          // 2 bytes — raw gyro Z
  "battery": "uint8",         // 1 byte  — battery level %
  "status": "uint8"           // 1 byte  — sensor status flags
}
```

### 3.2 Data Transmission
- **Protocol:** BLE GATT (notify mode) → edge relay → backend via HTTPS/WSS
- **Packet rate:** 100 packets/second at 100 Hz sampling
- **Buffer on device:** Circular buffer, 30-minute capacity (≈ 180,000 packets)
- **Data validation:** CRC-16 checksum per packet; dropped packets flagged

---

## 4. Signal Processing Engine

### 4.1 Preprocessing Pipeline

```
Raw IMU Signal
      │
      ▼
1. CALIBRATION CORRECTION
   - Remove sensor bias (zero-g offset)
   - Apply scale factor calibration
      │
      ▼
2. LOW-PASS FILTERING
   - Type: 4th-order Butterworth filter
   - Cutoff frequency: 20 Hz (configurable: 10–40 Hz)
   - Purpose: Remove high-frequency noise and vibration artifacts
      │
      ▼
3. NORMALIZATION
   - Z-score normalization per signal axis
   - Formula: x_norm = (x - μ) / σ
   - Computed per 60-second rolling window
      │
      ▼
4. ARTIFACT DETECTION & REMOVAL
   - Spike detection: |x| > 5σ flagged as artifact
   - Segment marked INVALID if >15% samples are artifacts
      │
      ▼
5. SEGMENTATION
   - Fixed time-window: 5 seconds (configurable: 2–10 s)
   - Overlap: 50% (configurable: 0–75%)
   - Output: Array of N-point segments per axis
```

### 4.2 Entropy Computation Algorithms

#### 4.2.1 Approximate Entropy (ApEn)
```
Parameters:
  - m (template length): 2
  - r (tolerance): 0.2 × std(signal_segment)

Algorithm:
  1. For each template vector X_m(i) of length m
  2. Count pairs where |X_m(i) - X_m(j)| < r for all dimensions
  3. C_m(r) = count / (N-m+1)
  4. ApEn(m, r, N) = Φ_m(r) - Φ_{m+1}(r)
     where Φ_m(r) = (N-m+1)^(-1) × Σ ln(C_m(r))

Output range: [0, ∞), higher = more irregular/complex
Fatigue interpretation: INCREASES with fatigue onset
```

#### 4.2.2 Sample Entropy (SampEn)
```
Parameters:
  - m (template length): 2
  - r (tolerance): 0.2 × std(signal_segment)

Algorithm:
  1. Template matching (excludes self-matches, unlike ApEn)
  2. A = number of template matches of length m+1
  3. B = number of template matches of length m
  4. SampEn(m, r, N) = -ln(A/B)

Advantages over ApEn:
  - No self-counting bias
  - More consistent for short segments
  - Recommended primary metric for fatigue detection

Output range: [0, ∞), lower = more regular movement
```

#### 4.2.3 Permutation Entropy (PermEn) — Optional
```
Parameters:
  - Order (d): 3–7
  - Delay (τ): 1

Output: Normalized value [0, 1]
Use case: Faster computation, good for real-time screening
```

### 4.3 Fatigue Index Calculation
```python
# Fatigue Index Score (FIS): 0–100
# Based on rolling entropy trend analysis

def compute_fatigue_index(entropy_series: List[float], baseline: float) -> float:
    """
    entropy_series: last 12 entropy values (60 seconds, 5s segments)
    baseline: mean entropy from first 60s (rested state)
    """
    current_mean = np.mean(entropy_series[-6:])  # last 30s
    delta = current_mean - baseline
    
    # Normalize delta to 0-100 scale
    # +delta = increasing entropy = fatigue signal
    fis = min(100, max(0, (delta / baseline) * 200))
    return fis

# Fatigue Threshold Classification:
# FIS 0–20:  Normal
# FIS 21–40: Early Fatigue (alert coach)
# FIS 41–65: Moderate Fatigue (recommend rest)
# FIS 66–100: High Fatigue (immediate intervention)
```

---

## 5. API Specifications

### 5.1 REST API Endpoints

#### Session Management
```
POST   /api/v1/sessions                    — Start new session
GET    /api/v1/sessions/{session_id}       — Get session details
PATCH  /api/v1/sessions/{session_id}/end   — End session
GET    /api/v1/sessions?athlete_id={id}    — List athlete sessions
```

#### Data Ingestion
```
POST   /api/v1/sessions/{id}/raw-data     — Upload IMU raw data batch
GET    /api/v1/sessions/{id}/signals      — Get preprocessed signals
```

#### Entropy & Fatigue
```
GET    /api/v1/sessions/{id}/entropy      — Get entropy time series
GET    /api/v1/sessions/{id}/fatigue-index — Get FIS over time
GET    /api/v1/sessions/{id}/alerts       — Get fatigue alerts
```

#### Athlete & User Management
```
POST   /api/v1/athletes                   — Create athlete profile
GET    /api/v1/athletes/{id}              — Get athlete details
GET    /api/v1/athletes/{id}/history      — Get fatigue history
```

#### Reports
```
GET    /api/v1/sessions/{id}/report       — Generate session report (PDF/CSV)
```

### 5.2 WebSocket API
```
WSS /ws/sessions/{session_id}/live

Messages from server:
{
  "type": "entropy_update",
  "timestamp": "ISO8601",
  "apen": 0.87,
  "sampen": 0.91,
  "fatigue_index": 34,
  "fatigue_state": "EARLY_FATIGUE"
}

{
  "type": "fatigue_alert",
  "severity": "WARNING",
  "message": "Early fatigue detected — consider reducing intensity"
}
```

---

## 6. Performance Requirements

| Metric | Target |
|---|---|
| End-to-end latency (sensor → dashboard) | ≤ 1,000 ms |
| Entropy computation per 5s segment | ≤ 500 ms |
| API response time (p95) | ≤ 200 ms |
| WebSocket message delivery | ≤ 100 ms |
| Concurrent sessions supported | ≥ 50 |
| Database write throughput | ≥ 500 data points/second |

---

## 7. Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | React (Vite) + Chart.js / Recharts | Fast SPA, excellent real-time charting |
| Backend API | FastAPI (Python 3.11+) | Async support, auto-documentation, native Python signal processing |
| Signal Processing | NumPy, SciPy, antropy library | Scientific computing, entropy algorithms |
| Real-time | WebSocket (Python websockets) | Low-latency live data streaming |
| Primary DB | PostgreSQL 15 | Relational data (athletes, sessions, users) |
| Time-series DB | TimescaleDB (PostgreSQL extension) | Optimized hypertable for sensor time-series |
| Caching | Redis 7 | Session state, real-time FIS caching |
| Auth | JWT (OAuth2) via FastAPI-Users | Secure, stateless authentication |
| Container | Docker + Docker Compose | Reproducible deployment |
| File Storage | MinIO / AWS S3 | Report files, exported CSVs |

---

## 8. Security Requirements

| Area | Requirement |
|---|---|
| Authentication | JWT Bearer tokens, 1-hour expiry with refresh |
| Authorization | RBAC: Athlete / Coach / Admin roles |
| Data at rest | AES-256 encryption for all stored sensor data |
| Data in transit | TLS 1.3 mandatory for all connections |
| PII handling | Athlete names pseudonymized by default |
| Audit log | All data access and modifications logged |
| Sensor pairing | Device pairing requires QR-code + PIN confirmation |

---

## 9. Testing Requirements

| Test Type | Coverage Target |
|---|---|
| Unit tests (signal processing) | ≥ 90% function coverage |
| Integration tests (API) | All critical paths covered |
| Performance tests | Load test: 50 concurrent sessions |
| Entropy algorithm validation | Validated against published benchmark datasets |
| End-to-end tests | Full sensor → dashboard flow tested |
