from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from uuid import UUID
from datetime import datetime, timezone
from typing import List

from app.core.database import get_db
from app.models.session import Session, SessionStatus
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate

router = APIRouter()

@router.post("/", response_model=SessionRead)
async def create_session(session_data: SessionCreate, db: AsyncSession = Depends(get_db)):
    new_session = Session(**session_data.model_dump())
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

@router.get("/{session_id}", response_model=SessionRead)
async def get_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.patch("/{session_id}/end", response_model=SessionRead)
async def end_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session.status = SessionStatus.COMPLETED
    session.ended_at = datetime.now(timezone.utc)
    
    await db.commit()
    await db.refresh(session)
    return session
