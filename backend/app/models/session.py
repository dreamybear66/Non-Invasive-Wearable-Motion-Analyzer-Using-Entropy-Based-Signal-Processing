from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timezone
import uuid
import enum
from app.core.database import Base

class SessionStatus(enum.Enum):
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    COMPLETED = 'COMPLETED'
    INTERRUPTED = 'INTERRUPTED'

class FatigueState(enum.Enum):
    NORMAL = 'NORMAL'
    EARLY_FATIGUE = 'EARLY_FATIGUE'
    MODERATE_FATIGUE = 'MODERATE_FATIGUE'
    HIGH_FATIGUE = 'HIGH_FATIGUE'

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athletes.id", ondelete="CASCADE"), nullable=False, index=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    
    session_name = Column(String(255))
    sport_activity = Column(String(100))
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ACTIVE, index=True)
    
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    ended_at = Column(DateTime(timezone=True))
    
    sampling_rate_hz = Column(Integer, default=100)
    window_size_sec = Column(Float, default=5.0)
    window_overlap = Column(Float, default=0.5)
    filter_cutoff_hz = Column(Float, default=20.0)
    
    peak_fis = Column(Float)
    mean_fis = Column(Float)
    peak_fatigue_state = Column(SQLEnum(FatigueState))
    baseline_apen = Column(Float)
    baseline_sampen = Column(Float)
    total_segments = Column(Integer, default=0)
    alert_count = Column(Integer, default=0)
    
    notes = Column(String)
    tags = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
