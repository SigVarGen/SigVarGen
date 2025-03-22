import numpy as np

from SigVarGen.utils import interpoling

def generate_signal(t, n_sinusoids, amplitude_range, frequency_range, amp_md_min=0.05, amp_md_max=0.95):
    
    """
    Generate a composite signal made up of multiple sinusoids.

    This function creates a time-domain signal by summing `n_sinusoids` individual sine waves. 
    Each sinusoid has a randomly assigned amplitude, frequency, and phase, ensuring a diverse 
    and realistic composite waveform.

    Parameters:
    ----------
    t : numpy.ndarray
        A time vector representing the sample points.
    n_sinusoids : int
        The number of sin waves the generated signal will be consist of.
    amplitude_range : tuple (float, float)
        The minimum and maximum amplitude values for the individual sine waves.
    frequency_range : tuple (float, float)
        The minimum and maximum frequency values (in Hz) for the sine waves.
    amp_md_min : float, optional
        A minimum amplitude modifier (as a fraction of amplitude_range[0]) to avoid overly small values. 
        Default is 0.05.
    amp_md_max : float, optional
        A maximum amplitude modifier (as a fraction of amplitude_range[1]) to limit the upper amplitude 
        used during sinusoid generation. Default is 0.95.

    Returns:
    -------
    signal : numpy.ndarray
        The generated composite signal consisting of multiple summed sinusoids.
    sinusoids_params : list of dict
        A list containing dictionaries, each describing the parameters (`amp`, `freq`, `phase`) 
        of an individual sinusoid used to construct the final signal.

    Example:
    -------
    >>> import numpy as np
    >>> t = np.linspace(0, 1, 1000)  # 1000 samples
    >>> signal, params = generate_signal(t, n_sinusoids=5, amplitude_range=(0.1, 1.0), frequency_range=(5, 50))
    >>> print(params)  # View sinusoid parameters

    Notes:
    ------
    - The phase of each sinusoid is randomly initialized between 0 and 2π.
    - The generated signal is non-periodic.
    """

    signal = np.zeros_like(t)
    sinusoids_params = []

    # Generate and sum sinusoids
    for _ in range(n_sinusoids):
        amp = np.random.uniform(amplitude_range[0], amp_md_max*amplitude_range[1])
        freq = np.random.uniform(*frequency_range)
        phase = np.random.uniform(0, 2 * np.pi)
        sinusoid = amp * np.sin(2 * np.pi * freq * t + phase)
        signal += sinusoid
        sinusoids_params.append({'amp': amp, 'freq': freq, 'phase': phase})

    # Normalize signal to range [-1, 1]
    signal -= np.mean(signal)  # Remove DC offset
    max_abs_value = np.max(np.abs(signal))

    if max_abs_value == 0:
        raise ValueError("Generated signal has zero amplitude. Check input parameters.")
    
    signal /= max_abs_value  # Normalize to [-1, 1]

    # Rescale signal to be within the exact amplitude range [A_min, A_max]
    A_min = max(amplitude_range[0], amp_md_min*amplitude_range[0])
    A_max = min(amplitude_range[1], amp_md_max*amplitude_range[1])
    signal = ((signal + 1) / 2) * (A_max - A_min) + A_min

    return signal, sinusoids_params