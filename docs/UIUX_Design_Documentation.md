# 🎨 UI/UX Design Documentation
## Sports EL — Athletic Fatigue Detection Platform
**Version:** 1.0  
**Date:** June 2026  
**Status:** Approved  
**Designer Reference:** Sports EL Design System v1

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing & Layout Tokens](#4-spacing--layout-tokens)
5. [Iconography](#5-iconography)
6. [Component Library](#6-component-library)
7. [Screen Definitions](#7-screen-definitions)
8. [Navigation Flow](#8-navigation-flow)
9. [Animation & Motion System](#9-animation--motion-system)
10. [3D Visual Layer — Three.js](#10-3d-visual-layer--threejs)
11. [Responsive Design](#11-responsive-design)
12. [Accessibility](#12-accessibility)
13. [Interaction Patterns](#13-interaction-patterns)

---

## 1. Design Philosophy

Sports EL's interface is built on three foundational principles that govern every design decision:

### 1.1 Clarity Under Pressure
Coaches and athletes make critical decisions in high-stress, time-sensitive environments. The UI must communicate fatigue status instantly — without requiring the user to read or interpret. Color, form, and position must all convey the same message simultaneously.

### 1.2 Data Density Without Clutter
The platform presents dense analytical data (entropy values, FIS scores, signal segments, timelines) without overwhelming the user. Information is presented in progressive layers — summary first, detail on demand.

### 1.3 Trust Through Precision
Scientific and biomechanical data must appear precise and measured. The visual language borrows from medical monitoring displays, sports telemetry systems, and professional analytics dashboards — not from consumer apps.

### 1.4 Design Paradigm
> **Dark-mode first, motion-aware, data-centric.**

The design is inspired by:
- **Catapult & StatSports** — professional sports telemetry dashboards
- **Hospital vitals monitors** — always-on, high-contrast, state-driven UI
- **Developer dashboards (Vercel, Linear)** — clean information hierarchy with excellent data type handling

---

## 2. Color System

The palette is purposefully restrained. Every color carries meaning. No decorative color is used — each hue maps to a semantic value.

### 2.1 Background & Surface Scale

| Token | Hex Value | Usage |
|---|---|---|
| `bg` | `#050912` | Page background — deepest layer |
| `surface` | `#0d1424` | Card backgrounds, primary containers |
| `surface-2` | `#111c30` | Elevated cards, input fields, secondary containers |
| `border` | `#1a2840` | All dividers, card outlines, separators |

> [!NOTE]
> The background is not pure black — it carries a deep navy undertone (`#050912`) which reduces eye strain during extended monitoring sessions and provides better contrast for blue-spectrum data visualizations.

### 2.2 Brand Colors

| Token | Hex | Usage |
|---|---|---|
| `primary-blue` | `#3b82f6` | Primary actions, active states, brand identity, links |
| `primary-glow` | `#3b82f620` | Blue glow overlays on hover/active states |
| `secondary-purple` | `#8b5cf6` | Secondary metric (SampEn line), accent decorations |
| `purple-glow` | `#8b5cf620` | Purple glow overlays |
| `cyan` | `#06b6d4` | Informational states, data gradient terminus, positive trends |

### 2.3 ⚡ Fatigue State Colors — Critical Semantic Palette

This is the most important color group in the entire system. These four colors appear across every layer of the application — sensor badges, gauge arcs, alert banners, timeline blocks, and session cards. They must never be used decoratively.

| State | Hex | FIS Range | Semantic Meaning |
|---|---|---|---|
| **Normal** | `#22c55e` | 0 – 20 | Athlete is performing within baseline parameters |
| **Early Fatigue** | `#eab308` | 21 – 40 | Entropy rising — coach awareness triggered |
| **Moderate Fatigue** | `#f97316` | 41 – 65 | Noticeable irregularity — rest recommendation |
| **High Fatigue** | `#ef4444` | 66 – 100 | Critical irregularity — immediate intervention required |

> [!IMPORTANT]
> Fatigue state must **always** be communicated through three channels simultaneously: **color** + **icon/symbol** + **text label**. Never rely on color alone — this is both an accessibility requirement and a redundancy safeguard for high-stress environments.

### 2.4 Text Scale

| Token | Hex | Usage |
|---|---|---|
| `text-primary` | `#f1f5f9` | Headlines, key values, primary content |
| `text-secondary` | `#94a3b8` | Supporting text, descriptions, placeholders |
| `text-muted` | `#475569` | Timestamps, metadata, disabled states |

### 2.5 Gradient Usage

| Gradient Name | Definition | Usage |
|---|---|---|
| Brand Gradient | `135deg · #3b82f6 → #8b5cf6` | CTA buttons, hero elements, badges |
| Data Gradient | `135deg · #3b82f6 → #06b6d4` | Gauge arcs, data highlights, FIS number fill |
| Fatigue Spectrum | `90deg · #22c55e → #eab308 → #f97316 → #ef4444` | Gauge arc background track, session timeline fills |

### 2.6 Opacity & Glow Rules

All glow effects are applied using the base color with specific opacity values:
- **Card hover glow:** Base color at `12%` opacity as background + `25%` border
- **Alert background fill:** Base color at `8%` opacity
- **Gauge glow ring:** Base color at `40%` opacity, `28px` blur radius
- **Particle glow:** Base color at `30–70%` opacity depending on layer depth

---

## 3. Typography

### 3.1 Font Families

| Family | Source | Role |
|---|---|---|
| **Inter** | Google Fonts | All UI text — headings, body, labels, buttons |
| **JetBrains Mono** | Google Fonts | All numeric data — entropy values, FIS scores, timestamps, hex values |

> [!TIP]
> JetBrains Mono is specifically chosen for data display because its tabular numerals prevent value columns from shifting width as numbers update in real-time, which is critical for the live entropy chart and FIS counter.

### 3.2 Type Scale

| Role | Size | Weight | Letter Spacing | Line Height | Font |
|---|---|---|---|---|---|
| **Display** | 48px | 900 | -0.04em | 1.0 | Inter |
| **H1** | 32px | 700 | -0.03em | 1.1 | Inter |
| **H2** | 24px | 600 | -0.02em | 1.2 | Inter |
| **H3** | 18px | 600 | -0.01em | 1.3 | Inter |
| **Body Large** | 16px | 400 | 0 | 1.7 | Inter |
| **Body** | 14px | 400 | 0 | 1.6 | Inter |
| **Small** | 12px | 400 | 0 | 1.5 | Inter |
| **Label** | 11px | 500 | +0.12em | 1.4 | Inter — UPPERCASE |
| **Mono Data** | 13px | 400–700 | 0 | 1.5 | JetBrains Mono |
| **Mono Hero** | 48px | 900 | -0.05em | 1.0 | JetBrains Mono |

### 3.3 Usage Examples by Context

- **FIS Score (hero):** Display · 48–72px · JetBrains Mono · 900 weight · Brand gradient fill
- **Section heading:** H2 · 24px · Inter · 600 · `text-primary`
- **Card sub-label:** Label · 11px · Inter · UPPERCASE · `text-muted`
- **Entropy values:** Mono Data · 13px · JetBrains Mono · `cyan`
- **Timestamps:** Mono Data · 11px · JetBrains Mono · `text-muted`
- **Alert title:** Body · 14px · Inter · 700 · Fatigue state color

---

## 4. Spacing & Layout Tokens

### 4.1 Base Unit
All spacing is derived from a **4px base unit**.

| Token | Value | Common Usage |
|---|---|---|
| `space-1` | 4px | Icon-text gap, tight chip padding |
| `space-2` | 8px | Internal component padding, badge padding |
| `space-3` | 12px | Small card inner padding |
| `space-4` | 16px | Standard gap, button padding |
| `space-5` | 20px | Card inner padding (compact) |
| `space-6` | 24px | Section inner padding, list gap |
| `space-8` | 32px | Card inner padding (standard) |
| `space-10` | 40px | Component group gap |
| `space-12` | 48px | Large section padding |
| `space-16` | 64px | Navigation height, section gap |
| `space-24` | 96px | Major section spacing |
| `space-30` | 120px | Hero vertical padding |

### 4.2 Border Radius Scale

| Token | Value | Usage |
|---|---|---|
| `radius-sm` | 6px | Tags, small badges, chips |
| `radius-md` | 10px | Input fields, small cards |
| `radius-lg` | 16px | Standard cards, modals |
| `radius-xl` | 20px | Large feature cards |
| `radius-full` | 9999px | Pills, badges, avatar chips |

### 4.3 Layout Grid

| Breakpoint | Columns | Gutter | Max Width |
|---|---|---|---|
| Mobile (< 768px) | 4 | 16px | 100% |
| Tablet (768–1023px) | 8 | 20px | 100% |
| Laptop (1024–1439px) | 12 | 24px | 1280px |
| Desktop (≥ 1440px) | 12 | 32px | 1440px |

### 4.4 Elevation / Shadow Scale

| Level | Application | Shadow Definition |
|---|---|---|
| Level 0 | Flat surfaces | No shadow |
| Level 1 | Standard cards | `0 1px 3px rgba(0,0,0,0.4)` |
| Level 2 | Hover state cards | `0 8px 24px rgba(59,130,246,0.08)` |
| Level 3 | Modals, dropdowns | `0 20px 60px rgba(0,0,0,0.6)` |
| Level 4 | Gauge glow | `0 0 40px [state-color]40` |
| Level 5 | DANGER alert | `0 0 30px rgba(239,68,68,0.3)` + animated border |

---

## 5. Iconography

### 5.1 Icon Library
**Primary:** Heroicons (Outline style, 24px stroke-width 1.5)  
**Fallback:** Lucide Icons (for any gaps in Heroicons)

### 5.2 Icon Usage Rules
- All icons default to `text-secondary` (`#94a3b8`)
- Active/selected icons use `primary-blue` (`#3b82f6`)
- Fatigue state icons follow the state color (never decorative)
- Icon + label pairs must always maintain an 8px minimum gap
- Icons in buttons are 20px; standalone section icons are 24px; mini indicators are 16px

### 5.3 Fatigue State Icons

| State | Icon | Symbol |
|---|---|---|
| Normal | `check-circle` | ● |
| Early Fatigue | `exclamation-triangle` | ⚠ |
| Moderate Fatigue | `exclamation-circle` | 🔶 |
| High Fatigue | `x-circle` (pulsing) | 🚨 |

---

## 6. Component Library

### 6.1 Fatigue Gauge

The hero widget of the entire platform. Appears prominently in the Live Session View and as a mini version in the Coach Dashboard athlete cards.

**Anatomy:**
- **Arc track:** 180° semicircle, 16px stroke, `border` color (`#1a2840`)
- **Zone rings:** Four colored background arcs corresponding to fatigue zones (8% opacity)
- **Active arc:** Animated fill arc, 16px stroke, `Data Gradient` fill
- **Glow arc:** Secondary arc at 28px stroke, 20–40% opacity — creates depth behind the main arc
- **Center value:** FIS number in JetBrains Mono, 48–72px, 900 weight, Brand gradient text fill
- **Sub-label:** "Fatigue Index" in Label style, `text-muted`
- **State badge:** Pill below the gauge with state color + icon + text
- **Tick marks:** Three structural ticks at 0%, 50%, 100% positions

**Size Variants:**
- **Full (Live Session):** 260px diameter arc, centered in viewport
- **Mini (Dashboard Card):** 120px diameter arc, right-aligned in card
- **Micro (Sidebar):** 48px diameter arc, icon-only with FIS tooltip

**Behavior:**
- Arc fill animates smoothly on every FIS update (800ms, spring easing)
- Gradient end-color transitions between state colors
- Glow shadow color transitions to match current fatigue state
- State badge text and color update with a brief scale pulse animation

---

### 6.2 Entropy Trend Chart

Real-time scrolling line chart displaying ApEn and SampEn values over session time.

**Visual Structure:**
- **Background zones:** Four horizontal band fills corresponding to fatigue levels (5–8% opacity)
- **Grid lines:** Horizontal only, subtle `border` color, at 0.5 entropy intervals
- **ApEn line:** Electric blue (`#3b82f6`), 2.5px stroke, with bezier smoothing between points
- **SampEn line:** Purple (`#8b5cf6`), 2.5px stroke, with bezier smoothing
- **Glow trails:** Each line has a 6px blurred duplicate at 30% opacity behind it for depth
- **Live dot:** Animated pulsing dot at the current data endpoint (each line)
- **Threshold line:** Red dashed horizontal line at the configured fatigue threshold
- **Tooltip:** Dark glassmorphism overlay on hover showing both values + state + time
- **Axis labels:** JetBrains Mono, `text-muted`, Y-axis = entropy value, X-axis = elapsed time

**Animation:**
- New data points enter from the right with a 300ms ease-out slide
- The chart viewport scrolls leftward continuously as new data arrives
- Glow dots pulse at 1.5s interval using sine wave opacity variation

---

### 6.3 Session Status Card

A horizontal card summarizing one athlete's current session state.

**Layout:** Icon (36×36, colored by state) → Athlete name + sport → FIS badge → Duration → Mini gauge

**States:**
- **ACTIVE:** Left border 4px `primary-blue`, live pulsing dot, real-time updating values
- **PAUSED:** Left border 4px `amber`, static display, "PAUSED" badge
- **COMPLETED:** Left border 4px `text-muted`, no animation, historical values shown
- **INTERRUPTED:** Left border 4px `red`, "!" icon, last known values shown

---

### 6.4 Fatigue Alert Banner

Three severity variants displayed as slide-down banners at the top of the main content area.

**INFO (Cyan):**
- Background: `#06b6d415` (8% cyan)
- Left accent bar: 3px solid `cyan`
- Icon: `ℹ` in cyan
- Auto-dismisses after 8 seconds

**WARNING (Amber):**
- Background: `#eab30815` (8% amber)
- Left accent bar: 3px solid `amber`
- Icon: `⚠` in amber
- Auto-dismisses after 15 seconds

**DANGER (Red):**
- Background: `#ef444415` (8% red)
- Left accent bar: 3px solid `red`
- Border: animated pulse between `#ef444440` and `#ef444480`
- Box shadow pulses: `0 0 20px rgba(239,68,68,0.2)` at 2s interval
- Icon: `🚨` with shake micro-animation on appear
- **Does NOT auto-dismiss** — requires deliberate coach action
- Audio notification triggered (configurable)

**Content Structure (all variants):**
- Icon · Alert Title (bold, state color) · Dismiss button (right)
- Alert message (body size, `text-secondary`)
- Timestamp · FIS at event · Entropy values (mono, `text-muted`)

---

### 6.5 Athlete Avatar Chip

A compact interactive element representing one athlete across the UI.

**Anatomy:**
- **Avatar:** 40×40px circle — initials on `surface-2` background, or profile photo
- **Name:** Body weight 600, `text-primary`
- **Sport tag:** Small label, `text-secondary`
- **State dot:** 10×10px circle on top-right of avatar, color = current fatigue state, pulsing if ACTIVE session

**Hover State:** Expands to a 240px card showing: last session date, peak FIS, current state  
**Click Behavior:** Navigates to Athlete Profile page

---

### 6.6 Navigation Sidebar

**Collapsed state (48px wide):** Icons only, tooltips on hover  
**Expanded state (260px wide):** Icons + labels + section groupings

**Sections:**
1. **Main:** Dashboard · Live Sessions · Athletes
2. **Analytics:** History · Reports
3. **Admin:** Settings · Team Management

**Active state:** Blue left border (3px) + `blue-glow` background + blue icon  
**Hover state:** `surface-2` background + white icon  
**Badge:** Red unread-count badge on "Live Sessions" when there are active alerts

---

### 6.7 Data Table

| Feature | Specification |
|---|---|
| Row height | 48px (standard), 64px (with sub-row) |
| Header | `surface-2` background, Label style, `text-muted` |
| Row hover | `surface-2` background, 200ms transition |
| Sort indicator | Animated chevron, blue when active |
| Pagination | Compact numeric, 10 rows default |
| Loading | Skeleton shimmer rows (3 visible) |
| Empty state | Centered illustration + descriptive label + CTA |
| Export button | Top-right of table header bar |

### 6.8 Button System

| Variant | Background | Text | Border | Usage |
|---|---|---|---|---|
| Primary | Brand Gradient | White | None | Main CTAs — Start Session, Confirm |
| Danger | Red-Orange Gradient | White | None | Destructive — End Session, Delete |
| Success | Green-Cyan Gradient | White | None | Positive confirm — Save, Approve |
| Secondary | Transparent | `text-primary` | `border` | Secondary — Export, Cancel |
| Ghost | Transparent | `text-secondary` | None | Tertiary — Dismiss, Skip |
| Icon | `surface-2` | Icon color | `border` | Icon-only actions |

**Sizes:** `sm` (32px height) · `md` (40px) · `lg` (48px)  
**States:** Default · Hover (translate-Y -2px + enhanced shadow) · Active (scale 0.98) · Disabled (40% opacity, no pointer events) · Loading (spinner replaces text)

---

### 6.9 Live Badge

A persistent indicator showing session is actively streaming data.

**Design:** Rounded pill · `#22c55e15` background · `#22c55e40` border · Green text  
**Content:** Pulsing green dot (8px) + "LIVE" text in Label style  
**Animation:** Dot pulses with a ring expansion (box-shadow) at 1.4s interval

---

### 6.10 Glassmorphism Tooltip

Applied to chart data points and icon hovers throughout.

**Design:** `rgba(13, 20, 36, 0.9)` background · 1px `border` · `backdrop-filter: blur(16px)` · `border-radius: 12px` · `box-shadow: 0 8px 24px rgba(0,0,0,0.5)`  
**Content:** Formatted in two columns — label (mono, muted) + value (mono, white)  
**Animation:** Fade-in 150ms ease-out · Follows cursor with 50ms lag

---

## 7. Screen Definitions

### Screen 1 — Login / Landing

**Purpose:** Entry point, brand first impression, authentication  
**Layout:** Full-bleed split — left panel (60%) = animated visual, right panel (40%) = auth form

**Left Panel:**
- Three.js animated particle field fills the entire panel
- Sports EL logo centered, large format (64px, white)
- Tagline below: *"See fatigue before it sees you"* — H2, `text-secondary`
- Subtle athlete silhouette illustration at panel base

**Right Panel:**
- White-on-dark form on `surface` background
- "Welcome back" heading (H1)
- Email field → Password field → Remember me toggle → Login button (full width, Primary style)
- "Forgot password" link below form
- Organization logo slot at top of right panel

---

### Screen 2 — Coach Dashboard (Home)

**Purpose:** Command center for monitoring all active athletes simultaneously  
**Layout:** Fixed sidebar (left) + Main content area (scrollable)

**Header Bar:**
- Left: Sports EL logo + current organization name
- Center: Active session count badge (animated, blue)
- Right: Coach avatar + name + dropdown menu

**Main Content — Top Row (Stats Cards):**
Three horizontal stat cards showing:
- Active Sessions count (with live indicator)
- Athletes monitored today
- Active alerts (red if > 0, normal if 0)

**Main Content — Live Sessions Grid:**
- 3-column card grid (2-column on laptop, 1-column on tablet)
- Each card: Athlete avatar chip + Mini gauge + FIS number + State label + FIS progress bar
- Cards sorted by FIS score descending (highest fatigue first)
- Cards animate to new sorted positions when FIS changes

**Right Panel — Alert Feed:**
- Chronological list of recent fatigue events
- Each entry: Time · Athlete name · State · FIS · Quick-action button ("View Session")
- Unread entries have left accent line in state color

---

### Screen 3 — Live Session View

**Purpose:** Full-focus single-athlete monitoring during an active training session  
**Layout:** Two-column — Left (40%) = Gauge + Controls, Right (60%) = Chart + Timeline

**Left Column:**
- Large Fatigue Gauge (full variant, centered)
- FIS value + State badge below gauge
- Session meta: Athlete name · Sport · Duration counter · Segment count
- "Pause Session" and "End Session" buttons
- "Mark Timestamp" button (creates a labeled event on timeline)

**Right Column:**
- Entropy Trend Chart (full width, 280px height)
- Signal Quality Bar: Three bars for X/Y/Z axes, color coded by noise level
- Session Event Timeline: Horizontal track showing fatigue state changes as colored blocks
- Recent Segments Table: Last 10 segments with time · ApEn · SampEn · FIS · State

**Alert Area:**
- Banners slide down from top of right column when state changes

---

### Screen 4 — Session History / Replay

**Purpose:** Post-session analysis and historical review  
**Layout:** Filter panel (left, collapsible 280px) + Main content (scrollable)

**Filter Panel:**
- Athlete selector (searchable dropdown)
- Date range picker
- Fatigue state filter (multi-select checkboxes)
- Activity type filter
- "Apply Filters" + "Reset" buttons

**Main Content:**
- Session list (data table format): Date · Athlete · Duration · Peak FIS · State · Segments · Actions
- Each row expands to show mini entropy chart preview
- "Replay" button opens session in replay mode

**Replay Mode:**
- Timeline scrubber at top (horizontal, draggable)
- Scrubber shows fatigue state color blocks across the full session
- Dragging scrubber updates the Entropy Chart and Gauge to that point in time
- "Play / Pause" controls for automatic replay at 10× speed

---

### Screen 5 — Athlete Profile

**Purpose:** Individual athlete history, patterns, and configuration  
**Layout:** Two-column — Left (30%) = Profile info, Right (70%) = Analytics

**Left Column:**
- Avatar (80px) + full name + athlete code + sport + position
- Quick stats: Total sessions · Avg FIS · Peak FIS ever
- Sensor assignment: Current paired sensor ID + battery level
- Alert threshold configuration: Three sliders (Early / Moderate / High FIS thresholds)
- Tags list

**Right Column — Analytics Tabs:**
- **Overview:** 90-day FIS trend (area chart) + Fatigue state frequency (donut chart)
- **Entropy:** Long-term ApEn + SampEn distribution histogram
- **Sessions:** Last 20 sessions table with sort/filter
- **Comparison:** Compare two date ranges side-by-side

---

### Screen 6 — Reports

**Purpose:** Generate and export session reports for coaching records, medical use, or research  
**Layout:** Filter sidebar (left) + Live PDF-style preview (right)

**Filter Controls:**
- Report type: Session Report · Athlete Summary · Team Overview · Custom
- Athlete / team selector
- Date range
- Metrics to include (multi-select): FIS trend · Entropy values · Event log · Signal quality

**Preview Panel:**
- Rendered report preview (styled as document)
- Auto-updates as filters change
- Watermark shows "PREVIEW" across preview

**Actions:**
- "Download PDF" (Primary button)
- "Export CSV" (Secondary button)
- "Copy Share Link" (Ghost button)
- "Schedule Weekly Report" (toggle)

---

### Screen 7 — Settings

**Purpose:** Organization and user configuration  
**Layout:** Left nav (settings categories) + Right content

**Categories:**
| Category | Contents |
|---|---|
| Organization | Name, logo upload, timezone, sport type |
| Team Management | Add/remove athletes, assign sensors, manage coaches |
| Alert Thresholds | Global default thresholds (per-athlete overrides in Profile) |
| Notifications | Email / SMS alert preferences, severity filter |
| Sensor Management | View all sensors, battery status, firmware version |
| Integrations | Webhooks, API keys, third-party exports |
| Security | Password change, 2FA setup, active sessions list |
| Data & Privacy | Export all data (ZIP), data retention settings, account deletion |
| Billing | Plan details, usage metrics, invoice history |

---

## 8. Navigation Flow

```
Login
  │
  └─► Coach Dashboard (Home)
          │
          ├─► Live Session View ──────────────────────────┐
          │       │                                        │
          │       └─► (session ends) ──────────────────────► Session History
          │
          ├─► Athletes List
          │       │
          │       └─► Athlete Profile ──────────────────────► Session Detail
          │
          ├─► History ──────────────────────────────────────► Session Replay
          │
          ├─► Reports ──────────────────────────────────────► Download / Share
          │
          └─► Settings
                  │
                  └─► [Subsection Pages]
```

**Navigation Rules:**
- Navigating away from an **ACTIVE** session triggers a confirmation modal ("Session is live — are you sure you want to leave?")
- The sidebar always shows the currently active sessions count as a live badge
- The browser `Back` button is supported and maintains correct state
- Deep links are supported for all screens (e.g., `/sessions/{id}/live`)

---

## 9. Animation & Motion System

Sports EL uses **GSAP (GreenSock Animation Platform)** as the primary animation engine. All motion is intentional and data-driven — no decorative animations that don't carry meaning.

### 9.1 GSAP Animation Library

| Animation Type | GSAP Method | Duration | Easing |
|---|---|---|---|
| Hero text entry (stagger) | `gsap.timeline` · `from` | 0.8–1.0s per element | `power3.out` |
| Scroll reveal (sections) | `ScrollTrigger` · `fromTo` | 0.9s | `power3.out` |
| Scroll reveal (stagger) | `ScrollTrigger` · `stagger: 0.1` | 0.6s each | `power2.out` |
| Card hover in | `gsap.to` (via CSS class) | 0.3s | `back.out(1.7)` — spring |
| Card hover out | `gsap.to` | 0.2s | `power2.in` |
| Gauge arc update | `gsap.to strokeDashoffset` | 1.2s | `power2.out` |
| Gauge value counter | `gsap.to` numeric value | 1.2s | `power2.out` |
| Alert slide-in | `gsap.from y: -80` | 0.5s | `expo.out` |
| Alert slide-out | `gsap.to y: -80, opacity: 0` | 0.3s | `power2.in` |
| Modal open | `gsap.from scale: 0.9, opacity: 0` | 0.4s | `back.out(1.7)` |
| Modal close | `gsap.to scale: 0.95, opacity: 0` | 0.25s | `power2.in` |
| Page transition in | `gsap.from y: 20, opacity: 0` | 0.4s | `power2.out` |
| Counter animation | `gsap.to` numeric target | 2.0s | `power2.out` |
| Chart data point entry | Canvas transform | 0.3s | `easeOut` |
| Fatigue state badge pulse | `gsap.fromTo scale: 0.9` | 0.5s | `back.out(1.7)` |
| Sidebar expand/collapse | `gsap.to width` | 0.3s | `power2.inOut` |

### 9.2 ScrollTrigger Configuration

- **Trigger:** `top 88%` — element starts animating when 88% into the viewport
- **toggleActions:** `play none none none` — animations play once on scroll-in, don't reverse on scroll-out
- **Stagger groups:** Color swatches stagger at `0.06s` · Type rows at `0.08s` · Cards at `0.1s`

### 9.3 Continuous Animations (Loop)

| Element | Animation | Period | Easing |
|---|---|---|---|
| Navigation logo dot | Scale 1 → 1.4, opacity 1 → 0.7 | 2.0s | `sine.inOut` |
| Live session badge dot | Pulse ring expansion | 1.4s | `power2.out` |
| High fatigue alert border | Opacity pulse `40%` → `80%` | 2.0s | `sine.inOut` |
| Gauge glow arc | Box-shadow size pulse | 2.5s | `sine.inOut` |
| Entropy chart live dot | Radius 5px → 8px + opacity | 1.5s | `sine.inOut` |
| Three.js particles | Rotation, drift, opacity pulse | Continuous | Perlin noise |
| Hero scroll hint | Float up/down 8px | 2.0s | `sine.inOut` |

### 9.4 Micro-Interactions

| Trigger | Response | Duration |
|---|---|---|
| Button hover | `translateY(-2px)` + enhanced box-shadow | 0.3s |
| Button click | `scale(0.97)` momentary press | 0.1s |
| Card hover | `translateY(-4px)` + blue glow border appears | 0.4s |
| Swatch hover | `scale(1.1)` + copy overlay appears | 0.2s |
| Flow node click | `scale(0.9 → 1.0)` spring bounce | 0.4s |
| Gauge state change | Badge `scale(0.9 → 1.0)` + color cross-fade | 0.5s |
| Alert dismiss | Slide-out left + height collapse | 0.3s |
| Sort column click | Chevron rotation 180° | 0.25s |
| Sidebar toggle | Width animate + icon fade | 0.3s |

### 9.5 Easing Reference Guide

| Easing | Behavior | When to Use |
|---|---|---|
| `power2.out` | Fast start, gentle deceleration | Data updates, chart entries |
| `power3.out` | Stronger fast start, smooth landing | Page reveals, hero elements |
| `expo.out` | Very fast initial burst, long tail | Alert banners, notifications |
| `back.out(1.7)` | Overshoots slightly, springs back | Card hovers, badge pulses, modals |
| `power2.inOut` | Smooth S-curve | Sidebar, toggles, tab switches |
| `sine.inOut` | Gentle sinusoidal | Loop animations, pulsing elements |

---

## 10. 3D Visual Layer — Three.js

Three.js is used exclusively for the **hero/login background** and as an optional ambient visual layer on the dashboard. It is **never used for data presentation** — all data charts use 2D Canvas or SVG.

### 10.1 Particle Network Scene

**Particle System Configuration:**
- **Count:** 1,200 particles
- **Distribution:** Randomized across a 220 × 220 × 120 unit volume
- **Size variation:** 0.5 – 2.5px (randomized per particle)
- **Depth:** Particles at different Z-depths create natural parallax

**Particle Colors — sampled from brand palette:**
- Electric Blue (`#3b82f6`) — 30% of particles
- Purple (`#8b5cf6`) — 20% of particles
- Cyan (`#06b6d4`) — 15% of particles
- Green (`#22c55e`) — 10% of particles
- Dim Navy Blue (`#1a3060`) — 25% of particles (background filler)

**Connection Lines:**
- Rendered as `LineSegments` between particles within 30 unit distance
- Blue (`#3b82f6`) at 6% opacity — very subtle
- Creates a "neural network" aesthetic that evokes neuromuscular signal analysis

**Camera & Motion:**
- Camera: `PerspectiveCamera`, 60° FOV, Z = 80 units
- **Mouse parallax:** Camera smoothly tracks mouse position (15 unit X range, 10 unit Y range), with 3% lerp factor per frame for smooth lag
- **Scene rotation:** Particle group rotates at 0.0004 rad/frame on Y-axis, 0.0001 rad/frame on X-axis

**Opacity Pulse:**
- Overall particle opacity oscillates between 0.5 and 0.65 using `sin(frame × 0.01)` — creates breathing effect

**Performance:**
- `PixelRatio` capped at 2 to prevent GPU overload on retina displays
- Particle system reuses a single geometry with `BufferAttribute` for efficiency
- Connection line computation done once at init (not per-frame)

### 10.2 Dashboard Ambient Layer (Optional)

On the Coach Dashboard, a minimal version of the Three.js scene runs at 20% opacity behind the content area — providing visual depth without distraction. This is disabled by default and enabled in user Settings → Appearance.

### 10.3 `prefers-reduced-motion` Behavior

When the OS-level reduced motion preference is detected:
- All Three.js animations pause (particles freeze)
- GSAP global timeline pauses
- CSS `animation` and `transition` are set to `0.01ms` via media query
- All scroll reveals fire instantly (no movement, just opacity change)

---

## 11. Responsive Design

### 11.1 Breakpoint System

| Name | Range | Columns | Sidebar |
|---|---|---|---|
| **Mobile** | `< 768px` | 4 | Bottom tab bar |
| **Tablet** | `768px – 1023px` | 8 | Bottom tab bar |
| **Laptop** | `1024px – 1439px` | 12 | Collapsed icon sidebar |
| **Desktop** | `≥ 1440px` | 12 | Full expanded sidebar |

### 11.2 Capability Matrix by Breakpoint

| Feature | Mobile | Tablet | Laptop | Desktop |
|---|---|---|---|---|
| FIS alert view | ✅ | ✅ | ✅ | ✅ |
| Push notifications | ✅ | ✅ | ✅ | ✅ |
| Single session view | ✅ | ✅ | ✅ | ✅ |
| Entropy chart | ❌ | ✅ (compact) | ✅ | ✅ |
| Multi-athlete dashboard | ❌ | ❌ | ✅ (2-col) | ✅ (3-col) |
| Chart configuration | ❌ | ❌ | ✅ | ✅ |
| Report generation | ❌ | ✅ (CSV only) | ✅ | ✅ |
| Settings (all) | ❌ | ✅ | ✅ | ✅ |
| Three.js ambient layer | ❌ | ❌ | Optional | Optional |

> [!WARNING]
> The Mobile view is intentionally limited to a read-only alert experience. Full coaching functionality requires a minimum screen width of 1024px. This is a deliberate design decision — not a future enhancement.

### 11.3 Mobile-Specific Design

**Navigation:** Bottom tab bar (5 items max) — replaces sidebar  
**Fatigue View:** Single large FIS number + State badge + Alert feed  
**Session Card:** Stacked layout, avatar top + FIS bottom  
**Typography:** Scale reduces by 10–15% across all headings  
**Touch targets:** Minimum 44×44px for all interactive elements

---

## 12. Accessibility

### 12.1 Color & Contrast

| Requirement | Standard | Implementation |
|---|---|---|
| Normal text contrast | WCAG AA (≥ 4.5:1) | `text-primary (#f1f5f9)` on `bg (#050912)` = 18.5:1 ✅ |
| Large text contrast | WCAG AA (≥ 3:1) | All H1–H3 exceed 7:1 ✅ |
| Interactive elements | WCAG AA (≥ 3:1) | All buttons exceed 4.5:1 ✅ |
| Fatigue state communication | WCAG (non-color) | Color + icon + text label — always all three ✅ |

### 12.2 Keyboard Navigation

- Full tab order follows visual reading order (top-left to bottom-right)
- All interactive elements are reachable by keyboard
- Modal dialogs trap focus within the modal while open
- `Escape` key closes all modals, dropdowns, and flyouts
- Arrow keys navigate within grouped components (tabs, table rows, list items)
- Focus indicator: 2px solid `#3b82f6` outline, 2px offset — never hidden

### 12.3 Screen Reader Support

- All images have descriptive `alt` attributes
- All icons have `aria-label` or adjacent visible text
- Live fatigue updates use `aria-live="polite"` for FIS score announcements
- Alert banners use `role="alert"` for immediate screen reader announcement
- Charts have `aria-label` describing the data trend and current values
- Form fields have `<label>` elements with explicit `for` associations

### 12.4 Reduced Motion

- `@media (prefers-reduced-motion: reduce)` disables all GSAP transitions
- Three.js particle animation pauses
- CSS animations set to `duration: 0.01ms`
- Scroll reveals become instant opacity changes (no movement)
- Pulsing elements (live dot, gauge glow) become static

### 12.5 Additional Accessibility Features

- All text can be resized up to 200% without horizontal scrolling
- Form error messages are linked to their fields via `aria-describedby`
- Loading states use `aria-busy="true"` on the affected containers
- Tooltips are accessible via keyboard focus (not hover-only)
- Color blind modes: All fatigue states use distinct icons as primary indicator

---

## 13. Interaction Patterns

### 13.1 Loading States

| Context | Loading Pattern |
|---|---|
| Initial page load | Full-page skeleton with shimmer animation |
| Chart loading | Pulsing placeholder chart area (same dimensions) |
| Button action | Spinner icon replaces button text; button disabled |
| Table rows | 3 shimmer skeleton rows |
| Data refresh | Non-blocking in-place spinner (top-right of component) |

### 13.2 Empty States

| Context | Empty State Design |
|---|---|
| No active sessions | Centered illustration + "Start a New Session" CTA |
| No athletes in org | "Add your first athlete" onboarding card |
| No alerts today | Green checkmark + "All clear — no fatigue alerts today" |
| No sessions in history | Calendar illustration + date filter suggestion |
| Session with no data | "Waiting for sensor data…" with animated dots |

### 13.3 Error States

| Error Type | UI Response |
|---|---|
| API error | Bottom-right toast notification, 5s auto-dismiss, Retry button |
| Sensor disconnected | Warning banner at top of session view + reconnect button |
| Session interrupted | Modal with options: Resume / End / Save Partial |
| Invalid form input | Inline red error text below field, field border turns red |
| Network offline | Persistent top banner, grey out live-update components |

### 13.4 Confirmation Dialogs

Required for all destructive or irreversible actions:
- End Session
- Delete Athlete Profile
- Revoke API Key
- Delete Account

**Dialog structure:** Title · Risk description (amber/red text) · Cancel (secondary) · Confirm (danger button)  
**Animation:** Modal fades in + scales from 0.9 to 1.0 using `back.out(1.7)`

### 13.5 Toast Notification System

- **Position:** Bottom-right corner, 20px from edges
- **Stack:** Up to 3 toasts visible at once; oldest auto-dismisses first
- **Types:** Success (green) · Info (blue) · Warning (amber) · Error (red)
- **Auto-dismiss:** 5 seconds (configurable per toast)
- **Entry animation:** Slide in from right + fade in, 0.4s `expo.out`
- **Exit animation:** Slide out right + fade out, 0.25s `power2.in`

---

*Document maintained by the Sports EL Design Team · Last updated: June 2026*
