import enum

class FatigueState(str, enum.Enum):
    NORMAL = 'NORMAL'
    EARLY_FATIGUE = 'EARLY_FATIGUE'
    MODERATE_FATIGUE = 'MODERATE_FATIGUE'
    HIGH_FATIGUE = 'HIGH_FATIGUE'

def compute_fatigue_index(current_entropy: float, baseline_entropy: float) -> float:
    """
    Computes a Fatigue Index Score (FIS) from 0 to 100.
    FIS is based on the relative drop in entropy (as entropy drops, fatigue increases).
    """
    if baseline_entropy == 0:
        return 0.0
        
    delta = baseline_entropy - current_entropy
    if delta <= 0:
        return 0.0 # No fatigue (entropy is higher than baseline)
        
    # Scale: A 50% drop in entropy equals 100 FIS
    # Formular: (delta / baseline_entropy) * 200 -> caps at 100
    fis = (delta / baseline_entropy) * 200.0
    return min(100.0, max(0.0, fis))

def classify_fatigue(fis: float, t_early: float = 20.0, t_mod: float = 40.0, t_high: float = 65.0) -> FatigueState:
    if fis >= t_high:
        return FatigueState.HIGH_FATIGUE
    elif fis >= t_mod:
        return FatigueState.MODERATE_FATIGUE
    elif fis >= t_early:
        return FatigueState.EARLY_FATIGUE
    else:
        return FatigueState.NORMAL
