"""create timeseries tables

Revision ID: 005
Revises: 004
Create Date: 2026-06-01 10:04:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE raw_imu_data (
        time            TIMESTAMPTZ NOT NULL,
        session_id      UUID NOT NULL REFERENCES sessions(id),
        sensor_id       UUID REFERENCES sensors(id),
        packet_id       INTEGER NOT NULL,
        acc_x           FLOAT NOT NULL,
        acc_y           FLOAT NOT NULL,
        acc_z           FLOAT NOT NULL,
        gyro_x          FLOAT NOT NULL,
        gyro_y          FLOAT NOT NULL,
        gyro_z          FLOAT NOT NULL,
        battery_pct     SMALLINT,
        is_valid        BOOLEAN DEFAULT TRUE,
        placement       sensor_placement
    );
    """)
    op.execute("SELECT create_hypertable('raw_imu_data', 'time', chunk_time_interval => INTERVAL '1 day')")
    
    op.execute("""
    ALTER TABLE raw_imu_data SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'session_id'
    );
    """)
    op.execute("SELECT add_compression_policy('raw_imu_data', INTERVAL '7 days')")
    op.execute("CREATE INDEX idx_raw_imu_session ON raw_imu_data(session_id, time DESC)")

    op.execute("""
    CREATE TABLE preprocessed_signals (
        time            TIMESTAMPTZ NOT NULL,
        session_id      UUID NOT NULL REFERENCES sessions(id),
        segment_index   INTEGER NOT NULL,
        acc_x           FLOAT[] NOT NULL,
        acc_y           FLOAT[] NOT NULL,
        acc_z           FLOAT[] NOT NULL,
        gyro_x          FLOAT[],
        gyro_y          FLOAT[],
        gyro_z          FLOAT[],
        samples_count   INTEGER NOT NULL,
        artifact_count  INTEGER DEFAULT 0,
        is_valid        BOOLEAN DEFAULT TRUE,
        window_size_sec FLOAT
    );
    """)
    op.execute("SELECT create_hypertable('preprocessed_signals', 'time', chunk_time_interval => INTERVAL '1 day')")
    op.execute("CREATE INDEX idx_preprocessed_session ON preprocessed_signals(session_id, time DESC)")
    op.execute("CREATE INDEX idx_preprocessed_segment ON preprocessed_signals(session_id, segment_index)")

def downgrade() -> None:
    op.drop_table('preprocessed_signals')
    op.drop_table('raw_imu_data')
