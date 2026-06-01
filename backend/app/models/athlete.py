from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Date, CHAR
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    athlete_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(200))
    date_of_birth = Column(Date)
    sport = Column(String(100))
    position = Column(String(100))
    gender = Column(CHAR(1))
    
    baseline_apen = Column(Float)
    baseline_sampen = Column(Float)
    fatigue_threshold_early = Column(Float, default=20.0)
    fatigue_threshold_moderate = Column(Float, default=40.0)
    fatigue_threshold_high = Column(Float, default=65.0)
    
    notes = Column(String)
    tags = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
