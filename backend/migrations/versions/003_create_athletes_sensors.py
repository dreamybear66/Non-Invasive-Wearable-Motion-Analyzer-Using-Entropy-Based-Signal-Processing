"""create athletes sensors

Revision ID: 003
Revises: 002
Create Date: 2026-06-01 10:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('athletes',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('athlete_code', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('sport', sa.String(length=100), nullable=True),
        sa.Column('position', sa.String(length=100), nullable=True),
        sa.Column('gender', sa.CHAR(length=1), nullable=True),
        sa.Column('baseline_apen', sa.Float(), nullable=True),
        sa.Column('baseline_sampen', sa.Float(), nullable=True),
        sa.Column('fatigue_threshold_early', sa.Float(), server_default='20.0', nullable=True),
        sa.Column('fatigue_threshold_moderate', sa.Float(), server_default='40.0', nullable=True),
        sa.Column('fatigue_threshold_high', sa.Float(), server_default='65.0', nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('athlete_code')
    )
    op.create_index('idx_athletes_org', 'athletes', ['organization_id'])
    op.create_index('idx_athletes_code', 'athletes', ['athlete_code'])

    op.create_table('sensors',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('device_id', sa.String(length=100), nullable=False),
        sa.Column('firmware_version', sa.String(length=50), nullable=True),
        sa.Column('sensor_model', sa.String(length=100), server_default='MPU-6050', nullable=True),
        sa.Column('sampling_rate_hz', sa.Integer(), server_default='100', nullable=True),
        sa.Column('battery_level', sa.Integer(), nullable=True),
        sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('device_id')
    )
    op.create_index('idx_sensors_device', 'sensors', ['device_id'])

    op.create_table('athlete_sensors',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('athlete_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sensor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('placement', postgresql.ENUM('LOWER_BACK', 'RIGHT_WRIST', 'LEFT_WRIST', 'RIGHT_ANKLE', 'LEFT_ANKLE', 'CHEST', name='sensor_placement', create_type=False), nullable=False),
        sa.Column('paired_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('paired_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_current', sa.Boolean(), server_default='true', nullable=True),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['paired_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sensor_id', 'is_current')
    )
    op.create_index('idx_athlete_sensors_athlete', 'athlete_sensors', ['athlete_id'])

def downgrade() -> None:
    op.drop_table('athlete_sensors')
    op.drop_table('sensors')
    op.drop_table('athletes')
