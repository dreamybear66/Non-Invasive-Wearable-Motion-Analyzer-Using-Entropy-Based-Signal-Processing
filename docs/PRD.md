# 📋 Product Requirements Document (PRD)
## Sports EL — Early Athletic Fatigue Detection System
**Version:** 1.0  
**Date:** June 2026  
**Status:** Draft  
**Project Code:** SPORTS-EL

---

## 1. Executive Summary

**Sports EL** is a wearable-integrated, software-driven platform for the **non-invasive, real-time early detection of athletic fatigue** using entropy-based analysis of motion signals. By leveraging Inertial Measurement Units (IMUs) attached to athletes, the system collects raw acceleration and angular velocity data, processes it through a signal pipeline (filtering → segmentation → entropy computation), and produces fatigue indicators *before* visible performance decline occurs.

The core insight is that **fatigue alters neuromuscular control**, causing measurable increases in the complexity and irregularity of motion signals — detectable via entropy metrics such as Approximate Entropy (ApEn) and Sample Entropy (SampEn).

---

## 2. Problem Statement

Athletic fatigue develops gradually during physical activity and often manifests **before any visible decline in performance**. Left undetected, it leads to:
- Reduced athletic efficiency and skill degradation
- Overtraining syndrome and increased injury risk
- Suboptimal training load management

**Existing limitations:**
| Approach | Limitation |
|---|---|
| Blood lactate analysis | Invasive, lab-bound |
| Electromyography (EMG) | Requires electrode attachment, not suited for real-time |
| Heart rate / perceived exertion | Subjective, lags behind actual fatigue onset |
| Linear kinematic metrics | Cannot capture nonlinear neuromuscular changes |

**Gap:** No reliable, non-invasive, continuous method exists for **early** fatigue detection using motion signals in real-world training environments.

---

## 3. Product Vision

> *"Empower athletes and coaches with an intelligent wearable system that detects the invisible onset of fatigue — before performance suffers."*

**Sports EL** will be the first entropy-driven motion analytics platform designed for continuous, real-world athletic monitoring.

---

## 4. Target Users / Personas

### 4.1 Athlete (Primary User)
- **Age:** 16–35
- **Context:** Training sessions, competition warm-ups
- **Needs:** Real-time awareness of fatigue levels; injury prevention
- **Pain Points:** Doesn't know when to reduce intensity; coaches rely on observation

### 4.2 Coach / Sports Scientist (Primary User)
- **Age:** 28–55
- **Context:** Field-side monitoring, post-session analysis
- **Needs:** Objective fatigue data per athlete; comparative analysis
- **Pain Points:** Relies on subjective cues; no continuous data stream

### 4.3 Sports Physiotherapist (Secondary User)
- **Age:** 25–50
- **Context:** Recovery planning, injury prevention
- **Needs:** Historical fatigue patterns; correlation with injury incidents
- **Pain Points:** Lack of quantitative pre-injury fatigue data

### 4.4 Researcher / Academic (Secondary User)
- **Context:** Lab or field study environments
- **Needs:** Raw signal access, configurable parameters, exportable data
- **Pain Points:** Tools are either too clinical or too consumer-grade

---

## 5. Core Features & Functional Requirements

### 5.1 Data Acquisition Module
| ID | Requirement |
|---|---|
| FR-01 | System SHALL support IMU sensors measuring 3-axis acceleration (±8g range) and 3-axis angular velocity |
| FR-02 | System SHALL support sampling frequencies of 50Hz, 100Hz, and 200Hz (configurable) |
| FR-03 | System SHALL support wireless data transmission (BLE/Wi-Fi) from wearable to processing unit |
| FR-04 | System SHALL support sensor placement at lower back, wrist, or ankle |
| FR-05 | System SHALL buffer up to 30 minutes of raw motion data locally on device |

### 5.2 Signal Preprocessing Module
| ID | Requirement |
|---|---|
| FR-06 | System SHALL apply low-pass/band-pass filtering to remove motion artifacts and high-frequency noise |
| FR-07 | System SHALL normalize signals to a standard range to reduce inter-session variability |
| FR-08 | System SHALL detect and mark invalid/corrupted signal segments |
| FR-09 | System SHALL segment processed signals into configurable time windows (default: 5 seconds) |

### 5.3 Feature Extraction (Entropy Engine)
| ID | Requirement |
|---|---|
| FR-10 | System SHALL compute Approximate Entropy (ApEn) for each signal segment |
| FR-11 | System SHALL compute Sample Entropy (SampEn) for each signal segment |
| FR-12 | System SHALL support additional entropy metrics (Permutation Entropy, Fuzzy Entropy) as configurable options |
| FR-13 | System SHALL compute entropy per axis (X, Y, Z) and produce aggregate scores |
| FR-14 | Entropy computation SHALL complete within 500ms per 5-second segment |

### 5.4 Fatigue Detection & Alerting
| ID | Requirement |
|---|---|
| FR-15 | System SHALL classify fatigue state as: `Normal`, `Early Fatigue`, `Moderate Fatigue`, `High Fatigue` |
| FR-16 | System SHALL generate real-time alerts when fatigue threshold is crossed |
| FR-17 | System SHALL provide a Fatigue Index Score (0–100) updated every 10 seconds |
| FR-18 | System SHALL allow coaches to configure per-athlete fatigue alert thresholds |

### 5.5 Visualization & Dashboard
| ID | Requirement |
|---|---|
| FR-19 | System SHALL display real-time entropy trend charts (line graphs) during session |
| FR-20 | System SHALL show per-segment fatigue timeline across the session |
| FR-21 | System SHALL support session replay with entropy overlay |
| FR-22 | System SHALL generate post-session PDF/CSV reports |
| FR-23 | System SHALL support multi-athlete monitoring on a single coach dashboard |

### 5.6 Data Management
| ID | Requirement |
|---|---|
| FR-24 | System SHALL store all sessions with athlete ID, timestamp, raw signals, entropy features |
| FR-25 | System SHALL support data export in CSV and JSON formats |
| FR-26 | System SHALL retain session data for a minimum of 12 months |

---

## 6. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Latency** | Real-time entropy analysis latency ≤ 1 second end-to-end |
| **Accuracy** | Fatigue onset detection sensitivity ≥ 85%, specificity ≥ 80% |
| **Reliability** | System uptime ≥ 99.5% for cloud backend |
| **Battery Life** | Wearable device SHALL operate ≥ 4 hours continuous on a single charge |
| **Connectivity** | System SHALL function in Wi-Fi and Bluetooth environments; offline mode for local storage |
| **Security** | All athlete data SHALL be encrypted at rest (AES-256) and in transit (TLS 1.3) |
| **Scalability** | Platform SHALL support up to 50 simultaneous athlete sessions per organization |
| **Usability** | Dashboard SHALL be operable by non-technical coaches within 10 minutes of onboarding |
| **Portability** | Wearable SHALL weigh ≤ 30g and be water-resistant (IP54 minimum) |
| **Compliance** | System SHALL comply with GDPR / applicable health data privacy regulations |

---

## 7. Success Metrics (KPIs)

| Metric | Target |
|---|---|
| Fatigue detection accuracy | ≥ 85% sensitivity vs. gold-standard EMG |
| Mean time to fatigue alert (from onset) | ≤ 45 seconds |
| Athlete onboarding time | ≤ 5 minutes per session setup |
| Coach dashboard adoption | ≥ 80% session usage after 2 weeks |
| Data export success rate | 100% |
| System downtime per month | < 4 hours |

---

## 8. Constraints & Assumptions

### Constraints
- Initial prototype is **software-only** (simulation mode using recorded datasets)
- Hardware wearable integration in Phase 2
- Processing pipeline limited to Python/MATLAB toolchain

### Assumptions
- Athletes will wear sensors consistently throughout training
- Coaches have basic digital literacy
- IMU sensors are pre-calibrated before each session

---

## 9. Out of Scope (v1.0)

- Nutrition/hydration integration
- GPS/location tracking
- Sport-specific fatigue models (sport-agnostic in v1.0)
- AI/ML-based predictive modeling (entropy rules-based only in v1.0)
- Mobile app (web dashboard only in v1.0)

---

## 10. Timeline Overview

| Phase | Deliverable | Duration |
|---|---|---|
| Phase 1 | Literature review & sensor selection | Weeks 1–2 |
| Phase 2 | Data acquisition setup | Weeks 3–4 |
| Phase 3 | Signal preprocessing & segmentation | Weeks 5–6 |
| Phase 4 | Entropy feature extraction | Weeks 7–8 |
| Phase 5 | Result interpretation, validation & reporting | Weeks 9–10 |
