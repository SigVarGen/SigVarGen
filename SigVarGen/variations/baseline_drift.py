import numpy as np

def apply_baseline_drift_region(wave, max_drift, start_frac=0.3, end_frac=0.7):
    drift = np.zeros(len(wave))
    start_idx = int(start_frac * len(wave))
    end_idx = int(end_frac * len(wave))
    
    # Only in [start_idx:end_idx], we introduce a linear drift
    final_value = np.random.uniform(-max_drift, max_drift)
    drift[start_idx:end_idx] = np.linspace(0, final_value, end_idx - start_idx)
    
    return wave + drift

def apply_baseline_drift_polynomial(wave, max_drift, reversed=False, order=2):
    N = len(wave)
    x = np.linspace(0, 1, N)
    final_value = np.random.uniform(-max_drift, max_drift)
    
    if not reversed:
        # e.g., for order=2, drift ~ final_value * x^2
        drift = final_value * (x ** order)
    else:
        # e.g., for order=2, reversed drift ~ final_value * (1 - x^2)
        drift = final_value * (1 - x ** order)
    
    return wave + drift

def apply_baseline_drift_piecewise(wave, max_drift, reversed=False, num_pieces=3):
    N = len(wave)
    drift = np.zeros(N)
    
    # Break the wave into segments
    segment_length = N // num_pieces
    
    # Random final values for each piece
    piece_values = np.random.uniform(-max_drift, max_drift, num_pieces)
    
    if reversed:
        # If reversed, we can reverse the order of final piece values
        piece_values = piece_values[::-1]
    
    for i in range(num_pieces):
        start_idx = i * segment_length
        end_idx = (i + 1) * segment_length if (i < num_pieces - 1) else N
        
        # Linear ramp in each piece, from the end value of the previous piece to the new piece_values[i]
        if i == 0:
            start_value = 0.0 if not reversed else piece_values[0]
        else:
            start_value = piece_values[i - 1]
        
        end_value = piece_values[i]
        
        length = end_idx - start_idx
        drift[start_idx:end_idx] = np.linspace(start_value, end_value, length)
    
    return wave + drift

def apply_baseline_drift_quadratic(wave, max_drift, reversed=False):

    # 1. Create a time vector from 0 to 1 for the length of the wave
    N = len(wave)
    t = np.linspace(0, 1, N)

    # 2. Pick a final drift value randomly within [-max_drift, max_drift]
    final_value = np.random.uniform(-max_drift, max_drift)

    # 3. Construct a quadratic drift:
    #    - If not reversed: drift(0) = 0, drift(1) = final_value
    #      a simple form is final_value * t^2
    #    - If reversed: drift(0) = final_value, drift(1) = 0
    #      a simple form is final_value * (1 - t)^2
    if not reversed:
        drift = final_value * (t**2)
    else:
        drift = final_value * ((1 - t)**2)

    # 4. Add the drift to the original wave
    return wave + drift

def apply_baseline_drift_middle_peak(wave, max_drift, direction='down', min_drift=0):
    """
    Applies a baseline drift to the wave that is stable (zero) at both ends
    and peaks in the middle.

    Parameters
    ----------
    wave : np.array
        The original 1D signal.
    max_drift : float
        The maximum absolute amplitude of the drift in the middle.

    Returns
    -------
    np.array
        The wave with a pronounced (positive or negative) drift peak at t=0.5
        and stable baseline at t=0 and t=1.
    """

    N = len(wave)
    if N == 0:
        return wave  # Edge case: empty wave

    # Create a time vector from 0 to 1
    t = np.linspace(0.0, 1.0, N)

    # Pick a final drift value randomly in [-max_drift, max_drift]
    final_value = np.random.uniform(0+min_drift, max_drift)

    if direction=='down':
        final_value=-final_value

    # Parabola with a peak at t=0.5 and zeros at t=0 and t=1
    # Maximum is final_value at t=0.5
    drift = final_value * 4 * t * (1 - t)

    return wave + drift