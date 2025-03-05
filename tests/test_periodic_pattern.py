import numpy as np
import pytest
from SigVarGen import add_periodic_interrupts, generate_semi_periodic_signal


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
        inter_sig=inter_sig,
        amplitude_range=(0,2),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        a=(1.7, 2)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"

    # Check that changes occurred before and after main window
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
        inter_sig=inter_sig,
        amplitude_range=(0,6),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        a=(1.7, 2)
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
        inter_sig=inter_sig,
        amplitude_range=(0,2),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        a=(1.7, 2)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified even with zero offset (from the interrupts themselves)"


def test_add_periodic_interrupts_with_short_signal():
    """
    Test edge case with very short signal.
    """
    base_signal = np.zeros(50)
    inter_sig = np.ones(50)

    start_idx = 10
    duration_idx = 20
    offset = 1.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        inter_sig=inter_sig,
        amplitude_range=(0,1),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=50,
        a=(1.7, 2)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified for short signals too"


def test_add_periodic_interrupts_with_partial_overlap(sample_time_vector):
    """
    Test where interruption window partially overlaps the signal edges.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    inter_sig = np.ones_like(t)

    start_idx = len(t) - 50
    duration_idx = 100  # This pushes beyond the end of the signal
    offset = 1.5

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        inter_sig=inter_sig,
        amplitude_range=(0,1),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        a=(1.7, 2)
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should still be modified even with edge overlap"
    assert np.all(modified_signal[start_idx:] != base_signal[start_idx:]), "Overlap region should be modified"


def test_add_periodic_interrupts_with_random_amplitude(sample_time_vector):
    """
    Test that the amplitude scaling varies within the expected range.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    inter_sig = np.ones_like(t)

    start_idx = 300
    duration_idx = 150
    offset = 2.0

    modified_signal = add_periodic_interrupts(
        base_signal=base_signal.copy(),
        inter_sig=inter_sig,
        amplitude_range=(0,1),
        offset=offset,
        start_idx=start_idx,
        duration_idx=duration_idx,
        length=len(t),
        a=(1.7, 2)
    )

    # Since amplitude scaling has randomness, we can't assert exact values, but we can check ranges
    assert np.max(modified_signal) <= 1, "Max amplitude should be within boundaries"
    assert np.min(modified_signal) >= 0, "Min amplitude should be within boundaries"
