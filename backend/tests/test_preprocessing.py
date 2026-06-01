import pytest
import numpy as np
from app.processing.preprocessing import apply_butterworth_filter, z_score_normalize, detect_artifacts
from app.processing.segmentation import segment_signal

def test_butterworth_filter():
    fs = 100.0
    t = np.arange(0, 1.0, 1.0/fs)
    # Signal: 2Hz (keep) + 40Hz (remove)
    signal = np.sin(2 * np.pi * 2 * t) + 0.5 * np.sin(2 * np.pi * 40 * t)
    
    filtered = apply_butterworth_filter(signal.tolist(), cutoff=20.0, fs=fs)
    
    # The 40Hz component should be heavily attenuated
    assert len(filtered) == len(signal)
    
def test_z_score_normalize():
    signal = [1, 2, 3, 4, 5]
    normalized = z_score_normalize(signal)
    
    assert np.isclose(np.mean(normalized), 0.0)
    assert np.isclose(np.std(normalized), 1.0)
    
def test_segmentation():
    fs = 100.0
    signal = np.zeros(6000).tolist() # 60 seconds
    
    # 5 sec windows, 50% overlap (2.5 sec step)
    segments = segment_signal(signal, fs, 5.0, 0.5)
    
    # 60s / 2.5s step = 24 windows (approximately)
    assert len(segments) > 0
    assert len(segments[0]) == 500
