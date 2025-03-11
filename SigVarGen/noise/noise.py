import numpy as np

def get_conversion_factor(max_amp, threshold=0.1):
    """
    Determines the unit conversion based on the device's maximum amplitude.
    """
    if max_amp < threshold:
        return 1e6, "µV"  # Use microvolts for low amplitude devices
    else:
        return 1e3, "mV"  # Otherwise, use millivolts

def dynamic_noise_fraction(interrupt_range, domain, base_fraction=0.01, low_amp_threshold=0.1, k=8):
    """
    Computes a dynamic noise fraction using an exponential decay.
    
    For devices with max_amp below low_amp_threshold, the noise fraction is:
      noise_fraction = base_fraction * exp(-k * (low_amp_threshold - max_amp) / low_amp_threshold)
      
    The parameter 'k' controls how aggressively the fraction decays.
    """
    min_amp, max_amp = interrupt_range[domain]['amplitude']
    if max_amp < low_amp_threshold:
        scale = np.exp(-k * (low_amp_threshold - max_amp) / low_amp_threshold)
        return base_fraction * scale
    else:
        return base_fraction

def get_noise_params(interrupt_range, domain, noise_fraction=None, steps=10):
    """
    Computes noise level parameters using a dynamic noise fraction.
    
    Unlike before, this version does not force a minimum noise range
    and instead works in continuous (floating-point) space.
    
    Returns:
      - start_val: starting value of the noise range
      - stop_val: end value of the noise range
      - step_val: increment for the noise levels
      - unit: unit for the noise (mV/µV)
      - noise_fraction: the computed (or provided) noise fraction
    """
    if noise_fraction is None:
        noise_fraction = dynamic_noise_fraction(interrupt_range, domain)
    
    min_amp, max_amp = interrupt_range[domain]['amplitude']
    conv_factor, unit = get_conversion_factor(max_amp)
    
    # Convert amplitudes without forcing a minimum of 1.
    min_val = min_amp * conv_factor
    max_val = max_amp * conv_factor

    # Compute noise_range as a continuous value.
    noise_range = (max_val - min_val) * noise_fraction

    # Compute step size as a fraction of the noise_range.
    step_val = noise_range / steps if noise_range != 0 else 0

    # Use the midpoint of the noise range for starting point.
    start_val = min_val + noise_range / 2

    return start_val, start_val + noise_range, step_val, unit, noise_fraction

def calculate_noise_power(start_value, stop_value, step_value, unit="mV", noise_fraction=0.01):
    """
    Calculates noise power based on the noise level range and the provided noise fraction.
    
    Returns a list of tuples with:
      (noise level in unit, sigma in V, noise power (variance))
    """
    conversion_factors = {"mV": 1e3, "µV": 1e6}
    conv_factor = conversion_factors[unit]
    
    noise_levels = []
    val = start_value
    while val <= stop_value:
        sigma_V = (val / conv_factor) * noise_fraction
        noise_power = sigma_V ** 2
        noise_levels.append((val, sigma_V, noise_power))
        val += step_value

    return noise_levels


def add_colored_noise(wave, noise_power, npw, mf, color='pink', mod_envelope=None):
    """
    Add colored noise (white, pink, or brown) to a signal.

    Parameters:
    - wave: Original signal (numpy array).
    - noise_power: Base noise power level (variance).
    - npw: Tuple specifying the range over which to vary the noise power (relative to noise_power).
    - mf: Tuple specifying the modulation factor range to slightly vary the amplitude of the signal.
    - color: Type of noise to add ('white', 'pink', 'brown'). Default is 'pink'.
    - mod_envelope: Dictionary {'func': envelope_sine, 'param': [0.0001, 0.01]}

    Returns:
    - res: The signal with added colored noise.
    """

    # Determine noise power within the specified range
    noise_pw = np.sqrt(noise_power) #np.sqrt ???  # * np.random.uniform(*npw)
    
    # Generate white noise
    white_noise = np.random.normal(0, 1, size=len(wave))
    
    # Generate colored noise
    freqs = np.fft.rfftfreq(len(white_noise), d=1.0)
    freqs[0] = freqs[1] 
    
    if color == 'pink':
        # Pink noise has a PSD proportional to 1/f
        filter = 1 / np.sqrt(freqs)
    elif color == 'brown':
        # Brown noise has a PSD proportional to 1/f^2
        filter = 1 / freqs
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
        env = func(num_samples=len(wave), npw=npw, param=pm)
        noise = noise * env # Ensure the envelope is the same length

    modulation_factor = np.random.uniform(*mf)
    res = (wave * modulation_factor) + noise

    return res