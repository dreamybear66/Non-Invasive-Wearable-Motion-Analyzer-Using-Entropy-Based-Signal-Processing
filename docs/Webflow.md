# 🎨 Webflow / UI-UX Design Specification
## Sports EL — Athletic Fatigue Detection Dashboard
**Version:** 1.0  
**Date:** June 2026

---

## 1. Design Philosophy

Sports EL's design is built on three pillars:
- **Clarity under pressure** — Coaches and athletes need instant, unambiguous information during live sessions
- **Data density without clutter** — Rich analytics displayed progressively without overwhelming the user
- **Trust through precision** — Scientific data must look precise and professional, not consumer-grade

**Design Paradigm:** Dark-mode dashboard with high-contrast status indicators, inspired by sports analytics platforms (Catapult, StatSports), medical monitoring (hospital vitals), and modern developer dashboards.

---

## 2. Color System

```
Primary Palette:
  Background:        #0A0E1A  (deep navy black)
  Surface:           #111827  (card background)
  Surface Elevated:  #1C2333  (elevated card)
  Border:            #1E293B  (subtle divider)

Brand:
  Primary:           #3B82F6  (electric blue)
  Primary Glow:      #3B82F620 (primary with 12% opacity for glow)
  Secondary:         #8B5CF6  (purple accent)
  
Fatigue States (Critical UI):
  Normal:            #22C55E  (green   — FIS 0–20)
  Early Fatigue:     #EAB308  (amber   — FIS 21–40)
  Moderate Fatigue:  #F97316  (orange  — FIS 41–65)
  High Fatigue:      #EF4444  (red     — FIS 66–100)
  
Text:
  Primary:           #F1F5F9
  Secondary:         #94A3B8
  Muted:             #475569
  
Data Visualization:
  ApEn Line:         #3B82F6  (blue)
  SampEn Line:       #8B5CF6  (purple)
  Threshold Line:    #EF444480 (red dashed, 50% opacity)
  Zone Fill:         gradient alpha fills per fatigue zone
```

---

## 3. Typography

```
Font Stack:
  Headings:    "Inter", sans-serif (Google Fonts)
  Body:        "Inter", sans-serif
  Monospace:   "JetBrains Mono", monospace (sensor data, values)
  
Scale:
  Display:     48px / 700 weight (hero numbers: FIS score)
  H1:          32px / 700
  H2:          24px / 600
  H3:          18px / 600
  Body:        14px / 400
  Small:       12px / 400
  Label:       11px / 500 / uppercase / letter-spacing: 0.08em
  Mono:        13px / 400 (entropy values, timestamps)
```

---

## 4. Component Library

### 4.1 Fatigue Gauge (Hero Widget)
```
Shape:          Arc gauge (180° half-circle)
Size:           240px diameter
Center Text:    Large FIS number (48px bold mono)
                Fatigue state label below (18px)
Arc Fill:       Animated gradient: green → amber → orange → red
Arc Track:      #1E293B (empty track)
Glow Effect:    Box-shadow with fatigue state color at 40% opacity
Animation:      Smooth 800ms easing on value change
```

### 4.2 Entropy Trend Chart
```
Library:        Recharts (LineChart)
Dimensions:     Full width, 280px height
Lines:          ApEn (blue, 2px), SampEn (purple, 2px)
Reference Line: Fatigue threshold (red dashed)
Zones:          Colored background bands for fatigue levels
Tooltip:        Dark glassmorphism tooltip with both values + state
X-Axis:         Time (MM:SS elapsed)
Y-Axis:         Entropy value (0–2.5 typical range)
Dot Style:      No dots for density; 6px dot on hover
Animation:      New data points animate in from right (1s)
```

### 4.3 Session Status Card
```
Layout:         Horizontal card with icon + label + value
States:         LIVE (pulsing green dot), COMPLETED, PAUSED
Metrics shown:  Duration | FIS | Peak Entropy | Segments Processed
Background:     #111827 with subtle blue-left border (4px)
```

### 4.4 Fatigue Alert Banner
```
Position:       Top of main content area (slide-down animation)
Variants:       INFO / WARNING / DANGER
Content:        Icon + message + timestamp + Dismiss button
WARNING:        Yellow-amber background with amber text
DANGER:         Red glow with pulsing border animation
Auto-dismiss:   DANGER alerts do NOT auto-dismiss (require manual action)
```

### 4.5 Athlete Avatar Chip
```
Shape:          Circle avatar (40px) + name + sport + status badge
Badge:          FIS-colored dot (top-right of avatar)
Hover:          Expand card with last session summary
Click:          Navigate to Athlete Profile
```

### 4.6 Data Table
```
Style:          Borderless rows, subtle hover (#1C2333)
Sorting:        Column header click with animated sort indicator
Pagination:     Compact (10 rows default), configurable
Export button:  Top-right of table
Loading state:  Skeleton shimmer animation
```

---

## 5. Screen Definitions

### Screen 1: Login / Landing
```
Layout:    Split screen: left = brand visual, right = auth form
Visual:    Animated particle background + silhouette of athlete
Form:      Email + Password + Login button
Extras:    "Remember me" toggle, "Forgot password" link
Brand:     Sports EL logo (top-left), tagline: "See fatigue before it sees you"
```

### Screen 2: Coach Dashboard (Home)
```
Header:
  - Sports EL logo (left)
  - Active sessions count badge (center)
  - Coach profile avatar + menu (right)

Sidebar (collapsed by default, 260px expanded):
  - Dashboard (home icon)
  - Live Sessions
  - Athletes
  - History
  - Reports
  - Settings

Main Content:
  ┌─────────────────────────────────────────────────────┐
  │ OVERVIEW STATS ROW                                   │
  │ [Active Sessions: 3] [Athletes Today: 8] [Alerts: 2]│
  ├─────────────────────────────────────────────────────┤
  │ LIVE SESSIONS GRID (2-3 columns)                     │
  │ ┌──────────────┐  ┌──────────────┐                  │
  │ │ ATHLETE NAME │  │ ATHLETE NAME │                  │
  │ │ Mini Gauge   │  │ Mini Gauge   │  ...             │
  │ │ FIS: 34      │  │ FIS: 67 🔴   │                  │
  │ │ EARLY FATIGUE│  │ HIGH FATIGUE │                  │
  │ └──────────────┘  └──────────────┘                  │
  ├─────────────────────────────────────────────────────┤
  │ RECENT ALERTS FEED (right panel)                     │
  │ 14:23 — John K. — High Fatigue Alert                │
  │ 14:18 — Sarah M. — Moderate Fatigue                 │
  └─────────────────────────────────────────────────────┘
```

### Screen 3: Live Session View
```
Layout:    Full-screen analytics view for one athlete
Header:    Athlete name | Sport | Session ID | LIVE indicator | Duration
Left:
  ┌──────────────────────────────────┐
  │  FATIGUE GAUGE (large, center)   │
  │       ██████ FIS: 42 ██████      │
  │      MODERATE FATIGUE            │
  │                                  │
  │  [Stop Session] [Mark Timestamp] │
  └──────────────────────────────────┘
Right Column:
  - Entropy Trend Chart (real-time, scrolling)
  - Signal Quality Indicator (per axis)
  - Session Event Timeline (fatigue state changes)
  
Bottom Row:
  - Raw Entropy Values Table (last 10 segments)
  - Segment metadata (timestamp, window, axes)
```

### Screen 4: Session History / Replay
```
Layout:    Timeline-based playback view
Timeline:  Horizontal scrubber with fatigue state color blocks
Charts:    Entropy overlay on selected time range
Filters:   Date range, athlete, fatigue level threshold
Export:    PDF / CSV buttons (top-right)
```

### Screen 5: Athlete Profile
```
Layout:    Two-column: left = profile info, right = history charts
Profile:   Avatar | Name | Age | Sport | Sensor ID | Join Date
Charts:
  - Long-term FIS trend (90 days)
  - Entropy distribution histogram
  - Fatigue state frequency donut chart
Sessions Table: Last 20 sessions with quick-access links
```

### Screen 6: Reports Page
```
Layout:    Filter panel (left) + report preview (right)
Filters:   Athlete | Date Range | Session | Metric
Preview:   Live PDF-style preview of selected report
Export:    "Download PDF" | "Export CSV" | "Share Link"
```

### Screen 7: Settings
```
Sections:
  - Organization: Name, logo, timezone
  - Athletes: Manage roster, sensor assignments
  - Thresholds: Per-athlete fatigue alert levels
  - Notifications: Email/SMS alert preferences
  - Security: Password, 2FA, active sessions
  - Data: Export all data, delete account
```

---

## 6. Navigation Flow

```
Login
  └── Coach Dashboard (Home)
        ├── Live Sessions → Live Session View
        │                       └── Post-Session → Session History (auto-navigate)
        ├── Athletes → Athlete List → Athlete Profile
        │                                └── Session Detail
        ├── History → Session History List → Session Replay
        ├── Reports → Report Generator → Download/Share
        └── Settings → Subsection Pages
```

---

## 7. Interaction Patterns

### Real-time Updates
- **WebSocket connection:** Reconnects automatically on drop (1s backoff)
- **Entropy chart:** New point animates in from right (300ms ease-out)
- **FIS gauge:** Value transitions smoothly (800ms spring animation)
- **Alert banner:** Slides down from top (400ms ease-out)
- **Status badges:** Pulse animation for LIVE indicators

### Loading States
- **Initial load:** Full-page skeleton with shimmer animation
- **Chart loading:** Pulsing placeholder chart
- **API calls:** Inline spinner on buttons; no full-page spinners

### Empty States
- **No active sessions:** Illustration + "Start a Session" CTA button
- **No athletes:** "Add your first athlete" onboarding card
- **No alerts:** Green checkmark + "All clear — no alerts today"

### Error States
- **Sensor disconnected:** Warning banner + reconnect button
- **API error:** Toast notification (bottom-right) with retry action
- **Session interrupted:** Modal with options: Resume / End / Save Partial

---

## 8. Responsive Layout

| Breakpoint | Layout |
|---|---|
| ≥ 1440px | Full sidebar + full charts + 3-col athlete grid |
| 1024–1439px | Collapsed sidebar + 2-col athlete grid |
| 768–1023px | Bottom navigation + stacked charts |
| < 768px | Mobile: Read-only view; alerts and FIS score only |

> [!NOTE]
> Full coaching functionality requires ≥ 1024px screen. Mobile (< 768px) is alert-only read mode for athletes/assistants.

---

## 9. Accessibility

| Requirement | Implementation |
|---|---|
| Color blindness | All fatigue states use both color + icon + label |
| Screen reader | ARIA labels on all interactive elements |
| Keyboard navigation | Tab order follows visual flow; Esc closes modals |
| Focus indicators | High-contrast 2px focus ring (brand blue) |
| Contrast ratio | All text meets WCAG AA (≥ 4.5:1) |
| Motion sensitivity | `prefers-reduced-motion` media query supported |
