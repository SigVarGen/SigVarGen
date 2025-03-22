import numpy as np

def generate_noise_power(wave, snr_range=(-20, 30)):
    """
    Generates noise power based on a randomly selected SNR within a given range.
    
    Parameters:
    ----------
    - wave : numpy.ndarray
        The input signal.
    - snr_range : tuple (int, int)
        The range of SNR values (in dB) to randomly select from.

    Returns:
    ----------
    - noise_power : float 
        Computed noise power (variance).
    - selected_snr_db : float 
        The randomly selected SNR (for reference).
    """
    
    # Compute the standard deviation of the input signal
    signal_std = np.std(wave)

    # Randomly select an SNR value from the given range
    selected_snr_db = np.random.uniform(*snr_range)  # Random SNR between min and max range

    # Convert SNR (dB) to linear noise fraction
    desired_noise_fraction = 10 ** (-selected_snr_db / 20)

    # Compute noise standard deviation (sigma_V) based on signal standard deviation
    sigma_V = signal_std * desired_noise_fraction

    # Compute noise power (variance)
    noise_power = sigma_V ** 2

    return noise_power, selected_snr_db

def harmonic_peaks(freqs, base_freq=100, num_harmonics=5, width=5):
    filter = np.zeros_like(freqs)
    for i in range(1, num_harmonics + 1):
        center = base_freq * i
        filter += np.exp(-((freqs - center) ** 2) / (2 * width**2))
    return filter

def add_colored_noise(wave, fs, noise_power, npw, mf, color='pink', mod_envelope=None):
    """
    Add colored noise (white, pink, or brown) to a signal.

    Parameters:
    ----------
    - wave : numpy.ndarray
        Original signal.
    - noise_power : float
        Base noise power level (variance).
    - npw : tuple (float, float)
        Tuple specifying the range over which to vary the noise power (relative to noise_power).
    - mf : tuple (float, float)
        Tuple specifying the modulation factor range to slightly vary the amplitude of the signal.
    - color : str or callable, optional
        Specifies the spectral profile of the noise to be added. Accepts:
        - Predefined strings:
            - 'white'  → flat spectrum
            - 'pink'   → power ∝ 1/f
            - 'brown'  → power ∝ 1/f^2
            - 'blue'   → power ∝ f
            - 'violet' → power ∝ f^2
        - A custom function: A callable that takes a frequency array and returns a filter of the same shape.
          For example, `lambda freqs: 1 / (freqs**0.8)` for a custom decay.
    - mod_envelope : Dictionary {'func': function, 'param': list}
        Dictionary selected from noise_funcs. 

    Returns:
    - res : numpy.ndarray
        The signal with added colored noise.
    """

    # Determine noise power within the specified range
    noise_pw = noise_power # * np.random.uniform(*npw)
    
    # Generate white noise
    white_noise = np.random.normal(0, 1, size=len(wave))
    
    # Generate colored noise
    d = 1/fs
    freqs = np.fft.rfftfreq(len(white_noise), d=d)
    freqs[0] = freqs[1] 
    
    if callable(color):
        # If color is a function, than apply it as a filter
        filter = color(freqs)
    elif color == 'pink':
        # Pink noise has a PSD proportional to 1/f
        filter = 1 / np.sqrt(freqs)
    elif color == 'brown':
        # Brown (red) noise has a PSD proportional to 1/f^2
        filter = 1 / freqs
    elif color == 'blue':
        # density proportional to f
        filter = np.sqrt(freqs)
    elif color == 'violet':
        # density proportional to f^2
        filter = freqs
    else:
        # White noise (no filtering)
        filter = np.ones_like(freqs)
    
    # Apply the filter to the noise spectrum
    noise_spectrum = np.fft.rfft(white_noise) * filter
    
    # Inverse FFT to get the time-domain noise signal
    noise = np.fft.irfft(noise_spectrum, n=len(white_noise))
    
    # Normalize the noise to zero mean
    noise = noise - np.mean(noise)
    
    # Compute the standard deviation
    noise_std = np.std(noise)
    
    # Prevent division by zero
    if noise_std == 0:
        noise_std = 1
    
    # Normalize to unit variance
    noise = noise / noise_std
    
    # Scale noise to have the desired RMS value
    noise_rms = np.sqrt(noise_pw)
    noise = noise * noise_rms
    
    # Combine the original wave with the noise and apply modulation factor

    # 3) Apply time-varying amplitude envelope
    if mod_envelope is None:
        pass
    else:
        func = mod_envelope['func']
        pm = np.random.uniform(mod_envelope['param'][0], mod_envelope['param'][1])
        amp = (min(wave), max(wave))
        env = func(num_samples=len(wave), npw=amp, param=pm)
        noise = noise * env # Ensure the envelope is the same length

    modulation_factor = np.random.uniform(*mf)
    res = (wave * modulation_factor) + noise

    return res, noise