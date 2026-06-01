"""create audit refresh tokens

Revision ID: 008
Revises: 007
Create Date: 2026-06-01 10:07:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('session_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('generated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('format', postgresql.ENUM('PDF', 'CSV', 'JSON', name='report_format', create_type=False), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='PENDING', nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), server_default=sa.text("NOW() + INTERVAL '30 days'"), nullable=True),
        sa.ForeignKeyConstraint(['generated_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_reports_session', 'session_reports', ['session_id'])

    op.create_table('refresh_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_revoked', sa.Boolean(), server_default='false', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash')
    )
    op.create_index('idx_tokens_user', 'refresh_tokens', ['user_id'])
    op.create_index('idx_tokens_hash', 'refresh_tokens', ['token_hash'])

    op.execute("""
    CREATE TABLE audit_log (
        id          BIGSERIAL,
        time        TIMESTAMPTZ DEFAULT NOW(),
        user_id     UUID REFERENCES users(id),
        action      VARCHAR(100) NOT NULL,
        resource    VARCHAR(100),
        resource_id UUID,
        ip_address  INET,
        user_agent  TEXT,
        old_values  JSONB,
        new_values  JSONB,
        PRIMARY KEY (id, time)
    );
    """)
    op.execute("SELECT create_hypertable('audit_log', 'time', chunk_time_interval => INTERVAL '30 days')")
    op.execute("CREATE INDEX idx_audit_user ON audit_log(user_id, time DESC)")
    op.execute("CREATE INDEX idx_audit_resource ON audit_log(resource, resource_id)")
    
    op.execute("SELECT add_retention_policy('raw_imu_data', INTERVAL '90 days')")
    op.execute("SELECT add_retention_policy('preprocessed_signals', INTERVAL '90 days')")

def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('refresh_tokens')
    op.drop_table('session_reports')
