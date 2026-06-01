from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime, timezone
import numpy as np

from app.core.database import get_db
from app.models.signal_data import RawIMUData, PreprocessedSignal
from app.models.session import Session
from app.processing.preprocessing import apply_butterworth_filter, z_score_normalize, detect_artifacts
from app.processing.segmentation import segment_signal

router = APIRouter()

async def process_session_data(session_id: UUID, db: AsyncSession):
    """
    Pulls raw data, filters, normalizes, segments, and stores it.
    """
    # 1. Fetch raw data
    query = select(RawIMUData).where(RawIMUData.session_id == session_id).order_by(RawIMUData.time)
    result = await db.execute(query)
    raw_data = result.scalars().all()
    
    if not raw_data:
        return
        
    # 2. Extract arrays
    acc_x = [d.acc_x for d in raw_data]
    acc_y = [d.acc_y for d in raw_data]
    acc_z = [d.acc_z for d in raw_data]
    times = [d.time for d in raw_data]
    
    # Session configs (defaults for now)
    fs = 100.0
    cutoff = 20.0
    window_sec = 5.0
    overlap = 0.5
    
    # 3. Preprocessing
    def process_axis(data):
        filtered = apply_butterworth_filter(data, cutoff, fs)
        normalized = z_score_normalize(filtered)
        cleaned, artifact_count = detect_artifacts(normalized)
        segments = segment_signal(cleaned, fs, window_sec, overlap)
        return segments, artifact_count

    segments_x, art_x = process_axis(acc_x)
    segments_y, art_y = process_axis(acc_y)
    segments_z, art_z = process_axis(acc_z)
    
    num_segments = min(len(segments_x), len(segments_y), len(segments_z))
    
    # 4. Store preprocessed segments
    preprocessed_objects = []
    for i in range(num_segments):
        # Calculate start time of segment
        # Index of start = i * step_samples = i * (fs * window_sec * (1-overlap))
        start_idx = int(i * (fs * window_sec * (1.0 - overlap)))
        if start_idx < len(times):
            seg_time = times[start_idx]
        else:
            seg_time = datetime.now(timezone.utc)
            
        is_valid = True
        total_artifacts = art_x + art_y + art_z
        # Simplistic validity check
        if total_artifacts > (fs * window_sec * 0.15): # 15% artifacts across axes
            is_valid = False
            
        obj = PreprocessedSignal(
            time=seg_time,
            session_id=session_id,
            segment_index=i,
            acc_x=segments_x[i],
            acc_y=segments_y[i],
            acc_z=segments_z[i],
            samples_count=len(segments_x[i]),
            artifact_count=total_artifacts,
            is_valid=is_valid,
            window_size_sec=window_sec
        )
        preprocessed_objects.append(obj)
        
    db.add_all(preprocessed_objects)
    
    # Update session
    session_res = await db.execute(select(Session).where(Session.id == session_id))
    session = session_res.scalars().first()
    if session:
        session.total_segments = num_segments
        
    await db.commit()

@router.post("/{session_id}/process")
async def trigger_preprocessing(session_id: UUID, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Triggers the async preprocessing pipeline"""
    # Check if session exists
    res = await db.execute(select(Session).where(Session.id == session_id))
    if not res.scalars().first():
        raise HTTPException(status_code=404, detail="Session not found")
        
    background_tasks.add_task(process_session_data, session_id, db)
    return {"status": "processing triggered"}

@router.get("/{session_id}/signals")
async def get_signals(session_id: UUID, db: AsyncSession = Depends(get_db)):
    """Fetch preprocessed segments"""
    query = select(PreprocessedSignal).where(PreprocessedSignal.session_id == session_id).order_by(PreprocessedSignal.segment_index)
    result = await db.execute(query)
    signals = result.scalars().all()
    
    return [
        {
            "segment_index": s.segment_index,
            "time": s.time,
            "samples_count": s.samples_count,
            "is_valid": s.is_valid
        }
        for s in signals
    ]
