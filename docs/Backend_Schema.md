# 🗄️ Backend Database Schema
## Sports EL — Athletic Fatigue Detection System
**Version:** 1.0  
**Date:** June 2026  
**Database:** PostgreSQL 15 + TimescaleDB Extension

---

## 1. Entity Relationship Overview

```
organizations ─┬─ users (coaches, admins)
               └─ athletes ─┬─ sessions ─┬─ raw_imu_data        (timeseries)
                             │            ├─ preprocessed_signals (timeseries)
                             │            ├─ entropy_results      (timeseries)
                             │            ├─ fatigue_events
                             │            └─ session_reports
                             └─ athlete_sensors ─ sensors
```

---

## 2. Enumerations

```sql
-- Fatigue classification levels
CREATE TYPE fatigue_state AS ENUM (
    'NORMAL',
    'EARLY_FATIGUE',
    'MODERATE_FATIGUE',
    'HIGH_FATIGUE'
);

-- Sensor placement on body
CREATE TYPE sensor_placement AS ENUM (
    'LOWER_BACK',
    'RIGHT_WRIST',
    'LEFT_WRIST',
    'RIGHT_ANKLE',
    'LEFT_ANKLE',
    'CHEST'
);

-- Session status
CREATE TYPE session_status AS ENUM (
    'ACTIVE',
    'PAUSED',
    'COMPLETED',
    'INTERRUPTED'
);

-- User roles
CREATE TYPE user_role AS ENUM (
    'ADMIN',
    'COACH',
    'ATHLETE',
    'PHYSIOTHERAPIST'
);

-- Alert severity
CREATE TYPE alert_severity AS ENUM (
    'INFO',
    'WARNING',
    'DANGER'
);

-- Report format
CREATE TYPE report_format AS ENUM (
    'PDF',
    'CSV',
    'JSON'
);
```

---

## 3. Core Relational Tables

### 3.1 organizations
```sql
CREATE TABLE organizations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,  -- URL-safe identifier
    sport_type      VARCHAR(100),                  -- Football, Running, etc.
    logo_url        VARCHAR(500),
    timezone        VARCHAR(100) DEFAULT 'UTC',
    settings        JSONB DEFAULT '{}',            -- Threshold configs, etc.
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index for slug lookups
CREATE UNIQUE INDEX idx_organizations_slug ON organizations(slug);
```

### 3.2 users
```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email           VARCHAR(320) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(200) NOT NULL,
    role            user_role NOT NULL DEFAULT 'COACH',
    avatar_url      VARCHAR(500),
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_org ON users(organization_id);
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### 3.3 athletes
```sql
CREATE TABLE athletes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    -- Identity (pseudonymized by default)
    athlete_code    VARCHAR(50) UNIQUE NOT NULL,   -- Internal code e.g. "ATH-001"
    full_name       VARCHAR(200),                   -- Optional PII
    date_of_birth   DATE,
    sport           VARCHAR(100),
    position        VARCHAR(100),                   -- e.g., "Midfielder"
    gender          CHAR(1),                        -- M/F/O
    -- Fatigue baseline config
    baseline_apen   FLOAT,                         -- Per-athlete rested entropy baseline
    baseline_sampen FLOAT,
    fatigue_threshold_early    FLOAT DEFAULT 20.0, -- FIS threshold overrides
    fatigue_threshold_moderate FLOAT DEFAULT 40.0,
    fatigue_threshold_high     FLOAT DEFAULT 65.0,
    -- Metadata
    notes           TEXT,
    tags            TEXT[],                         -- e.g., ['sprinter', 'post-injury']
    is_active       BOOLEAN DEFAULT TRUE,
    created_by      UUID REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_athletes_org ON athletes(organization_id);
CREATE INDEX idx_athletes_code ON athletes(athlete_code);
```

### 3.4 sensors
```sql
CREATE TABLE sensors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    device_id       VARCHAR(100) UNIQUE NOT NULL,  -- MAC address or serial
    firmware_version VARCHAR(50),
    sensor_model    VARCHAR(100) DEFAULT 'MPU-6050',
    sampling_rate_hz INTEGER DEFAULT 100,
    battery_level   INTEGER,                       -- 0–100%
    last_seen_at    TIMESTAMPTZ,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sensors_device ON sensors(device_id);
```

### 3.5 athlete_sensors (Junction — active pairing)
```sql
CREATE TABLE athlete_sensors (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    athlete_id  UUID NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    sensor_id   UUID NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    placement   sensor_placement NOT NULL,
    paired_at   TIMESTAMPTZ DEFAULT NOW(),
    paired_by   UUID REFERENCES users(id),
    is_current  BOOLEAN DEFAULT TRUE,
    UNIQUE (sensor_id, is_current)  -- Only one active pairing per sensor
);

CREATE INDEX idx_athlete_sensors_athlete ON athlete_sensors(athlete_id);
```

### 3.6 sessions
```sql
CREATE TABLE sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    athlete_id      UUID NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    coach_id        UUID REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    -- Session info
    session_name    VARCHAR(255),
    sport_activity  VARCHAR(100),                  -- e.g., "Sprint Training"
    status          session_status DEFAULT 'ACTIVE',
    -- Timing
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    ended_at        TIMESTAMPTZ,
    duration_seconds INTEGER GENERATED ALWAYS AS (
                      EXTRACT(EPOCH FROM (COALESCE(ended_at, NOW()) - started_at))::INTEGER
                    ) STORED,
    -- Configuration
    sampling_rate_hz INTEGER DEFAULT 100,
    window_size_sec  FLOAT DEFAULT 5.0,
    window_overlap   FLOAT DEFAULT 0.5,           -- 0.0–1.0
    filter_cutoff_hz FLOAT DEFAULT 20.0,
    -- Aggregate results (computed at session end)
    peak_fis         FLOAT,
    mean_fis         FLOAT,
    peak_fatigue_state fatigue_state,
    baseline_apen    FLOAT,
    baseline_sampen  FLOAT,
    total_segments   INTEGER DEFAULT 0,
    alert_count      INTEGER DEFAULT 0,
    -- Metadata
    notes           TEXT,
    tags            TEXT[],
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sessions_athlete ON sessions(athlete_id);
CREATE INDEX idx_sessions_org ON sessions(organization_id);
CREATE INDEX idx_sessions_started ON sessions(started_at DESC);
CREATE INDEX idx_sessions_status ON sessions(status);
```

---

## 4. Time-Series Tables (TimescaleDB Hypertables)

> [!IMPORTANT]
> These tables use TimescaleDB hypertables for optimized time-series storage. The `time` column is the partitioning key.

### 4.1 raw_imu_data
```sql
CREATE TABLE raw_imu_data (
    time            TIMESTAMPTZ NOT NULL,          -- Partition key
    session_id      UUID NOT NULL REFERENCES sessions(id),
    sensor_id       UUID REFERENCES sensors(id),
    packet_id       INTEGER NOT NULL,              -- Rolling counter from firmware
    -- Accelerometer (g, 1g = 9.81 m/s²)
    acc_x           FLOAT NOT NULL,
    acc_y           FLOAT NOT NULL,
    acc_z           FLOAT NOT NULL,
    -- Gyroscope (°/s)
    gyro_x          FLOAT NOT NULL,
    gyro_y          FLOAT NOT NULL,
    gyro_z          FLOAT NOT NULL,
    -- Quality
    battery_pct     SMALLINT,                      -- 0–100
    is_valid        BOOLEAN DEFAULT TRUE,          -- FALSE if CRC error
    placement       sensor_placement
);

-- Create hypertable (partition by time, 1-day chunks)
SELECT create_hypertable('raw_imu_data', 'time', chunk_time_interval => INTERVAL '1 day');

-- Compression policy (auto-compress chunks older than 7 days)
ALTER TABLE raw_imu_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'session_id'
);
SELECT add_compression_policy('raw_imu_data', INTERVAL '7 days');

-- Indexes
CREATE INDEX idx_raw_imu_session ON raw_imu_data(session_id, time DESC);
```

### 4.2 preprocessed_signals
```sql
CREATE TABLE preprocessed_signals (
    time            TIMESTAMPTZ NOT NULL,          -- Partition key (segment start time)
    session_id      UUID NOT NULL REFERENCES sessions(id),
    segment_index   INTEGER NOT NULL,
    -- Filtered & normalized signal arrays (stored as float arrays)
    acc_x           FLOAT[] NOT NULL,              -- Array of N samples
    acc_y           FLOAT[] NOT NULL,
    acc_z           FLOAT[] NOT NULL,
    gyro_x          FLOAT[],
    gyro_y          FLOAT[],
    gyro_z          FLOAT[],
    -- Segment metadata
    samples_count   INTEGER NOT NULL,
    artifact_count  INTEGER DEFAULT 0,
    is_valid        BOOLEAN DEFAULT TRUE,          -- FALSE if >15% artifacts
    window_size_sec FLOAT
);

SELECT create_hypertable('preprocessed_signals', 'time', 
                          chunk_time_interval => INTERVAL '1 day');

CREATE INDEX idx_preprocessed_session ON preprocessed_signals(session_id, time DESC);
CREATE INDEX idx_preprocessed_segment ON preprocessed_signals(session_id, segment_index);
```

### 4.3 entropy_results
```sql
CREATE TABLE entropy_results (
    time            TIMESTAMPTZ NOT NULL,          -- Partition key (segment time)
    session_id      UUID NOT NULL REFERENCES sessions(id),
    segment_index   INTEGER NOT NULL,
    -- ApEn per axis
    apen_x          FLOAT,
    apen_y          FLOAT,
    apen_z          FLOAT,
    apen_combined   FLOAT,                         -- Mean of X,Y,Z
    -- SampEn per axis
    sampen_x        FLOAT,
    sampen_y        FLOAT,
    sampen_z        FLOAT,
    sampen_combined FLOAT,
    -- Permutation Entropy (optional, faster)
    perm_entropy_x  FLOAT,
    perm_entropy_y  FLOAT,
    perm_entropy_z  FLOAT,
    -- Fatigue scoring
    fatigue_index   FLOAT NOT NULL,               -- 0–100 FIS
    fatigue_state   fatigue_state NOT NULL,
    -- Algorithm parameters used
    m_param         INTEGER DEFAULT 2,             -- Template length
    r_param         FLOAT,                         -- Tolerance (absolute)
    UNIQUE (session_id, segment_index)
);

SELECT create_hypertable('entropy_results', 'time', 
                          chunk_time_interval => INTERVAL '1 day');

CREATE INDEX idx_entropy_session ON entropy_results(session_id, time DESC);
CREATE INDEX idx_entropy_state ON entropy_results(session_id, fatigue_state);
```

### 4.4 fatigue_events (Alerts Log)
```sql
CREATE TABLE fatigue_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    time            TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- Partition key
    session_id      UUID NOT NULL REFERENCES sessions(id),
    athlete_id      UUID NOT NULL REFERENCES athletes(id),
    -- Event details
    event_type      VARCHAR(50) NOT NULL,          -- 'STATE_CHANGE' | 'ALERT_TRIGGERED' | 'THRESHOLD_CROSSED'
    previous_state  fatigue_state,
    new_state       fatigue_state NOT NULL,
    fatigue_index   FLOAT NOT NULL,
    severity        alert_severity NOT NULL,
    message         TEXT,
    segment_index   INTEGER,
    -- Acknowledgement
    acknowledged    BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMPTZ,
    -- Context
    apen_at_event   FLOAT,
    sampen_at_event FLOAT
);

SELECT create_hypertable('fatigue_events', 'time',
                          chunk_time_interval => INTERVAL '7 days');

CREATE INDEX idx_events_session ON fatigue_events(session_id, time DESC);
CREATE INDEX idx_events_athlete ON fatigue_events(athlete_id, time DESC);
CREATE INDEX idx_events_unack ON fatigue_events(acknowledged, time DESC) 
    WHERE acknowledged = FALSE;
```

---

## 5. Supporting Tables

### 5.1 session_reports
```sql
CREATE TABLE session_reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES sessions(id),
    generated_by    UUID REFERENCES users(id),
    format          report_format NOT NULL,
    file_url        VARCHAR(500),                  -- S3/MinIO path
    file_size_bytes INTEGER,
    status          VARCHAR(50) DEFAULT 'PENDING', -- PENDING / COMPLETED / FAILED
    generated_at    TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ DEFAULT NOW() + INTERVAL '30 days'
);

CREATE INDEX idx_reports_session ON session_reports(session_id);
```

### 5.2 refresh_tokens
```sql
CREATE TABLE refresh_tokens (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash  VARCHAR(255) UNIQUE NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    is_revoked  BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ
);

CREATE INDEX idx_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_tokens_hash ON refresh_tokens(token_hash);
```

### 5.3 audit_log
```sql
CREATE TABLE audit_log (
    id          BIGSERIAL PRIMARY KEY,
    time        TIMESTAMPTZ DEFAULT NOW(),
    user_id     UUID REFERENCES users(id),
    action      VARCHAR(100) NOT NULL,             -- e.g., 'SESSION_CREATED'
    resource    VARCHAR(100),                      -- e.g., 'sessions'
    resource_id UUID,
    ip_address  INET,
    user_agent  TEXT,
    old_values  JSONB,
    new_values  JSONB
);

SELECT create_hypertable('audit_log', 'time', chunk_time_interval => INTERVAL '30 days');
CREATE INDEX idx_audit_user ON audit_log(user_id, time DESC);
CREATE INDEX idx_audit_resource ON audit_log(resource, resource_id);
```

---

## 6. Redis Caching Schema

```
Key Pattern                               TTL     Value
─────────────────────────────────────────────────────────
session:{session_id}:fis                  10s     FLOAT — current Fatigue Index Score
session:{session_id}:state                10s     STRING — current fatigue_state enum
session:{session_id}:entropy_buffer       60s     JSON LIST — last 12 entropy values
session:{session_id}:baseline             24h     FLOAT — session ApEn baseline
session:{session_id}:status               5m      STRING — ACTIVE/PAUSED/COMPLETED
athlete:{athlete_id}:active_session       5m      UUID — current session ID (or null)
org:{org_id}:active_sessions              30s     JSON LIST — all active session IDs
user:{user_id}:jwt_blacklist:{jti}        1h      "1" — revoked JWT tracking
ws:session:{session_id}:subscribers       ∞       SET — connected WebSocket client IDs
```

---

## 7. TimescaleDB Continuous Aggregates

```sql
-- Per-minute fatigue summary (materialized view, auto-refreshed)
CREATE MATERIALIZED VIEW fatigue_minutely
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 minute', time) AS bucket,
    session_id,
    AVG(fatigue_index)            AS avg_fis,
    MAX(fatigue_index)            AS max_fis,
    AVG(apen_combined)            AS avg_apen,
    AVG(sampen_combined)          AS avg_sampen,
    COUNT(*)                      AS segments
FROM entropy_results
GROUP BY bucket, session_id
WITH NO DATA;

-- Auto-refresh policy: refresh last 2 hours every 30 seconds
SELECT add_continuous_aggregate_policy('fatigue_minutely',
    start_offset => INTERVAL '2 hours',
    end_offset   => INTERVAL '30 seconds',
    schedule_interval => INTERVAL '30 seconds'
);

-- Per-session summary (for history views)
CREATE MATERIALIZED VIEW session_entropy_stats
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time)    AS day,
    session_id,
    AVG(fatigue_index)            AS avg_fis,
    MAX(fatigue_index)            AS peak_fis,
    AVG(sampen_combined)          AS mean_sampen,
    COUNT(CASE WHEN fatigue_state != 'NORMAL' THEN 1 END) AS fatigue_segments
FROM entropy_results
GROUP BY day, session_id
WITH NO DATA;
```

---

## 8. Database Migrations Strategy

**Tool:** Alembic (Python)

```
migrations/
├── env.py
├── script.py.mako
└── versions/
    ├── 001_create_enums.py
    ├── 002_create_organizations_users.py
    ├── 003_create_athletes_sensors.py
    ├── 004_create_sessions.py
    ├── 005_create_timeseries_tables.py
    ├── 006_create_hypertables.py
    ├── 007_create_continuous_aggregates.py
    └── 008_create_audit_refresh_tokens.py
```

---

## 9. Retention & Data Lifecycle

| Table | Retention | Policy |
|---|---|---|
| raw_imu_data | 90 days (rolling) | TimescaleDB drop_chunks policy |
| preprocessed_signals | 90 days | Drop_chunks policy |
| entropy_results | 2 years | Archive to cold storage after 1 year |
| fatigue_events | 3 years | No auto-deletion |
| sessions | Indefinite | Manual deletion only |
| audit_log | 7 years | Compliance requirement |

```sql
-- Auto-drop raw IMU data older than 90 days
SELECT add_retention_policy('raw_imu_data', INTERVAL '90 days');
SELECT add_retention_policy('preprocessed_signals', INTERVAL '90 days');
```
