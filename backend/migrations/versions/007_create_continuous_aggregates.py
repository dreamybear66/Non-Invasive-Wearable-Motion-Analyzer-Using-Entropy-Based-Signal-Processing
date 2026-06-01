"""create continuous aggregates

Revision ID: 007
Revises: 006
Create Date: 2026-06-01 10:06:00.000000

"""
from alembic import op

revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
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
    """)

    op.execute("""
    SELECT add_continuous_aggregate_policy('fatigue_minutely',
        start_offset => INTERVAL '2 hours',
        end_offset   => INTERVAL '30 seconds',
        schedule_interval => INTERVAL '30 seconds'
    );
    """)

    op.execute("""
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
    """)

def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW session_entropy_stats")
    op.execute("DROP MATERIALIZED VIEW fatigue_minutely")
