import numpy as np
from scipy.signal import butter, filtfilt

def apply_butterworth_filter(signal: list, cutoff: float, fs: float, order: int = 4) -> list:
    """
    Applies a zero-phase Butterworth low-pass filter.
    """
    if not signal:
        return []
    
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    
    if normal_cutoff >= 1.0 or normal_cutoff <= 0.0:
        return signal  # Cannot filter if cutoff is outside valid range
        
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered = filtfilt(b, a, signal)
    return filtered.tolist()

def z_score_normalize(signal: list) -> list:
    """
    Applies Z-score normalization (zero mean, unit variance).
    """
    if not signal:
        return []
        
    arr = np.array(signal)
    mean = np.mean(arr)
    std = np.std(arr)
    
    if std == 0:
        return np.zeros_like(arr).tolist()
        
    normalized = (arr - mean) / std
    return normalized.tolist()

def detect_artifacts(signal: list, threshold: float = 5.0) -> tuple:
    """
    Flags samples where absolute value exceeds threshold (usually applied on Z-score).
    Returns (cleaned_signal, artifact_count).
    Here, cleaned_signal will interpolate or clip artifacts. For simplicity, we clip.
    """
    if not signal:
        return [], 0
        
    arr = np.array(signal)
    artifacts = np.abs(arr) > threshold
    artifact_count = np.sum(artifacts)
    
    # Clip artifacts
    arr = np.clip(arr, -threshold, threshold)
    return arr.tolist(), int(artifact_count)
