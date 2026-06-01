"""create enums

Revision ID: 001
Revises: 
Create Date: 2026-06-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("CREATE TYPE fatigue_state AS ENUM ('NORMAL', 'EARLY_FATIGUE', 'MODERATE_FATIGUE', 'HIGH_FATIGUE')")
    op.execute("CREATE TYPE sensor_placement AS ENUM ('LOWER_BACK', 'RIGHT_WRIST', 'LEFT_WRIST', 'RIGHT_ANKLE', 'LEFT_ANKLE', 'CHEST')")
    op.execute("CREATE TYPE session_status AS ENUM ('ACTIVE', 'PAUSED', 'COMPLETED', 'INTERRUPTED')")
    op.execute("CREATE TYPE user_role AS ENUM ('ADMIN', 'COACH', 'ATHLETE', 'PHYSIOTHERAPIST')")
    op.execute("CREATE TYPE alert_severity AS ENUM ('INFO', 'WARNING', 'DANGER')")
    op.execute("CREATE TYPE report_format AS ENUM ('PDF', 'CSV', 'JSON')")

def downgrade() -> None:
    op.execute("DROP TYPE report_format")
    op.execute("DROP TYPE alert_severity")
    op.execute("DROP TYPE user_role")
    op.execute("DROP TYPE session_status")
    op.execute("DROP TYPE sensor_placement")
    op.execute("DROP TYPE fatigue_state")
