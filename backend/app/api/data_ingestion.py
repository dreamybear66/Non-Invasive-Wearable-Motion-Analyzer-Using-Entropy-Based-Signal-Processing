from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime, timezone

from app.core.database import get_db
from app.schemas.session import RawDataBatch
from app.models.signal_data import RawIMUData

router = APIRouter()

@router.post("/{session_id}/raw-data")
async def ingest_raw_data(session_id: UUID, batch: RawDataBatch, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Ingest a batch of raw IMU data from the BLE Gateway or client"""
    
    # Store directly to TimescaleDB
    data_objects = []
    base_time = batch.timestamp
    
    # Simple interpolation of time across packet_ids (assuming 10ms per packet @ 100Hz)
    import datetime
    
    for idx, p in enumerate(batch.packets):
        time_offset = datetime.timedelta(milliseconds=idx * 10)
        packet_time = base_time + time_offset
        
        row = RawIMUData(
            time=packet_time,
            session_id=session_id,
            sensor_id=batch.sensor_id,
            packet_id=p.packet_id,
            acc_x=p.acc_x,
            acc_y=p.acc_y,
            acc_z=p.acc_z,
            gyro_x=p.gyro_x,
            gyro_y=p.gyro_y,
            gyro_z=p.gyro_z,
            battery_pct=p.battery_pct,
            is_valid=True
        )
        data_objects.append(row)
        
    db.add_all(data_objects)
    await db.commit()
    
    # TODO: Trigger preprocessing in background
    # background_tasks.add_task(trigger_preprocessing, session_id, batch_start, batch_end)
    
    return {"status": "success", "inserted": len(data_objects)}
