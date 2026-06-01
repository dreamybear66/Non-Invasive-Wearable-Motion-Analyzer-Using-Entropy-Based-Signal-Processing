from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, List
from app.models.session import SessionStatus, FatigueState

class SessionBase(BaseModel):
    session_name: Optional[str] = None
    sport_activity: Optional[str] = None
    sampling_rate_hz: Optional[int] = 100
    window_size_sec: Optional[float] = 5.0
    window_overlap: Optional[float] = 0.5
    filter_cutoff_hz: Optional[float] = 20.0
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class SessionCreate(SessionBase):
    athlete_id: UUID4
    organization_id: UUID4

class SessionUpdate(BaseModel):
    status: Optional[SessionStatus] = None
    ended_at: Optional[datetime] = None

class SessionRead(SessionBase):
    id: UUID4
    athlete_id: UUID4
    organization_id: UUID4
    status: SessionStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    peak_fis: Optional[float] = None
    mean_fis: Optional[float] = None
    peak_fatigue_state: Optional[FatigueState] = None
    baseline_apen: Optional[float] = None
    baseline_sampen: Optional[float] = None
    total_segments: int
    alert_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RawDataPacket(BaseModel):
    packet_id: int
    acc_x: float
    acc_y: float
    acc_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    battery_pct: Optional[int] = None

class RawDataBatch(BaseModel):
    sensor_id: UUID4
    timestamp: datetime
    packets: List[RawDataPacket]
