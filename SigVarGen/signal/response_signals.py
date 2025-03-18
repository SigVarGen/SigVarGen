import numpy as np
import random

from SigVarGen.signal.signal_generation import generate_signal
from SigVarGen.variations.baseline_drift import apply_baseline_drift_middle_peak

def get_non_overlapping_interval(signal_length, duration_idx, occupied_intervals, max_tries=1000, buffer=1):
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
    buffer : int, optional
        Extra buffer to prevent interrupts from being placed too close to each other.

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
        start_idx = random.randint(0, max(0, signal_length - duration_idx))
        end_idx = min(signal_length-1, start_idx + duration_idx)
        # Check overlap
        overlap = any(not (end_idx <= s-buffer or start_idx >= e+buffer) for (s, e) in occupied_intervals)
        if not overlap:
            return start_idx, end_idx
    return None

def place_interrupt(signal_length, duration_ratio, occupied_intervals, non_overlap, buffer=1):
    
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
    buffer : int, optional
        Extra buffer to prevent interrupts from being placed too close to each other.

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
        interval = get_non_overlapping_interval(signal_length, duration_idx, occupied_intervals, buffer=buffer)
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

    This function linearly combines a base signal slice and an interrupt slice using 
    a blend factor. The blending determines how much of the base signal is retained 
    versus how much of the interrupt is applied.

    Parameters
    ----------
    base_slice : np.ndarray
        The base signal segment to be modified.
    interrupt_slice : np.ndarray
        The interrupt signal segment to be blended into the base signal.
    blend : float, optional
        The blending factor between 0 and 1 (default: 0.5).
        - A value closer to 1 retains more of the base signal.
        - A value closer to 0 retains more of the interrupt signal.

    Returns
    -------
    blended_signal : np.ndarray
        The resulting signal segment after blending.
    """
    return blend * base_slice + (1 - blend) * interrupt_slice


def apply_interrupt_modifications(
    inter_part, base_part, device_min, device_max, drop, disperse=False, blend_factor=0.5
):
    """
    Apply modifications to an interrupt signal and ensure it fits within device constraints.

    This function adjusts an interrupt signal segment by optionally applying baseline drift, 
    shifting its amplitude within the allowed device range, and blending it into the base signal.

    Parameters
    ----------
    inter_part : np.ndarray
        The segment of the interrupt signal to be modified.
    base_part : np.ndarray
        The corresponding segment of the base signal.
    device_min : float
        Minimum allowed amplitude of the device.
    device_max : float
        Maximum allowed amplitude of the device.
    drop : bool
        If True, shifts the interrupt signal downward (drop below baseline).
        If False, shifts the interrupt signal upward.
    disperse : bool, optional
        If True, the interrupt will have a varying baseline drift with peak drift in the middle (default: True).
    blend_factor : float, optional
        Blend weight between base and interrupt signal (default: 0.5).
        - A higher value retains more of the base signal.
        - A lower value retains more of the interrupt signal.

    Returns
    -------
    modified_inter_part : np.ndarray
        The modified interrupt signal segment after applying drift and offset adjustments.
    offset : float
        The amount by which the interrupt signal was shifted.
    """
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
    Generate a main interrupt signal. Acts as a wrapper around generate_signal 
    function for perturbating signal generation application.
    
    Parameters
    ----------
    t : np.ndarray
        Time vector for the signal (usually np.linspace).
    domain : str
        Key for amplitude/frequency ranges in interrupt_ranges.
    interrupt_ranges : dict
        Contains response amplitude and frequency ranges for each device domain.
    temp : int
        Determines which frequency index to select.
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
    interrupt_params : list of dict
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
    Add a main response signal to the base signal, with optional addition of complex response.

    The main interrupt is a sinusoidal-based signal, scaled and placed into the base signal.
    Optionally, smaller secondary overlapping interrupts can be added inside the main interrupt
    when `complex_iter` > 0.

    Parameters
    ----------
    t : np.ndarray
        Time vector for the signal (usually np.linspace).
    base_signal : np.ndarray
        The original base signal (may already contain some modifications).
    domain : str
        Key for amplitude/frequency ranges in RANGES.
    DEVICE_RANGES : dict
        Contains overall device amplitude/frequency limits.
    INTERRUPT_RANGES : dict
        Contains response amplitude and frequency ranges for each device domain.
    temp : int
        Determines which frequency index to select.
    duration_ratio : float
        Fraction of total signal length the main interrupt should occupy.
    disperse : bool, optional
        If True, the interrupt will have a varying baseline drift with peak drift in the middle (default: True).
    drop : bool, optional
        If True, modify signal to dip below baseline instead of rising above.
    n_sinusoids : int, optional
        Number of sinusoids to sum. If None, randomly chosen (2-10).
    non_overlap : bool, optional
        If True, prevents the main interrupt from overlapping with existing intervals.
    complex_iter : int, optional
        Number of smaller overlapping interrupts to add inside the main interrupt.
    blend_factor : float, optional
        Blend weight between base and interrupt (default = 0.5).
    shrink_complex : bool, optional
        If True, each successive smaller interrupt is shorter than the previous.
    shrink_factor : float, optional
        Fraction to shrink the duration of each smaller interrupt (default = 0.9).

    Returns
    -------
    updated_base_signal : np.ndarray
        The base signal after adding the response signal.
    interrupt_params : list of dict
        Metadata describing the main interrupt and any smaller overlapping interrupts.
        Each entry contains:
            - start_idx (int): Start index of the interrupt.
            - duration_idx (int): Length of the interrupt.
            - offset (float): Applied offset.
            - sinusoids_params (dict): Parameters used to generate the sinusoid.
            - type (str): "main" for primary interrupt.
    occupied_intervals : list of tuple
        Updated list of (start_idx, end_idx) representing all occupied intervals after adding interrupts.
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

    if base_slice.size <= 1 or inter_part_raw.size <= 1:
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

    # Add smaller overlapping interrupts if complex_iter > 0

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
        Key for amplitude/frequency ranges in RANGES.
    DEVICE_RANGES : dict
        Contains overall device amplitude/frequency limits.
    INTERRUPT_RANGES : dict
        Contains response amplitude and frequency ranges for each device domain.
    drop : bool
        If True => subtract offset, else add offset.
    old_offset : float
        The main offset used; we might scale from that or do something different.
    sinusoids_params : dict or list
        The metadata describing how the main interrupt was generated (reuse if you want).
    blend_factor : float, optional
        Blend weight between base and interrupt (default = 0.5).
    
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

    # Slice out the portion from the updated base signal and the full interrupt wave
    base_slice2 = base_signal[start_idx2:end_idx2]
    inter_part2_raw = full_interrupt_signal[start_idx2:end_idx2]

    if base_slice2.size <= 1 or inter_part2_raw.size <= 1:
        return base_signal, None

    # Optionally apply drift + offset with bounding logic
    inter_part2_modified, final_offset2 = apply_interrupt_modifications(
        inter_part=inter_part2_raw.copy(),
        base_part=base_slice2.copy(),
        device_min=min(INTERRUPT_RANGES[domain]['amplitude'][0], DEVICE_RANGES[domain]['amplitude'][0]),
        device_max=max(INTERRUPT_RANGES[domain]['amplitude'][1], DEVICE_RANGES[domain]['amplitude'][1]),
        drop=drop,
        disperse=False, 
        blend_factor=blend_factor
    )

    # Combine with the base signal
    updated_slice2 = blend_signal(base_slice2, inter_part2_modified, blend=blend_factor)

    # Check final bounding and clamp if you want to avoid any small overshoot ? Should be redundant
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
    non_overlap=True,
    buffer=1
):
    """
    Add secondary (smaller) interrupts to a base signal.

    This function places and blends smaller sinusoidal-based interrupts into an existing
    base signal.

    Parameters
    ----------
    t : np.ndarray
        Time vector for the signal (usually np.linspace).
    base_signal : np.ndarray
        The original base signal (may already contain some modifications).
    INTERRUPT_RANGES : dict
        Contains response amplitude and frequency ranges for each device domain.
    domain : str
        Key for amplitude/frequency ranges in INTERRUPT_RANGES.
    temp : int
        Determines which frequency index to select.
    n_smaller_interrupts : int
        Number of smaller interrupts to insert into the base signal.
    occupied_intervals : list
        List of already occupied intervals (start_idx, end_idx) — used to avoid overlap.
    disperse : bool
        If True, the signal will have a varying baseline drift (default: True).
    drop : bool
        If True, modify signal to dip below baseline instead of rising above.
    small_duration_ratio : float
        Fraction of total signal length each small interrupt should occupy.
    n_sinusoids : int, optional
        Number of sinusoids to sum. If None, randomly chosen (2-10).
    non_overlap : bool, optional
        If True, prevents smaller interrupts from overlapping with occupied intervals.
    buffer : int, optional
        Minimum spacing (in samples) to keep between interrupts when non_overlap=True.
        Default is 1 sample, can be adjusted to enforce larger gaps.

    Returns
    -------
    updated_base_signal : np.ndarray
        The base signal after adding the new interrupts.
    interrupt_params : list of dict
        Metadata describing the smaller interrupt that was added.
        Metadata for each added interrupt, contains:
            - start_idx (int): Start index of interrupt.
            - duration_idx (int): Length of the interrupt.
            - offset (float): Applied offset.
            - sinusoids_params (dict): Parameters used to generate the sinusoid.
            - type (str): "small" indicating this is a smaller interrupt.
    """

    interrupt_params = []

    for _ in range(n_smaller_interrupts):
        
        # Generate interrupt signal (full length, then sliced later)
        small_interrupt_signal, small_sinusoids_params = generate_main_interrupt(
            t=t,
            domain=domain,
            interrupt_ranges=INTERRUPT_RANGES,
            temp=temp,
            n_sinusoids=n_sinusoids,
            amplitude_scale=1.0,
            frequency_scale=1.0
        )

        # Place the interrupt into the signal
        start_idx, end_idx = place_interrupt(
            len(t),
            small_duration_ratio,
            occupied_intervals,
            non_overlap,
            buffer=buffer
        )

        # If no valid position is found, skip this interrupt
        if start_idx is None:
            continue

        # Slice the relevant section of both base and generated signal
        base_slice = base_signal[start_idx:end_idx]
        s_inter_raw = small_interrupt_signal[start_idx:end_idx]

        if base_slice.size <= 1 or s_inter_raw.size <= 1:
            return base_signal, []

        # Apply signal modifications (e.g., dispersal, offset shift, clipping to device limits)
        s_inter_modified, s_offset = apply_interrupt_modifications(
            inter_part=s_inter_raw.copy(),
            base_part=base_slice.copy(),
            drop=drop,
            device_min=INTERRUPT_RANGES[domain]['amplitude'][0],
            device_max=INTERRUPT_RANGES[domain]['amplitude'][1],
            disperse=disperse
        )

        # Blend modified interrupt into the base signal
        base_signal[start_idx:end_idx] = blend_signal(base_slice, s_inter_modified)

        # Save metadata for this interrupt
        interrupt_params.append({
            'start_idx': start_idx,
            'duration_idx': end_idx - start_idx,
            'offset': s_offset,
            'sinusoids_params': small_sinusoids_params,
            'type': 'small'
        })

        # Mark interval as occupied to prevent future overlap
        occupied_intervals.append((start_idx, end_idx))

    return base_signal, interrupt_params


def add_interrupt_with_params(t, base_signal, domain, DEVICE_RANGES, INTERRUPT_RANGES, 
                            temp, drop=True, disperse=True, duration_ratio=None, n_smaller_interrupts=None, 
                            n_sinusoids=None, non_overlap=True, complex_iter=0, blend_factor=0.5, 
                            shrink_complex=False, shrink_factor=0.9, buffer=1):
    """
    Add one main interrupt and between 0 to 2 smaller interrupts to the signal.

    Parameters:
    ----------
    t : numpy.ndarray
        Time vector for the signal (usually np.linspace).
    base_signal : numpy.ndarray
        The base signal to modify.
    domain : str
        Key for amplitude/frequency ranges in RANGES.
    INTERRUPT_RANGES : dict
        Contains response amplitude and frequency ranges for each device domain.
    temp : int
        Determines which frequency index to select.
    drop : bool, optional
        If True, the interrupt signal will be negatively offset (default: True).
    disperse : bool, optional
        If True, the signal will have a varying baseline drift (default: True).
    duration_ratio : float, optional
        Ratio of signal length to allocate for main interrupt (default: Random from 0.06 to 0.12).
    n_smaller_interrupts : int, optional
        Number of smaller interrupts to add (default: Random 0 to 2).
    n_sinusoids : int, optional
        Number of sinusoids to sum. If None, randomly chosen (2-10).
    non_overlap : bool, optional
        If True, prevent interrupts from overlapping with previously occupied intervals.
    complex_iter : int, optional
        Number of smaller (overlapping) interrupts to embed inside the main interrupt region (default: 0).
    blend_factor : float, optional
        Blend weight between base and interrupt (default = 0.5).
    shrink_complex : bool, optional
        If True, each successive complex interrupt shrinks in size (default: False).
    shrink_factor : float, optional
        Fraction to shrink each overlapping complex interrupt by (default: 0.9).
    buffer : int, optional
        Minimum spacing (in samples) to keep between interrupts when non_overlap=True.
        Default is 1 sample, can be adjusted to enforce larger gaps.

    Returns:
    -------
    base_signal : numpy.ndarray
        The modified signal with added interrupts.
    interrupt_params : list of dict
        Metadata describing the smaller interrupt that was added.
        Metadata for each added interrupt, contains:
            - start_idx (int): Start index of interrupt.
            - duration_idx (int): Length of the interrupt.
            - offset (float): Applied offset.
            - sinusoids_params (dict): Parameters used to generate the sinusoid.
            - type (str): "small" indicating this is a smaller interrupt.
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
                non_overlap=non_overlap,
                buffer=buffer)

    return base_signal, main_interrupt_params + small_interrupt_params


def add_interrupt_bursts(
    t,
    base_signal,
    domain,
    DEVICE_RANGES,
    device_min,
    device_max,
    temp,
    start_idx=0,
    end_idx=0,
    n_small_interrupts=None,
    non_overlap=False,
    small_duration_ratio_range=None
):
    """
    Add multiple small interrupts to the signal within a specified time window.

    Parameters
    ----------
    t : np.ndarray
        Time vector for the signal (usually np.linspace).
    base_signal : np.ndarray
        The base signal to modify.
    domain : str
        Key for amplitude/frequency ranges in RANGES.
    DEVICE_RANGES : dict
        Contains overall device amplitude/frequency limits.
    device_min : float
        Minimum possible amplitude of the device.
    device_max : float
        Maximum possible amplitude of the device.
    temp : int
        Determines which frequency index to select.
    start_idx : int, optional
        Minimum start index for interrupts (default: 0).
    end_idx : int, optional
        Maximum end index for interrupts (default: 0, meaning full signal length).
    n_small_interrupts : int, optional
        Number of small interrupts to add (default: Random from 15 to 20).
    non_overlap : bool, optional
        If True, prevents overlap between bursts.
    small_duration_ratio_range : tuple of floats, optional (default: random from 0.001 to 0.005)
        Interrupt burst duration in relationship to t.


    Returns
    -------
    base_signal : np.ndarray
        The modified signal with added small interrupts.
    """
    if end_idx == 0:
        end_idx = len(t)

    burst_range = DEVICE_RANGES[domain]
    freq_range = burst_range['frequency'][temp] if temp != 0 else burst_range['frequency']
    burst_frequency_range = (freq_range[0] + (freq_range[1] - freq_range[0]) * 0.5, freq_range[1])

    if n_small_interrupts is None:
        n_small_interrupts = random.randint(15, 20)

    occupied_intervals = []
    dif = np.max(base_signal) - np.min(base_signal)

    for _ in range(n_small_interrupts):
        # Generate a small interrupt signal (full signal length)
        n_sinusoids = random.randint(2, 10)
        small_interrupt_signal, small_interrupt_sinusoids_params = generate_signal(
            t, n_sinusoids, (1 * burst_range['amplitude'][1], 1 * burst_range['amplitude'][1]), burst_frequency_range
        )

        # Convert global occupied intervals to local (within the window)
        local_occupied_intervals = [
            (s - start_idx, e - start_idx)
            for (s, e) in occupied_intervals
            if start_idx <= s < end_idx and start_idx <= e <= end_idx
        ]

        # Place within the window
        if small_duration_ratio_range == None:
            small_duration_ratio = random.uniform(0.001, 0.005)
        else:
            small_duration_ratio = random.uniform(small_duration_ratio_range[0],small_duration_ratio_range[1])
        local_start_idx, local_end_idx = place_interrupt(
            end_idx - start_idx,
            small_duration_ratio,
            local_occupied_intervals,
            non_overlap
        )

        # If placement failed (no room left), skip to next interrupt
        if local_start_idx is None:
            continue

        # Convert back to global indices
        actual_start_idx = local_start_idx + start_idx
        actual_end_idx = local_end_idx + start_idx

        # Slice the part of the generated signal to add
        s_inter_part = small_interrupt_signal[actual_start_idx:actual_end_idx]

        # Apply offset adjustment (random rise or drop)
        drop2 = random.choice([True, False])
        if drop2 and all(random.choice([True, False]) for _ in range(3)):  # Lower probability for "rise"
            s_offset = dif * random.uniform(0.01, 0.06)
            s_inter_part += s_offset
        else:
            s_offset = dif * random.uniform(0.06, 0.1)
            s_inter_part -= s_offset

        # Apply to base signal
        base_signal[actual_start_idx:actual_end_idx] = blend_signal(base_signal[actual_start_idx:actual_end_idx], s_inter_part)

        # Track this interval globally
        occupied_intervals.append((actual_start_idx, actual_end_idx))

    # Ensure final signal respects device limits
    base_signal = np.clip(base_signal, device_min, device_max)

    return base_signal