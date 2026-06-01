from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.database import get_db
from app.models.entropy_result import EntropyResult, FatigueEvent

router = APIRouter()

@router.get("/{session_id}/entropy")
async def get_entropy(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Fetch full entropy time series for a session"""
    query = select(EntropyResult).where(EntropyResult.session_id == session_id).order_by(EntropyResult.time)
    result = await db.execute(query)
    records = result.scalars().all()
    
    return [
        {
            "time": r.time,
            "segment_index": r.segment_index,
            "apen_combined": r.apen_combined,
            "sampen_combined": r.sampen_combined,
            "fatigue_index": r.fatigue_index,
            "fatigue_state": r.fatigue_state
        }
        for r in records
    ]

@router.get("/{session_id}/fatigue-index")
async def get_fis(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Fetch only Fatigue Index Score (FIS) over time"""
    query = select(EntropyResult).where(EntropyResult.session_id == session_id).order_by(EntropyResult.time)
    result = await db.execute(query)
    records = result.scalars().all()
    
    return [
        {
            "time": r.time,
            "fatigue_index": r.fatigue_index
        }
        for r in records
    ]

@router.get("/{session_id}/alerts")
async def get_alerts(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Fetch fatigue alert event log"""
    query = select(FatigueEvent).where(FatigueEvent.session_id == session_id).order_by(FatigueEvent.time.desc())
    result = await db.execute(query)
    records = result.scalars().all()
    
    return [
        {
            "id": str(r.id),
            "time": r.time,
            "event_type": r.event_type,
            "previous_state": r.previous_state,
            "new_state": r.new_state,
            "fatigue_index": r.fatigue_index,
            "severity": r.severity,
            "message": r.message
        }
        for r in records
    ]
