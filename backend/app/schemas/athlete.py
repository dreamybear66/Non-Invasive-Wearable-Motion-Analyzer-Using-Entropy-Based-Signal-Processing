from pydantic import BaseModel, UUID4
from datetime import date, datetime
from typing import Optional, List

class AthleteBase(BaseModel):
    athlete_code: str
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    sport: Optional[str] = None
    position: Optional[str] = None
    gender: Optional[str] = None
    fatigue_threshold_early: Optional[float] = 20.0
    fatigue_threshold_moderate: Optional[float] = 40.0
    fatigue_threshold_high: Optional[float] = 65.0
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class AthleteCreate(AthleteBase):
    organization_id: UUID4

class AthleteRead(AthleteBase):
    id: UUID4
    organization_id: UUID4
    baseline_apen: Optional[float] = None
    baseline_sampen: Optional[float] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
