import numpy as np

from SigVarGen.signal.signal_generation import generate_signal

def apply_time_shift(wave, max_shift):
    """
    Apply a random time shift to the signal.

    This function shifts the waveform by a random number of samples within the range [-max_shift, max_shift].

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform to be shifted.
    max_shift : int
        Maximum number of samples to shift in either direction.

    Returns:
    -------
    numpy.ndarray
        The time-shifted waveform.

    Example:
    -------
    >>> shifted_wave = apply_time_shift(wave, max_shift=50)
    """
    shift = np.random.randint(-max_shift, max_shift)  # Random shift value
    shifted_wave = np.roll(wave, shift)  # Circularly shift the wave
    return shifted_wave


def apply_time_warp(wave, max_warp_factor, t, n_sinusoids, amplitude_range, base_frequency_range):
    """
    Apply time warping to the signal by modifying the time scale.

    The function compresses or expands the time axis and fills any missing parts 
    by generating a new signal segment.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform to be warped.
    max_warp_factor : float
        Maximum factor by which time can be warped (values close to 1 result in minimal warping).
    t : numpy.ndarray
        Time vector.
    n_sinusoids : int
        Number of sinusoids used in the generated replacement signal.
    amplitude_range : tuple (float, float)
        The amplitude range for the generated signal.
    base_frequency_range : tuple (float, float)
        The frequency range for the generated signal.

    Returns:
    -------
    numpy.ndarray
        The time-warped waveform.

    Example:
    -------
    >>> warped_wave = apply_time_warp(wave, 0.1, t, 5, (0.1, 1.0), (10, 100))
    """
    warp_factor = np.random.uniform(1 - max_warp_factor, 1 + max_warp_factor)
    t_original = np.arange(len(wave))
    t_warped = t_original * warp_factor  # Scale the time axis
    warped_wave = np.interp(t_original, t_warped, wave)  # Interpolate

    # Handle any missing values at the end by generating new samples
    num = len(wave) - t_warped[-1]
    if int(num) > 0:
        generated_wave, _ = generate_signal(t, n_sinusoids, amplitude_range, base_frequency_range)
        warped_wave[-int(num):] = generated_wave[:int(num)]

    return warped_wave


def apply_gain_variation(wave, max_gain_variation):
    """
    Apply a random gain variation to the signal.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    max_gain_variation : float
        Maximum gain variation factor.

    Returns:
    -------
    numpy.ndarray
        The gain-modified waveform.

    Example:
    -------
    >>> modified_wave = apply_gain_variation(wave, max_gain_variation=0.2)
    """
    gain = np.random.uniform(1 - max_gain_variation, 1 + max_gain_variation)  # Random gain factor
    return wave * gain


def apply_amplitude_modulation(wave, modulation_depth):
    """
    Apply amplitude modulation to the signal.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    modulation_depth : float
        Depth of modulation.

    Returns:
    -------
    numpy.ndarray
        The amplitude-modulated waveform.

    Example:
    -------
    >>> modulated_wave = apply_amplitude_modulation(wave, 0.5)
    """
    modulation = 1 + modulation_depth * np.sin(2 * np.pi * np.random.uniform(0.1, 1.0) * np.linspace(0, 1, len(wave)))
    return wave * modulation


def apply_baseline_drift(wave, max_drift, reversed=False):
    """
    Apply a linear baseline drift to the waveform.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    max_drift : float
        Maximum drift in amplitude.
    reversed : bool, optional
        If True, drift starts at `max_drift` and decreases to zero (default: False).

    Returns:
    -------
    numpy.ndarray
        The waveform with baseline drift applied.

    Example:
    -------
    >>> drifted_wave = apply_baseline_drift(wave, 0.1, reversed=True)
    """
    if not reversed:
        drift = np.linspace(0, np.random.uniform(-max_drift, max_drift), len(wave))
    else:
        final_value = np.random.uniform(-max_drift, max_drift)
        drift = np.linspace(final_value, 0, len(wave))
    return wave + drift


def apply_amplitude_modulation_region(wave, modulation_depth=0.5, f_min=0.1, f_max=1.0):
    """
    Apply amplitude modulation to a specific region of the signal.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    modulation_depth : float, optional
        Depth of modulation (default: 0.5).
    f_min : float, optional
        Start fraction of signal where modulation begins (default: 0.1).
    f_max : float, optional
        End fraction of signal where modulation stops (default: 1.0).

    Returns:
    -------
    numpy.ndarray
        The waveform with localized amplitude modulation.

    Example:
    -------
    >>> modulated_wave = apply_amplitude_modulation_region(wave, 0.3, 0.2, 0.8)
    """
    t = np.linspace(0, 1, len(wave))
    modulation = np.ones(len(wave))
    start_idx = int(f_min * len(wave))
    end_idx = int(f_max * len(wave))

    modulation[start_idx:end_idx] = 1 + modulation_depth * np.sin(2 * np.pi * np.random.uniform(0.1, 1.0) * t[start_idx:end_idx])
    
    return wave * modulation


def transform_wave_with_score(original_wave, score, t, n_sinusoids, amplitude_range, base_frequency_range, interrupt_params):
    """
    Apply transformations to a wave based on a given score.

    Parameters:
    ----------
    original_wave : numpy.ndarray
        The original input waveform.
    score : float
        Scaling factor determining how much of the waveform to transform.
    t : numpy.ndarray
        Time vector.
    n_sinusoids : int
        Number of sinusoids in the generated signal.
    amplitude_range : tuple
        Amplitude range for the generated replacement signal.
    base_frequency_range : tuple
        Frequency range for the generated replacement signal.
    interrupt_params : list of dict
        List of dictionaries containing details about the interrupt locations.

    Returns:
    -------
    numpy.ndarray
        The transformed waveform.
    
    Example:
    -------
    >>> transformed_wave = transform_wave_with_score(wave, 0.5, t, n_sinusoids=10, 
                            amplitude_range=(0,1), base_frequency_range=(70, 75), 
                            interrupt_params=None)
    """
    generated_wave, _ = generate_signal(t, n_sinusoids, amplitude_range, base_frequency_range)

    N = len(original_wave)
    transformed_wave = original_wave.copy()

    num_segments = int(score * 5)
    segment_length = max(1, int(N * score * 0.2))

    interrupt_start = interrupt_params[0]['start_idx']
    interrupt_end = interrupt_start + interrupt_params[0]['duration_idx']

    for _ in range(num_segments):
        for attempt in range(10):
            start_idx = np.random.randint(0, N - segment_length)
            if start_idx + segment_length <= interrupt_start or start_idx >= interrupt_end:
                transformed_wave[start_idx:start_idx + segment_length] = generated_wave[start_idx:start_idx + segment_length]
                break

    return transformed_wave


def apply_nonlinear_distortion(wave, distortion_level):
    """
    Apply nonlinear distortion using a tanh-based transformation.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    distortion_level : float
        Strength of the distortion.

    Returns:
    -------
    numpy.ndarray
        The distorted waveform.
    """
    return np.tanh(distortion_level * wave)


def apply_quantization_noise(wave, num_bits):
    """
    Simulate the effect of quantization noise in a digitized signal.

    Parameters:
    ----------
    wave : numpy.ndarray
        The input waveform.
    num_bits : int
        Number of bits for quantization (lower bits = more noise).

    Returns:
    -------
    numpy.ndarray
        The quantized waveform.
    """
    max_amplitude = np.max(np.abs(wave))
    quantization_levels = 2 ** num_bits
    return np.round(wave / max_amplitude * (quantization_levels / 2)) * (max_amplitude / (quantization_levels / 2))
