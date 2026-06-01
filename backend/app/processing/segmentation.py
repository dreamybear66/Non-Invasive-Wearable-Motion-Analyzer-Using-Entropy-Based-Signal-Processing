def segment_signal(signal: list, fs: float, window_sec: float, overlap: float) -> list:
    """
    Segments a 1D signal into fixed-length windows with given overlap.
    Returns a list of lists.
    
    :param signal: List of signal samples
    :param fs: Sampling rate in Hz
    :param window_sec: Window length in seconds
    :param overlap: Overlap fraction (0.0 to 1.0)
    """
    if not signal:
        return []
        
    window_samples = int(fs * window_sec)
    step_samples = int(window_samples * (1.0 - overlap))
    
    if window_samples <= 0 or step_samples <= 0:
        return [signal]
        
    segments = []
    n = len(signal)
    
    for i in range(0, n, step_samples):
        segment = signal[i:i + window_samples]
        
        # Discard partial segment at end if < 80% full
        if len(segment) < (0.8 * window_samples):
            break
            
        segments.append(segment)
        
    return segments
