import numpy as np
import random

#from SigVarGen.utils import interpoling

def generate_semi_periodic_signal(length=450, base_pattern=None, flip_probability=0.1, seed=None):

    """
    Generate a semi-periodic digital signal with optional bit-flipping noise.

    This function creates a periodic sequence based on a base pattern and repeats it 
    to match the desired length. It also introduces random bit flips to simulate variations.

    Parameters:
    ----------
    length : int, optional
        The total length of the generated signal (default: 450).
    base_pattern : list of int, optional
        A binary list representing the repeating base pattern. If None, defaults to `[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]`.
    flip_probability : float, optional
        The probability of flipping each bit in the signal (default: 0.1).
    seed : int, optional
        Seed for random number generator to ensure reproducibility (default: None).

    Returns:
    -------
    numpy.ndarray
        The generated semi-periodic binary signal as an array.

    Example:
    -------
    >>> import numpy as np
    >>> signal = generate_semi_periodic_signal(length=1000, flip_probability=0.05)
    >>> print(signal[:20])  # First 20 values of the generated signal

    Notes:
    ------
    - Increasing `flip_probability` results in more random bit flips, making the signal less periodic.
    - If `base_pattern` is provided, the function will replicate and truncate it to fit `length`.
    """

    if base_pattern is None:
        base_pattern = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]

    if seed is not None:
        np.random.seed(seed)
        
    base_pattern = np.array(base_pattern, dtype=int)
    pattern_length = len(base_pattern)
    
    repeats_needed = (length // pattern_length) + 1
    signal = np.tile(base_pattern, repeats_needed)[:length]
    
    # Introduce random flips (bits of 0 changed to 1 or vice versa)
    random_flips = np.random.rand(length) < flip_probability
    # Flip the bits where random_flips is True
    signal[random_flips] = 1 - signal[random_flips]
    
    return signal #np.array([round(i) for i in interpoling(signal, target_len=length)])

def add_periodic_interrupts(base_signal, amplitude_range, inter_sig, start_idx, duration_idx, length=450, base_pattern=None, base_pattern_2=None, flip_probability=0.1, flip_probability_2=0.1, offset=0):

    """
    Add periodic digital interruptions to a continuous base signal.

    This function introduces periodic binary (0/1) signal interruptions into the base signal. 
    The interruptions are scaled versions of `inter_sig`, and they appear in two distinct phases:
    - Before and after the main interruption.
    - During the main interruption.

    Parameters:
    ----------
    base_signal : numpy.ndarray
        The original signal to which periodic interruptions will be added.
    amplitude_range : list or tuple
        Contains minimum and maximum aplitude of the device.
    inter_sig : numpy.ndarray
        The interrupt signal to be modulated and inserted into the base signal.
    offset : float
        The amplitude offset applied to the interruptions.
    start_idx : int
        The start index of the main interruption.
    duration_idx : int
        The duration (in samples) of the main interruption.
    length : int, optional
        The length of the default periodic signal if `func` is None (default: 450).
    base_pattern, base_pattern_2 : list of int, optional
        A binary list representing the repeating base pattern. If None, defaults to `[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]`.
    flip_probability, flip_probability_2 : float, optional
        The probability of flipping each bit in the signal (default: 0.1).

    Returns:
    -------
    numpy.ndarray
        The modified base signal with periodic interruptions.

    Example:
    -------
    >>> import numpy as np
    >>> base_signal = np.ones(1000)  # Example base signal
    >>> inter_sig = np.sin(np.linspace(0, np.pi, 1000))  # Example interrupting waveform
    >>> modified_signal = add_periodic_interrupts(base_signal, inter_sig, offset=0.5, start_idx=300, duration_idx=100)
    >>> print(modified_signal[:350])  # Print first 350 samples

    Notes:
    ------
    - The first phase of interruptions affects the signal **before and after** `start_idx` to `start_idx + duration_idx`.
    - The second phase introduces modulated interruptions **within the specified range**.
    """

    dig_sig1 = generate_semi_periodic_signal(length=length, base_pattern=base_pattern, flip_probability=flip_probability)

    dig_sig2 = generate_semi_periodic_signal(length=length, base_pattern=base_pattern_2, flip_probability=flip_probability_2)

    offset1 = (offset/1.3)*dig_sig1
    interrupts = (inter_sig.copy() * dig_sig1)

    base_signal[:start_idx] = base_signal[:start_idx] + interrupts[:start_idx]
    base_signal[start_idx+duration_idx:] = base_signal[start_idx+duration_idx:] + interrupts[start_idx+duration_idx:]

    rand1 = random.uniform(offset/1.6, offset/1.85)
    offset2 = (rand1)*dig_sig2
    interrupts = (inter_sig.copy() * dig_sig2)

    base_signal[start_idx:start_idx+duration_idx] = base_signal[start_idx:start_idx+duration_idx] + interrupts[start_idx:start_idx+duration_idx]

    base_signal = np.clip(base_signal, amplitude_range[0], amplitude_range[1])

    return base_signal