from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
import enum
from app.core.database import Base

class SensorPlacement(enum.Enum):
    LOWER_BACK = 'LOWER_BACK'
    RIGHT_WRIST = 'RIGHT_WRIST'
    LEFT_WRIST = 'LEFT_WRIST'
    RIGHT_ANKLE = 'RIGHT_ANKLE'
    LEFT_ANKLE = 'LEFT_ANKLE'
    CHEST = 'CHEST'

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    firmware_version = Column(String(50))
    sensor_model = Column(String(100), default='MPU-6050')
    sampling_rate_hz = Column(Integer, default=100)
    battery_level = Column(Integer)
    last_seen_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AthleteSensor(Base):
    __tablename__ = "athlete_sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athletes.id", ondelete="CASCADE"), nullable=False, index=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    placement = Column(SQLEnum(SensorPlacement), nullable=False)
    paired_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    paired_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_current = Column(Boolean, default=True)
