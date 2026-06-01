from sqlalchemy import Column, DateTime, Integer, Float, Boolean, ForeignKey, String, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.models.session import FatigueState
import uuid

class EntropyResult(Base):
    __tablename__ = "entropy_results"
    
    time = Column(DateTime(timezone=True), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), primary_key=True)
    segment_index = Column(Integer, nullable=False, primary_key=True)
    
    apen_x = Column(Float)
    apen_y = Column(Float)
    apen_z = Column(Float)
    apen_combined = Column(Float)
    
    sampen_x = Column(Float)
    sampen_y = Column(Float)
    sampen_z = Column(Float)
    sampen_combined = Column(Float)
    
    perm_entropy_x = Column(Float)
    perm_entropy_y = Column(Float)
    perm_entropy_z = Column(Float)
    
    fatigue_index = Column(Float, nullable=False)
    fatigue_state = Column(SQLEnum(FatigueState), nullable=False)
    
    m_param = Column(Integer, default=2)
    r_param = Column(Float)

class FatigueEvent(Base):
    __tablename__ = "fatigue_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time = Column(DateTime(timezone=True), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athletes.id"), nullable=False)
    
    event_type = Column(String(50), nullable=False)
    previous_state = Column(SQLEnum(FatigueState))
    new_state = Column(SQLEnum(FatigueState), nullable=False)
    
    fatigue_index = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text)
    segment_index = Column(Integer)
    
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    acknowledged_at = Column(DateTime(timezone=True))
    
    apen_at_event = Column(Float)
    sampen_at_event = Column(Float)
