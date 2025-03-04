import numpy as np
import random

from SigVarGen.signal.signal_generation import generate_signal
from SigVarGen.variations.baseline_drift import apply_baseline_drift_middle_peak

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
        interval = (start_idx, end_idx)

    if interval is None:
        return None, None  

    print(interval)
    return interval

def blend_signal(base_slice, interrupt_slice, blend=0.5):
    """
    Blend an interrupt slice into a base slice with a specified factor.
    """
    return blend * base_slice + (1 - blend) * interrupt_slice


def apply_interrupt_modifications(
    inter_part, base_part, device_min, device_max, drop, disperse=False, blend_factor=0.5
):
    if disperse:
        if not drop:
            allowed_drift = device_max - np.max(inter_part)
            allowed_drift = max(allowed_drift, 0)
            min_drift = np.max(inter_part)
            inter_part = apply_baseline_drift_middle_peak(inter_part, allowed_drift, direction='up', min_drift=min_drift)
        else:
            allowed_drift = np.min(inter_part) - device_min
            allowed_drift = max(allowed_drift, 0)
            min_drift = device_min
            inter_part = apply_baseline_drift_middle_peak(inter_part, allowed_drift, direction='down', min_drift=min_drift)

    # Compute the current interrupt range
    I_min, I_max = np.min(inter_part), np.max(inter_part)

    # Calculate available offset space to fit within device bounds
    if drop:
        # Drop = shift down
        max_offset = I_min - device_min
        min_offset = I_max - device_min  # Keep full interrupt within bounds
        offset_lower, offset_upper = -max_offset, -min_offset
    else:
        # Rise = shift up
        max_offset = device_max - I_max
        min_offset = device_max - I_min  # Keep full interrupt within bounds
        offset_lower, offset_upper = min_offset, max_offset

    # If something is weird (numerical instability), be safe
    if offset_lower > offset_upper:
        offset = 0.0
    else:
        offset = random.uniform(offset_lower, offset_upper)

    # Apply offset
    if drop:
        inter_part -= offset
    else:
        inter_part += offset

    return inter_part, offset


def generate_main_interrupt(
    t,
    domain,
    interrupt_ranges,
    temp,
    n_sinusoids=None,
    amplitude_scale=1.0,
    frequency_scale=1.0
):
    """
    Generate a main interrupt signal (raw sinusoidal wave).
    
    Parameters
    ----------
    t : np.ndarray
        Time vector.
    domain : str
        Device or domain to pick from interrupt_ranges.
    interrupt_ranges : dict
        Contains amplitude and frequency data for each domain.
    temp : int
        Determines which frequency index/range to select.
    n_sinusoids : int, optional
        Number of sinusoids to sum. If None, randomly chosen (2-10).
    amplitude_scale : float, optional
        Additional scale factor for amplitude (default=1.0).
    frequency_scale : float, optional
        Additional scale factor for frequency (default=1.0).

    Returns
    -------
    interrupt_signal : np.ndarray
        Generated sinusoidal-based interrupt signal (same length as t).
    interrupt_params : dict
        Parameters describing the generated sinusoids.
    """
    rng = interrupt_ranges[domain]
    
    # Pick frequency range
    if temp != 0:
        freq_range = rng['frequency'][temp]
    else:
        freq_range = rng['frequency']
        
    # Optionally scale frequency
    original_freq_min, original_freq_max = freq_range
    scaled_freq_min = max(original_freq_min, original_freq_min * frequency_scale)
    scaled_freq_max = min(original_freq_max, original_freq_max * frequency_scale)
    freq_range_scaled = (scaled_freq_min, scaled_freq_max)
    
    # Optionally scale amplitude
    original_amp_min, original_amp_max = rng['amplitude']
    scaled_amp_min = max(original_amp_min, original_amp_min * amplitude_scale)
    scaled_amp_max = min(original_amp_max, original_amp_max * amplitude_scale)
    amp_range_scaled = (scaled_amp_min, scaled_amp_max)

    # Number of sinusoids
    if n_sinusoids is None:
        n_sinusoids = random.randint(2, 10)

    # Actually generate the signal
    interrupt_signal, sinusoids_params = generate_signal(
        t,
        n_sinusoids,
        amp_range_scaled,
        freq_range_scaled
    )

    return interrupt_signal, sinusoids_params

def add_main_interrupt(
    t,
    base_signal,
    domain,
    DEVICE_RANGES,
    INTERRUPT_RANGES,
    temp,
    duration_ratio,
    disperse=True,
    drop=False,
    n_sinusoids=None,
    non_overlap=True,
    complex_iter=0,
    blend_factor=0.5,
    shrink_complex=False,
    shrink_factor=0.9
):
    """
    Orchestrate the process of adding a main interrupt to the base signal,
    plus optional smaller overlapping interruptions.
    """
    # Generate the main interrupt signal (raw)
    main_interrupt_signal, interrupt_sinusoids_params = generate_main_interrupt(
        t=t,
        domain=domain,
        interrupt_ranges=INTERRUPT_RANGES,
        temp=temp,
        n_sinusoids=n_sinusoids,
    )

    # Determine where to place
    occupied_intervals = []
    start_idx, end_idx = place_interrupt(
        len(t),
        duration_ratio,
        occupied_intervals,
        non_overlap
    )

    # If no space, return original
    if start_idx is None:
        return base_signal, [], occupied_intervals

    # Slice out the portion of the main interrupt
    inter_part_raw = main_interrupt_signal[start_idx:end_idx]

    # Apply modifications (offset, drift)
    base_slice = base_signal[start_idx:end_idx]

    if base_slice.size == 0 or inter_part_raw.size == 0:
        return base_signal, [], occupied_intervals

    inter_part_modified, offset_val = apply_interrupt_modifications(
        inter_part=inter_part_raw.copy(),
        base_part=base_slice.copy(),
        device_min=min(INTERRUPT_RANGES[domain]['amplitude'][0], DEVICE_RANGES[domain]['amplitude'][0]),
        device_max=max(INTERRUPT_RANGES[domain]['amplitude'][1], DEVICE_RANGES[domain]['amplitude'][1]),
        drop=drop,
        disperse=disperse
    )

    # Blend signal parts
    base_signal[start_idx:end_idx] = blend_signal(base_slice, inter_part_modified, blend=blend_factor)

    # Prepare metadata
    interrupt_params = [{
        'start_idx': start_idx,
        'duration_idx': end_idx - start_idx,
        'offset': offset_val,
        'sinusoids_params': interrupt_sinusoids_params,
        'type': 'main'
    }]

    occupied_intervals.append((start_idx, end_idx))

    # === Add smaller overlapping interrupts if complex_iter > 0 ===

    current_start = start_idx
    current_end = end_idx
    current_duration = end_idx - start_idx

    for _ in range(complex_iter):
        if shrink_complex:
            current_duration = max(1, int(current_duration * shrink_factor))

        complex_start = random.randint(current_start, max(current_start, current_end - current_duration))

        complex_end = complex_start + current_duration

        base_signal, complex_param = add_complexity_to_inter(
            base_signal=base_signal,
            full_interrupt_signal=main_interrupt_signal,
            start_main=complex_start,
            end_main=complex_end,
            domain=domain,
            DEVICE_RANGES=DEVICE_RANGES,
            INTERRUPT_RANGES=INTERRUPT_RANGES,
            drop=drop,
            old_offset=offset_val,
            sinusoids_params=interrupt_sinusoids_params,
            blend_factor=blend_factor
        )
        
        if complex_param:
            interrupt_params.append(complex_param)
        

    return base_signal, interrupt_params, occupied_intervals

def add_complexity_to_inter(
    base_signal,
    full_interrupt_signal,
    start_main,
    end_main,
    domain,
    DEVICE_RANGES,
    INTERRUPT_RANGES,
    drop,
    old_offset,
    sinusoids_params,
    blend_factor=0.5
):
    """
    Adds one 'complex' (overlapping) interrupt within the main interrupt region.

    Parameters
    ----------
    base_signal : np.ndarray
        The overall base signal, which may already have the main interrupt added.
    full_interrupt_signal : np.ndarray
        The full-length interrupt wave from which we slice a portion.
    start_main : int
        Start index of the main interrupt.
    end_main : int
        End index of the main interrupt.
    domain : str
        Key for amplitude/frequency ranges in INTERRUPT_RANGES.
    INTERRUPT_RANGES : dict
        Contains amplitude/frequency info for each domain.
    drop : bool
        If True => subtract offset, else add offset.
    old_offset : float
        The main offset used; we might scale from that or do something different.
    sinusoids_params : dict or list
        The metadata describing how the main interrupt was generated (reuse if you want).
    blend_factor : float, optional
        Weighting for final combination (default=0.5).
    
    Returns
    -------
    updated_base_signal : np.ndarray
        The base signal after adding the new overlapping interrupt.
    interrupt_params : dict
        Metadata describing the smaller interrupt that was added.
    """
    length_main = end_main - start_main
    if length_main <= 1:
        # No room to add a complex interrupt
        return base_signal, None

    min_small_len = max(1, length_main // 5)
    max_small_len = max(1, length_main // 3)
    duration2 = random.randint(min_small_len, max_small_len)
    start_idx2 = random.randint(start_main, max(start_main, end_main-duration2))
    end_idx2 = min(start_idx2 + duration2, end_main)

    # 2) Slice out the portion from the updated base signal and the full interrupt wave
    base_slice2 = base_signal[start_idx2:end_idx2]
    inter_part2_raw = full_interrupt_signal[start_idx2:end_idx2]

    if base_slice2.size <= 1 or inter_part2_raw.size <= 1:
        return base_signal, None

    #final_offset2 = random.uniform(old_offset, 1.4 * old_offset)

    # 4) Optionally apply drift + offset with bounding logic
    inter_part2_modified, final_offset2 = apply_interrupt_modifications(
        inter_part=inter_part2_raw.copy(),
        base_part=base_slice2.copy(),
        device_min=min(INTERRUPT_RANGES[domain]['amplitude'][0], DEVICE_RANGES[domain]['amplitude'][0]),
        device_max=max(INTERRUPT_RANGES[domain]['amplitude'][1], DEVICE_RANGES[domain]['amplitude'][1]),
        drop=drop,
        disperse=False,       # Maybe always disperse for complex interrupts?
        blend_factor=blend_factor
    )

    # 5) Combine with the base signal
    updated_slice2 = blend_signal(base_slice2, inter_part2_modified, blend=blend_factor)

    # 6) Check final bounding and clamp if you want to avoid any small overshoot:
    #updated_slice2 = np.clip(updated_slice2,
    #                         INTERRUPT_RANGES[domain]['amplitude'][0],
    #                         INTERRUPT_RANGES[domain]['amplitude'][1])

    # Write the updated slice back
    base_signal[start_idx2:end_idx2] = updated_slice2

    
    interrupt_params = {
        'start_idx': start_idx2,
        'duration_idx': end_idx2 - start_idx2,
        'offset': final_offset2,  # or offset2_raw if you used that
        'sinusoids_params': sinusoids_params,
        'type': 'main_overlapping'
    }

    return base_signal, interrupt_params

def add_smaller_interrupts(
    t,
    base_signal,
    INTERRUPT_RANGES,
    domain,
    temp,
    n_smaller_interrupts,
    occupied_intervals,
    disperse,
    drop,
    small_duration_ratio,
    n_sinusoids=None,
    non_overlap=True
):
    """
    Add secondary interrupts to the base signal, returning the updated signal
    plus metadata on each added interrupt.
    """
    interrupt_params = []

    for _ in range(n_smaller_interrupts):
        
        # 3) Generate interrupt signal
        small_interrupt_signal, small_sinusoids_params = generate_main_interrupt(
            t,
            domain,
            INTERRUPT_RANGES,
            temp,
            n_sinusoids=n_sinusoids,
            amplitude_scale=1.0,
            frequency_scale=1.0
        )

        # 2) Place
        start_idx, end_idx = place_interrupt(
            len(t), small_duration_ratio, occupied_intervals, non_overlap
        )
        if start_idx is None:
            continue

        # 3) Slice
        base_slice = base_signal[start_idx:end_idx]
        s_inter_raw = small_interrupt_signal[start_idx:end_idx]

        # 4) Modify
        s_inter_modified, s_offset = apply_interrupt_modifications(
            inter_part=s_inter_raw.copy(),
            base_part=base_slice.copy(),
            drop=drop,
            device_min=INTERRUPT_RANGES[domain]['amplitude'][0],
            device_max=INTERRUPT_RANGES[domain]['amplitude'][1],
            disperse=disperse
        )

        # 5) Combine
        base_signal[start_idx:end_idx] = blend_signal(base_slice, s_inter_modified) #s_inter_modified  

        # 6) Save metadata
        interrupt_params.append({
            'start_idx': start_idx,
            'duration_idx': end_idx - start_idx,
            'offset': s_offset,
            'sinusoids_params': small_sinusoids_params,
            'type': 'small'
        })

        occupied_intervals.append((start_idx, end_idx))

    return base_signal, interrupt_params




def add_interrupt_with_params(t, base_signal, domain, DEVICE_RANGES, INTERRUPT_RANGES, 
                            temp, drop=True, disperse=True, duration_ratio=None, n_smaller_interrupts=None, 
                            n_sinusoids=None, non_overlap=True, complex_iter=0, blend_factor=0.5, 
                            shrink_complex=False, shrink_factor=0.9):
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
                t=t,                               
                base_signal=base_signal,            
                domain=domain,                      
                DEVICE_RANGES=DEVICE_RANGES,        
                INTERRUPT_RANGES=INTERRUPT_RANGES,  
                temp=temp,                          
                duration_ratio=duration_ratio,      
                disperse=disperse,                  
                drop=drop,                          
                n_sinusoids=n_sinusoids,            
                non_overlap=non_overlap,            
                complex_iter=complex_iter,         
                blend_factor=blend_factor,
                shrink_complex=shrink_complex,
                shrink_factor=shrink_factor)


    if n_smaller_interrupts is None:
        n_smaller_interrupts = random.randint(0, 2)

    small_duration_ratio = random.uniform(0.01*duration_ratio, 0.9*duration_ratio)

    base_signal, small_interrupt_params = add_smaller_interrupts(
               t=t,
                base_signal=base_signal,
                INTERRUPT_RANGES=INTERRUPT_RANGES,
                domain=domain,
                temp=temp,
                n_smaller_interrupts=n_smaller_interrupts,
                occupied_intervals=occupied_intervals,
                disperse=disperse,
                drop=drop,
                small_duration_ratio=small_duration_ratio,
                n_sinusoids=n_sinusoids,
                non_overlap=non_overlap)

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