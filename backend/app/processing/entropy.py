import numpy as np
import antropy as ant

def compute_apen(signal: list, m: int = 2, r_multiplier: float = 0.2) -> float:
    if not signal:
        return 0.0
    arr = np.array(signal)
    r = r_multiplier * np.std(arr)
    # antropy app_entropy
    return float(ant.app_entropy(arr, order=m, metric='chebyshev'))

def compute_sampen(signal: list, m: int = 2, r_multiplier: float = 0.2) -> float:
    if not signal:
        return 0.0
    arr = np.array(signal)
    r = r_multiplier * np.std(arr)
    return float(ant.sample_entropy(arr, order=m, metric='chebyshev'))

def compute_perm_entropy(signal: list, order: int = 3) -> float:
    if not signal:
        return 0.0
    arr = np.array(signal)
    return float(ant.perm_entropy(arr, order=order, normalize=True))

def compute_entropy_batch(segments: list, m: int = 2, r_multiplier: float = 0.2) -> list:
    """Processes a list of segments and returns their entropy metrics"""
    results = []
    for seg in segments:
        results.append({
            "apen": compute_apen(seg, m, r_multiplier),
            "sampen": compute_sampen(seg, m, r_multiplier),
            "perm": compute_perm_entropy(seg)
        })
    return results
