from app.processing.fatigue_index import FatigueState
from datetime import datetime, timezone, timedelta
import uuid

class AlertSeverity(str):
    INFO = 'INFO'
    WARNING = 'WARNING'
    DANGER = 'DANGER'

def generate_alert(session_id: uuid.UUID, athlete_id: uuid.UUID, previous_state: FatigueState, new_state: FatigueState, fis: float):
    """
    State change detector. Generates an alert dict if transitioning to a higher fatigue state.
    """
    state_levels = {
        FatigueState.NORMAL: 0,
        FatigueState.EARLY_FATIGUE: 1,
        FatigueState.MODERATE_FATIGUE: 2,
        FatigueState.HIGH_FATIGUE: 3
    }
    
    prev_lvl = state_levels.get(previous_state, 0)
    new_lvl = state_levels.get(new_state, 0)
    
    if new_lvl > prev_lvl and new_lvl > 0:
        severity = AlertSeverity.INFO
        if new_state == FatigueState.MODERATE_FATIGUE:
            severity = AlertSeverity.WARNING
        elif new_state == FatigueState.HIGH_FATIGUE:
            severity = AlertSeverity.DANGER
            
        return {
            "session_id": session_id,
            "athlete_id": athlete_id,
            "event_type": "STATE_CHANGE",
            "previous_state": previous_state.value if previous_state else None,
            "new_state": new_state.value,
            "fatigue_index": fis,
            "severity": severity,
            "message": f"Athlete entered {new_state.value} (FIS: {fis:.1f})"
        }
    return None
