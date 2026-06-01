from sqlalchemy import Column, DateTime, Integer, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timezone
from app.core.database import Base
from app.models.sensor import SensorPlacement

class RawIMUData(Base):
    __tablename__ = "raw_imu_data"
    
    time = Column(DateTime(timezone=True), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), primary_key=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id"))
    packet_id = Column(Integer, nullable=False, primary_key=True)
    
    acc_x = Column(Float, nullable=False)
    acc_y = Column(Float, nullable=False)
    acc_z = Column(Float, nullable=False)
    gyro_x = Column(Float, nullable=False)
    gyro_y = Column(Float, nullable=False)
    gyro_z = Column(Float, nullable=False)
    
    battery_pct = Column(Integer)
    is_valid = Column(Boolean, default=True)
    placement = Column(SQLEnum(SensorPlacement))

class PreprocessedSignal(Base):
    __tablename__ = "preprocessed_signals"
    
    time = Column(DateTime(timezone=True), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), primary_key=True)
    segment_index = Column(Integer, nullable=False, primary_key=True)
    
    acc_x = Column(ARRAY(Float), nullable=False)
    acc_y = Column(ARRAY(Float), nullable=False)
    acc_z = Column(ARRAY(Float), nullable=False)
    gyro_x = Column(ARRAY(Float))
    gyro_y = Column(ARRAY(Float))
    gyro_z = Column(ARRAY(Float))
    
    samples_count = Column(Integer, nullable=False)
    artifact_count = Column(Integer, default=0)
    is_valid = Column(Boolean, default=True)
    window_size_sec = Column(Float)
