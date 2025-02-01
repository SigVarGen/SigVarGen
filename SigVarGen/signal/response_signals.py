import numpy as np
import random

from sigvargen.signal.signal_generation import generate_signal

def get_non_overlapping_interval(signal_length, duration_idx, occupied_intervals, max_tries=1000):
    """
    Attempt to find a start_idx for a new interrupt interval that does not overlap
    with any existing intervals in occupied_intervals. If no non-overlapping interval is found
    after max_tries, return None.

    Parameters:
    ----------
    signal_length : int
        The total length of the signal.
    duration_idx : int
        The duration (in samples) of the interrupt.
    occupied_intervals : list of tuples
        List of (start_idx, end_idx) pairs representing occupied intervals.
    max_tries : int, optional
        Maximum attempts to find a valid interval (default: 1000).

    Returns:
    -------
    tuple or None
        (start_idx, end_idx) if a non-overlapping interval is found, otherwise None.

    Example:
    -------
    >>> occupied = [(100, 200), (300, 400)]
    >>> get_non_overlapping_interval(1000, 50, occupied)
    (450, 500)  # Example output
    """

    for _ in range(max_tries):
        start_idx = random.randint(0, signal_length - duration_idx)
        end_idx = start_idx + duration_idx
        # Check overlap
        overlap = any(not (end_idx <= s-100 or start_idx >= e+100) for (s, e) in occupied_intervals)
        if not overlap:
            return start_idx, end_idx
    return None

def place_interrupt(signal_length, duration_ratio, occupied_intervals, non_overlap):
    
    """
    Wrapper function to find a valid location for an interrupt in the signal.

    Parameters:
    ----------
    signal_length : int
        Length of the signal.
    duration_ratio : float
        Fraction of the signal length for the interrupt duration.
    occupied_intervals : list of tuples
        List of existing occupied intervals.
    non_overlap : bool, optional
        Whether to ensure non-overlapping placement (default: True).

    Returns:
    -------
    tuple or None
        (start_idx, end_idx) if a valid placement is found, otherwise None.

    Example:
    -------
    >>> occupied = [(100, 200), (300, 400)]
    >>> place_interrupt(1000, 0.05, occupied)
    (500, 550)  # Example output
    """

    duration_idx = int(duration_ratio * signal_length)

    if non_overlap:
        interval = get_non_overlapping_interval(signal_length, duration_idx, occupied_intervals)
    else:
        start_idx = random.randint(0, signal_length - duration_idx)
        end_idx = start_idx + duration_idx

    if interval is None:
        return None, None  

    return interval


def apply_interrupt_modifications(inter_part, base_signal, disperse, drop):
    
    """
    Modify the interrupt signal by adding amplitude variations and baseline drift.

    Parameters:
    ----------
    inter_part : numpy.ndarray
        The interrupt waveform segment.
    base_signal : numpy.ndarray
        The base signal to compare amplitude ranges.
    disperse : bool
        Whether to apply random baseline drift.
    drop : bool
        If True, interrupt is negatively offset; otherwise, positively offset.

    Returns:
    -------
    tuple
        Modified inter_part and applied offset value.

    Example:
    -------
    >>> modified_inter, offset = apply_interrupt_modifications(inter_part, base_signal, disperse=True, drop=False)
    """

    dif = np.max(base_signal) - np.min(base_signal)
    offset = dif * random.uniform(1.0, 2.0)

    if disperse:
        inter_part = apply_baseline_drift_middle_peak(inter_part.copy(), max_drift=15)
        offset = dif * random.uniform(0.05, 1.0)

    if drop:
        inter_part -= offset
    else:
        inter_part += offset

    return inter_part, offset


def add_main_interrupt(t, base_signal, domain, INTERRUPT_RANGES, temp, disperse, drop, duration_ratio, n_sinusoids=None, non_overlap=True, complex_iter=0):
    
    """
    Add the main interrupt signal to the base signal, with optional smaller overlapping interruptions.

    Parameters:
    ----------
    t : numpy.ndarray
        Time vector of the signal.
    base_signal : numpy.ndarray
        The base signal to modify.
    domain : str
        The domain to use for selecting amplitude and frequency ranges.
    INTERRUPT_RANGES : dict
        Dictionary containing frequency and amplitude ranges for interrupts.
    temp : int
        Determines which frequency range to select.
    disperse : bool
        If True, the signal will have a varying baseline drift.
    drop : bool
        If True, the interrupt signal will be negatively offset. Otherwise, positive offset.
    duration_ratio : float
        Ratio of signal length to allocate for main interrupt.
    complex_iter : int, optional
        Number of overlapping interruptions to add (default: 0, no overlapping).
    n_sinusoids : int, optional
        Number of sinusoids in the main interrupt (default: Random 2-10).
    non_overlap : bool, optional
        Whether to ensure interrupts do not overlap (default: True).

    Returns:
    -------
    base_signal : numpy.ndarray
        The modified signal with added interrupts.
    interrupt_params : list of dict
        List of dictionaries containing details about the interrupts.
    occupied_intervals : list
        List of occupied signal intervals to prevent overlap.

    Example:
    -------
    >>> base_signal, params, occupied = add_main_interrupt(t, base_signal, "Arduino Board", INTERRUPT_RANGES, 1, True, False, 0.1)

    """

    interrupt_range = INTERRUPT_RANGES[domain]
    freq_range = interrupt_range['frequency'][temp] if temp != 0 else interrupt_range['frequency']
    interrupt_frequency_range = (freq_range[0] + (freq_range[1] - freq_range[0]) * 0.5, freq_range[1])

    if n_sinusoids is None:
        n_sinusoids = random.randint(2, 10)

    # Generate main interrupt signal
    interrupt_signal, interrupt_sinusoids_params = generate_signal(
        t, n_sinusoids, interrupt_range['amplitude'], interrupt_frequency_range
    )

    occupied_intervals = []
    start_idx, end_idx = place_interrupt(len(t), duration_ratio, occupied_intervals, non_overlap)

    if start_idx is None:
        return base_signal, [], occupied_intervals 

    inter_part = interrupt_signal[start_idx:end_idx].copy()
    inter_part, offset = apply_interrupt_modifications(inter_part, base_signal, disperse, drop)

    base_signal[start_idx:end_idx] += inter_part

    interrupt_params = [{
        'start_idx': start_idx,
        'duration_idx': end_idx - start_idx,
        'offset': offset,
        'sinusoids_params': interrupt_sinusoids_params,
        'type': 'main'
    }]

    occupied_intervals.append((start_idx, end_idx))

    # === Adding Smaller Overlapping Interrupts if complex_iter > 0 ===
    for _ in range(complex_iter):
        start_idx2 = random.randint(start_idx, end_idx)  
        end_idx2 = min(start_idx2 + random.randint((end_idx - start_idx) // 5, (end_idx - start_idx) // 3), end_idx)

        offset2 = random.uniform(offset, offset * 1.4)
        inter_part2 = interrupt_signal[start_idx2:end_idx2].copy()

        inter_part2 = apply_baseline_drift_middle_peak(inter_part2, max_drift=80, min_drift=10)

        if drop:
            inter_part2 -= offset2
        else:
            inter_part2 += offset2

        base_signal[start_idx2:end_idx2] += inter_part2

        interrupt_params.append({
            'start_idx': start_idx2,
            'duration_idx': end_idx2 - start_idx2,
            'offset': offset2,
            'sinusoids_params': interrupt_sinusoids_params,
            'type': 'main_overlapping'
        })

    return base_signal, interrupt_params, occupied_intervals


def add_smaller_interrupts(t, base_signal, INTERRUPT_RANGES, domain, temp, n_smaller_interrupts, occupied_intervals, disperse, drop, n_sinusoids=None, non_overlap=True):
    """
    Add smaller secondary interrupts to the base signal.
    """
    interrupt_range = INTERRUPT_RANGES[domain]
    freq_range = interrupt_range['frequency'][temp] if temp != 0 else interrupt_range['frequency']

    interrupt_frequency_range = (freq_range[0] + (freq_range[1] - freq_range[0]) * 0.5, freq_range[1])

    interrupt_params = []
    dif = np.max(base_signal) - np.min(base_signal)

    for _ in range(n_smaller_interrupts):
        if n_sinusoids is None:
            n_sinusoids = random.randint(2, 10)
        small_interrupt_signal, small_interrupt_sinusoids_params = generate_interrupt_signal(
            t, n_sinusoids, (0.7 * interrupt_range['amplitude'][0], 0.9 * interrupt_range['amplitude'][1]), interrupt_frequency_range
        )

        small_duration_ratio = random.uniform(0.04, 0.55)
        start_idx, end_idx = place_interrupt(len(t), small_duration_ratio, occupied_intervals, non_overlap)

        if start_idx is None:
            continue 

        s_inter_part = small_interrupt_signal[start_idx:end_idx]
        s_offset = dif * random.uniform(0.45, 0.6)

        if disperse:
            s_inter_part = apply_baseline_drift_middle_peak(s_inter_part.copy(), max_drift=10)
            s_offset = dif * random.uniform(0.01, 0.6)

        if drop:
            s_inter_part -= s_offset
        else:
            s_inter_part += s_offset

        base_signal[start_idx:end_idx] += s_inter_part

        interrupt_params.append({
            'start_idx': start_idx,
            'duration_idx': end_idx - start_idx,
            'offset': s_offset,
            'sinusoids_params': small_interrupt_sinusoids_params,
            'type': 'small'
        })

        occupied_intervals.append((start_idx, end_idx))

    return base_signal, interrupt_params


def add_interrupt_with_params(t, base_signal, domain, INTERRUPT_RANGES, temp, drop=True, disperse=True, duration_ratio=None, n_smaller_interrupts=None, n_sinusoids=None):
    """
    Add one main interrupt and between 0 to 2 smaller interrupts (non-overlapping) to the signal.

    Parameters:
    ----------
    t : numpy.ndarray
        Time vector of the signal.
    base_signal : numpy.ndarray
        The base signal to modify.
    domain : str
        The domain to use for selecting amplitude and frequency ranges.
    INTERRUPT_RANGES : dict
        Dictionary containing frequency and amplitude ranges for interrupts.
    temp : int
        Determines which frequency range to select.
    drop : bool, optional
        If True, the interrupt signal will be negatively offset (default: True).
    disperse : bool, optional
        If True, the signal will have a varying baseline drift (default: True).
    duration_ratio : float, optional
        Ratio of signal length to allocate for main interrupt (default: Random from 0.06 to 0.12).
    n_smaller_interrupts : int, optional
        Number of smaller interrupts to add (default: Random 0 to 2).

    Returns:
    -------
    base_signal : numpy.ndarray
        The modified signal with added interrupts.
    interrupt_params : list of dict
        List of dictionaries containing details about the interrupts.
    """
    if duration_ratio is None:
        duration_ratio = random.uniform(0.06, 0.12)

    base_signal, main_interrupt_params, occupied_intervals = add_main_interrupt(
        t, base_signal, domain, INTERRUPT_RANGES, temp, disperse, drop, duration_ratio, n_sinusoids=n_sinusoids
    )

    if n_smaller_interrupts is None:
        n_smaller_interrupts = random.randint(0, 2)

    base_signal, small_interrupt_params = add_smaller_interrupts(
        t, base_signal, INTERRUPT_RANGES, domain, temp, n_smaller_interrupts, occupied_intervals, disperse, drop, n_sinusoids=n_sinusoids
    )

    return base_signal, main_interrupt_params + small_interrupt_params


def add_interrupt_bursts(t, base_signal, domain, INTERRUPT_RANGES, temp, start_idx=0, end_idx=0, n_small_interrupts=None, non_overlap=False):
    """
    Add multiple small interrupts to the signal.

    Parameters:
    ----------
    t : numpy.ndarray
        Time vector of the signal.
    base_signal : numpy.ndarray
        The base signal to modify.
    domain : str
        The domain to use for selecting amplitude and frequency ranges.
    INTERRUPT_RANGES : dict
        Dictionary containing frequency and amplitude ranges for interrupts.
    temp : int
        Determines which frequency range to select.
    start_idx : int, optional
        Minimum start index for interrupts (default: 0).
    end_idx : int, optional
        Maximum end index for interrupts (default: 0).
    n_small_interrupts : int, optional
        Number of small interrupts to add (default: Random from 15 to 20).
    non_overlap : bool, optional
        If interrupt bursts overlaps with interrupts placed before

    Returns:
    -------
    base_signal : numpy.ndarray
        The modified signal with added small interrupts.
    """

    interrupt_range = INTERRUPT_RANGES[domain]
    freq_range = interrupt_range['frequency'][temp] if temp != 0 else interrupt_range['frequency']
    interrupt_frequency_range = (freq_range[0] + (freq_range[1] - freq_range[0]) * 0.5, freq_range[1])

    if n_small_interrupts is None:
        n_small_interrupts = random.randint(15, 20)

    occupied_intervals = []
    dif = np.max(base_signal) - np.min(base_signal)

    for _ in range(n_small_interrupts):
        # Generate a small interrupt signal
        n_sinusoids = random.randint(2, 10)
        small_interrupt_signal, small_interrupt_sinusoids_params = generate_signal(
            t, n_sinusoids, (0.7 * interrupt_range['amplitude'][1], 0.9 * interrupt_range['amplitude'][1]), interrupt_frequency_range
        )

        small_duration_ratio = random.uniform(0.001, 0.003)
        start_idx, end_idx = place_interrupt(len(t), small_duration_ratio, occupied_intervals, non_overlap)

        if start_idx is None:
            continue

        s_inter_part = small_interrupt_signal[start_idx:end_idx]

        # Randomly determine if offset should be added or subtracted
        drop2 = random.choice([True, False])
        if drop2 and all(random.choice([True, False]) for _ in range(3)):  # lower probability check
            s_offset = dif * random.uniform(0.01, 0.06)
            s_inter_part += s_offset
        else:
            s_offset = dif * random.uniform(0.06, 0.1)
            s_inter_part -= s_offset

        base_signal[start_idx:end_idx] += s_inter_part

        occupied_intervals.append((start_idx, end_idx))

    return base_signal



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
    
    return np.array([round(i) for i in interpoling(signal)])

def add_periodic_interrupts(base_signal, inter_sig, offset, start_idx, duration_idx, func=None, length=450, a=(1.7,2)):

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
    inter_sig : numpy.ndarray
        The interrupt signal to be modulated and inserted into the base signal.
    offset : float
        The amplitude offset applied to the interruptions.
    start_idx : int
        The start index of the main interruption.
    duration_idx : int
        The duration (in samples) of the main interruption.
    func : function, optional
        A custom function to generate a periodic signal. If None, the function defaults to `generate_semi_periodic_signal` (default: None).
    length : int, optional
        The length of the default periodic signal if `func` is None (default: 450).
    a : tuple (int, int), optional
        Increase length by random number in provided range, making density of bursts higher

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
    - If `func` is provided, it should return a binary (0/1) periodic pattern of the desired length.
    """

    if func == None:
        dig_sig1 = generate_semi_periodic_signal(length=length)
        rand1 = random.randint(length*a[0], length*a[1])
        dig_sig2 = generate_semi_periodic_signal(length=rand1)

    offset1 = (offset//1.3)*dig_sig1
    interrupts = (inter_sig.copy() * dig_sig1)-offset1

    base_signal[:start_idx] += interrupts[:start_idx]
    base_signal[start_idx+duration_idx:] += interrupts[start_idx+duration_idx:]

    rand1 = random.uniform(offset//1.6, offset//1.85)
    offset2 = (rand1)*dig_sig2
    interrupts = (inter_sig.copy() * dig_sig2)-offset2

    base_signal[start_idx:start_idx+duration_idx] += interrupts[start_idx:start_idx+duration_idx]

    return base_signal