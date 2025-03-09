import numpy as np
import random
import pytest

from SigVarGen import add_periodic_interrupts, generate_semi_periodic_signal

# -------------------------------------
# Tests for add_periodic_interrupts
# -------------------------------------

def test_add_periodic_interrupts_basic(sample_time_vector):
    """
    Basic functionality test: Adding periodic interrupts to a flat base signal.
    """
    t = sample_time_vector
    base_signal = np.ones_like(t) * 0.5
    inter_sig = np.ones_like(t)

    start_idx = 100
    duration_idx = 200
    offset = 2.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    # Check that changes occurred before and after the main window
    assert np.any(modified_signal[:start_idx] != base_signal[:start_idx]), "Pre-window signal should be modified"
    assert np.any(modified_signal[start_idx+duration_idx:] != base_signal[start_idx+duration_idx:]), "Post-window signal should be modified"
    # Check that changes occurred within the main window
    assert np.any(modified_signal[start_idx:start_idx+duration_idx] != base_signal[start_idx:start_idx+duration_idx]), "Main window signal should be modified"

def test_add_periodic_interrupts_with_high_base_signal(sample_time_vector):
    """
    Test with a high-amplitude base signal (boundary case).
    """
    t = sample_time_vector
    base_signal = np.ones_like(t) * 5.0
    inter_sig = np.ones_like(t)

    start_idx = 150
    duration_idx = 300
    offset = 1.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 6),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Base signal should be modified when periodic interrupts are added"

def test_add_periodic_interrupts_with_zero_offset(sample_time_vector):
    """
    Test periodic interrupts with zero offset.
    """
    t = sample_time_vector
    base_signal = np.ones_like(t) * 0.5
    inter_sig = np.ones_like(t)

    start_idx = 200
    duration_idx = 100
    offset = 0.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified even with zero offset (from the interrupts themselves)"

def test_add_periodic_interrupts_with_short_signal():
    """
    Test edge case with a very short signal.
    """
    base_signal = np.zeros(50)
    inter_sig = np.ones(50)

    start_idx = 10
    duration_idx = 20
    offset = 1.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 1),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=50
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified for short signals too"

def test_add_periodic_interrupts_with_partial_overlap(sample_time_vector):
    """
    Test where the interruption window partially overlaps the signal edges.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    inter_sig = np.ones_like(t)

    start_idx = len(t) - 50
    duration_idx = 100  # This pushes beyond the end of the signal
    offset = 1.5

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 1),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should still be modified even with edge overlap"
    assert np.any(modified_signal[start_idx:] != base_signal[start_idx:]), "Overlap region should be modified"

def test_add_periodic_interrupts_with_random_amplitude(sample_time_vector):
    """
    Test that the amplitude scaling varies within the expected boundaries.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    inter_sig = np.ones_like(t)

    start_idx = 300
    duration_idx = 150
    offset = 2.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 1),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t)
    )

    # Since the amplitude scaling involves randomness, we verify the overall boundaries.
    assert np.max(modified_signal) <= 1, "Max amplitude should be within boundaries"
    assert np.min(modified_signal) >= 0, "Min amplitude should be within boundaries"

def test_add_periodic_interrupts_with_custom_base_patterns(sample_time_vector):
    """
    Test that providing custom base patterns for the two phases results in a different output.
    """
    t = sample_time_vector
    base_signal = np.ones_like(t) * 0.5
    inter_sig = np.ones_like(t) * 2

    start_idx = 100
    duration_idx = 200
    offset = 2.0

    # Use custom base patterns and no bit-flipping (flip_probability=0) for determinism.
    custom_base_pattern1 = [0, 1, 1, 0, 1, 1]
    custom_base_pattern2 = [1, 1, 0, 1, 1, 0]

    modified_signal_custom = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        base_pattern=custom_base_pattern1,
        base_pattern_2=custom_base_pattern2,
        flip_probability=0,
        flip_probability_2=0
    )

    # Now run with default base patterns (and no flipping)
    modified_signal_default = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        flip_probability=0,
        flip_probability_2=0
    )
    
    # The outputs should differ because of the different base patterns.
    assert not np.array_equal(modified_signal_custom, modified_signal_default), "Custom base patterns should produce different output than default"

def test_add_periodic_interrupts_with_custom_flip_probabilities(sample_time_vector):
    """
    Test that varying flip probabilities (for both phases) alters the output compared to no flipping.
    """
    t = sample_time_vector
    base_signal = np.ones_like(t) * 0.5
    inter_sig = np.ones_like(t) * 2

    start_idx = 100
    duration_idx = 200
    offset = 2.0

    # Using no flipping.
    modified_signal_no_flip = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        flip_probability=0,
        flip_probability_2=0
    )

    # Using high flipping probabilities.
    modified_signal_high_flip = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        amplitude_range=(0, 2),
        inter_sig=inter_sig,
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        flip_probability=0.9,
        flip_probability_2=0.9
    )

    # The outputs should differ due to the effect of random bit flips.
    assert not np.array_equal(modified_signal_no_flip, modified_signal_high_flip), "High flip probabilities should produce different outputs compared to no flipping"

# -------------------------------------
# Tests for generate_semi_periodic_signal
# -------------------------------------

def test_generate_semi_periodic_signal_length():
    """
    Test that the generated semi-periodic signal has the correct length.
    """
    length = 500
    signal = generate_semi_periodic_signal(length=length)
    assert len(signal) == length, "Generated signal length should match the specified length"

def test_generate_semi_periodic_signal_default_pattern():
    """
    Test that the default base pattern is used when none is provided.
    """
    signal = generate_semi_periodic_signal(length=100)
    # With the default pattern, there should be at least one occurrence of 1.
    assert np.any(signal == 1), "Signal should contain 1s when using the default base pattern"

def test_generate_semi_periodic_signal_reproducibility():
    """
    Test that providing a seed produces reproducible signals.
    """
    seed = 42
    signal1 = generate_semi_periodic_signal(length=200, seed=seed)
    signal2 = generate_semi_periodic_signal(length=200, seed=seed)
    np.testing.assert_array_equal(signal1, signal2, "Signals with the same seed should be identical")

def test_generate_semi_periodic_signal_flip_probability():
    """
    Test that increasing the flip probability results in more bit flips.
    """
    signal_low_flip = generate_semi_periodic_signal(length=300, flip_probability=0.0, seed=123)
    signal_high_flip = generate_semi_periodic_signal(length=300, flip_probability=0.5, seed=123)
    # Count differences between the two signals.
    flips = np.sum(signal_low_flip != signal_high_flip)
    assert flips > 0, "Higher flip probability should result in more bit flips"
