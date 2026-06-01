"""create sessions

Revision ID: 004
Revises: 003
Create Date: 2026-06-01 10:03:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE sessions (
        id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        athlete_id      UUID NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
        coach_id        UUID REFERENCES users(id),
        organization_id UUID NOT NULL REFERENCES organizations(id),
        session_name    VARCHAR(255),
        sport_activity  VARCHAR(100),
        status          session_status DEFAULT 'ACTIVE',
        started_at      TIMESTAMPTZ DEFAULT NOW(),
        ended_at        TIMESTAMPTZ,
        duration_seconds INTEGER GENERATED ALWAYS AS (
                          EXTRACT(EPOCH FROM (COALESCE(ended_at, NOW()) - started_at))::INTEGER
                        ) STORED,
        sampling_rate_hz INTEGER DEFAULT 100,
        window_size_sec  FLOAT DEFAULT 5.0,
        window_overlap   FLOAT DEFAULT 0.5,
        filter_cutoff_hz FLOAT DEFAULT 20.0,
        peak_fis         FLOAT,
        mean_fis         FLOAT,
        peak_fatigue_state fatigue_state,
        baseline_apen    FLOAT,
        baseline_sampen  FLOAT,
        total_segments   INTEGER DEFAULT 0,
        alert_count      INTEGER DEFAULT 0,
        notes           TEXT,
        tags            TEXT[],
        created_at      TIMESTAMPTZ DEFAULT NOW(),
        updated_at      TIMESTAMPTZ DEFAULT NOW()
    );
    """)
    op.execute("CREATE INDEX idx_sessions_athlete ON sessions(athlete_id)")
    op.execute("CREATE INDEX idx_sessions_org ON sessions(organization_id)")
    op.execute("CREATE INDEX idx_sessions_started ON sessions(started_at DESC)")
    op.execute("CREATE INDEX idx_sessions_status ON sessions(status)")

def downgrade() -> None:
    op.drop_table('sessions')
