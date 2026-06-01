"""create hypertables

Revision ID: 006
Revises: 005
Create Date: 2026-06-01 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE entropy_results (
        time            TIMESTAMPTZ NOT NULL,
        session_id      UUID NOT NULL REFERENCES sessions(id),
        segment_index   INTEGER NOT NULL,
        apen_x          FLOAT,
        apen_y          FLOAT,
        apen_z          FLOAT,
        apen_combined   FLOAT,
        sampen_x        FLOAT,
        sampen_y        FLOAT,
        sampen_z        FLOAT,
        sampen_combined FLOAT,
        perm_entropy_x  FLOAT,
        perm_entropy_y  FLOAT,
        perm_entropy_z  FLOAT,
        fatigue_index   FLOAT NOT NULL,
        fatigue_state   fatigue_state NOT NULL,
        m_param         INTEGER DEFAULT 2,
        r_param         FLOAT,
        UNIQUE (session_id, segment_index)
    );
    """)
    op.execute("SELECT create_hypertable('entropy_results', 'time', chunk_time_interval => INTERVAL '1 day')")
    op.execute("CREATE INDEX idx_entropy_session ON entropy_results(session_id, time DESC)")
    op.execute("CREATE INDEX idx_entropy_state ON entropy_results(session_id, fatigue_state)")

    op.execute("""
    CREATE TABLE fatigue_events (
        id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        time            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        session_id      UUID NOT NULL REFERENCES sessions(id),
        athlete_id      UUID NOT NULL REFERENCES athletes(id),
        event_type      VARCHAR(50) NOT NULL,
        previous_state  fatigue_state,
        new_state       fatigue_state NOT NULL,
        fatigue_index   FLOAT NOT NULL,
        severity        alert_severity NOT NULL,
        message         TEXT,
        segment_index   INTEGER,
        acknowledged    BOOLEAN DEFAULT FALSE,
        acknowledged_by UUID REFERENCES users(id),
        acknowledged_at TIMESTAMPTZ,
        apen_at_event   FLOAT,
        sampen_at_event FLOAT
    );
    """)
    op.execute("SELECT create_hypertable('fatigue_events', 'time', chunk_time_interval => INTERVAL '7 days')")
    op.execute("CREATE INDEX idx_events_session ON fatigue_events(session_id, time DESC)")
    op.execute("CREATE INDEX idx_events_athlete ON fatigue_events(athlete_id, time DESC)")
    op.execute("CREATE INDEX idx_events_unack ON fatigue_events(acknowledged, time DESC) WHERE acknowledged = FALSE")

def downgrade() -> None:
    op.drop_table('fatigue_events')
    op.drop_table('entropy_results')
