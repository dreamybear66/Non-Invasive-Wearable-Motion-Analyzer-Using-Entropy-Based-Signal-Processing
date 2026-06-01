"""Fatigue Index Score (FIS) calculation and state classification"""
# TODO Phase 4
from enum import Enum
class FatigueState(Enum):
    NORMAL = 1
    EARLY_FATIGUE = 2
    MODERATE_FATIGUE = 3
    HIGH_FATIGUE = 4

def compute_fatigue_index(entropy_data): pass
def classify_fatigue(fis_score: float): pass
