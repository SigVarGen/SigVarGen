import numpy as np

def calculate_noise_power(start_mV, stop_mV, step_mV):
    """
    Function to calculate noise power (σ²)
    """
    data = []
    for mV in range(start_mV, stop_mV + step_mV, step_mV):
        sigma_V = mV / 1000  # Convert mV to V
        noise_power = sigma_V ** 2
        data.append((mV, sigma_V, noise_power))
    return data

def add_colored_noise(wave, noise_power, npw, mf, color='pink', plot=False, mod_envelope=None):
    """
    Add colored noise (white, pink, or brown) to a signal.

    Parameters:
    - wave: Original signal (numpy array).
    - noise_power: Base noise power level (variance).
    - npw: Tuple specifying the range over which to vary the noise power (relative to noise_power).
    - mf: Tuple specifying the modulation factor range to slightly vary the amplitude of the signal.
    - color: Type of noise to add ('white', 'pink', 'brown'). Default is 'pink'.
    - plot: Boolean indicating whether to plot the noise. Default is False.
    - mod_envelope: Dictionary {'func': envelope_sine, 'param': [0.0001, 0.01]}

    Returns:
    - res: The signal with added colored noise.
    """

    # Determine noise power within the specified range
    noise_pw = noise_power # * np.random.uniform(*npw)
    
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

    # Optional plotting
    if plot:
        plt.figure(figsize=(50, 5))
        plt.plot(range(len(res)), res, label=f'{color} Noise')
        plt.title(f'{color} Noise')
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.legend()
        #plt.grid(True)
        plt.show()

    return res