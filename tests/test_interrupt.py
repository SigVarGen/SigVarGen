import numpy as np
import pytest
from SigVarGen import generate_signal
from SigVarGen import (
    get_non_overlapping_interval,
    place_interrupt,
    blend_signal,
    apply_interrupt_modifications,
    generate_main_interrupt
)


# --- Tests for get_non_overlapping_interval ---

def test_get_non_overlapping_interval_no_conflict(sample_signal_length):
    """
    Ensure function can find a non-overlapping interval when no existing intervals are present.
    """
    occupied = []
    result = get_non_overlapping_interval(sample_signal_length, 50, occupied)

    assert result is not None, "Function should return a valid interval"
    assert 0 <= result[0] < sample_signal_length, "Start index should be within signal length"
    assert result[1] - result[0] == 50, "Interval duration should match requested duration"


def test_get_non_overlapping_interval_with_conflict():
    """
    Ensure function can find a non-overlapping interval when some occupied intervals exist.
    """
    occupied = [(100, 200), (300, 400)]
    result = get_non_overlapping_interval(1000, 50, occupied)

    assert result is not None, "Function should return a valid interval"

    start_idx, end_idx = result
    for (occ_start, occ_end) in occupied:
        assert end_idx <= occ_start - 100 or start_idx >= occ_end + 100, (
            f"Found interval ({start_idx}, {end_idx}) overlaps with occupied interval ({occ_start}, {occ_end})"
        )


def test_get_non_overlapping_interval_impossible():
    """
    Ensure function returns None when no valid interval can be found.
    """
    occupied = [(0, 999)]  # Entire space is taken
    result = get_non_overlapping_interval(1000, 50, occupied)
    assert result is None, "Should return None when placement is impossible"


# --- Tests for place_interrupt ---

def test_place_interrupt_non_overlap(sample_signal_length):
    """
    Ensure place_interrupt finds a non-overlapping interval when non_overlap=True.
    """
    occupied = [(100, 200)]
    result = place_interrupt(sample_signal_length, 0.05, occupied, non_overlap=True)

    assert result != (None, None), "Function should return a valid interval"

    start_idx, end_idx = result
    for (occ_start, occ_end) in occupied:
        assert end_idx <= occ_start - 100 or start_idx >= occ_end + 100, (
            f"Placed interval ({start_idx}, {end_idx}) overlaps with occupied interval ({occ_start}, {occ_end})"
        )


def test_place_interrupt_overlap_allowed(sample_signal_length):
    """
    Ensure place_interrupt works when overlapping is allowed (non_overlap=False).
    """
    occupied = [(100,200)]
    result = place_interrupt(sample_signal_length, 0.05, occupied, non_overlap=False)
    assert result != (None, None), "Function should return a valid interval when overlaps are allowed"


# --- Tests for blend_signal ---

def test_blend_signal():
    """
    Check blending two signals with 50% weight.
    """
    base = np.ones(100)
    interrupt = np.zeros(100)
    blended = blend_signal(base, interrupt, blend=0.5)

    assert np.allclose(blended, 0.5), "Blended signal should be average of base and interrupt when blend=0.5"


def test_blend_signal_weights():
    """
    Check blending with a custom blend factor (25% base, 75% interrupt).
    """
    base = np.ones(100)
    interrupt = np.zeros(100)
    blended = blend_signal(base, interrupt, blend=0.25)

    assert np.allclose(blended, 0.25 * base + 0.75 * interrupt), "Blended signal should respect custom blend factor"


# --- Tests for apply_interrupt_modifications ---

def test_apply_interrupt_modifications_rise():
    """
    Verify that modifications keep the signal within device bounds when rising.
    """
    inter_part = np.ones(100) * 0.5
    base_part = np.zeros(100)
    inter_mod, offset = apply_interrupt_modifications(
        inter_part, base_part, 0, 1, drop=False, disperse=False
    )
    assert np.min(inter_mod) >= 0, "Modified signal minimum should stay within device bounds (rise)"
    assert np.max(inter_mod) <= 1, "Modified signal maximum should stay within device bounds (rise)"


def test_apply_interrupt_modifications_drop():
    """
    Verify that modifications keep the signal within device bounds when dropping.
    """
    inter_part = np.ones(100) * 0.2
    base_part = np.ones(100) * 0.7
    inter_mod, offset = apply_interrupt_modifications(
        inter_part, base_part, 0, 1, drop=True, disperse=False
    )
    assert np.min(inter_mod) >= 0, "Modified signal minimum should stay within device bounds (drop)"
    assert np.max(inter_mod) <= 1, "Modified signal maximum should stay within device bounds (drop)"


def test_apply_interrupt_modifications_with_drift():
    """
    Check behavior when baseline drift is applied during modifications.
    """
    inter_part = np.ones(100) * 0.5
    base_part = np.zeros(100)
    inter_mod, offset = apply_interrupt_modifications(
        inter_part, base_part, 0, 1, drop=True, disperse=True
    )
    assert np.min(inter_mod) >= 0, "Modified signal minimum should stay within device bounds (with drift)"
    assert np.max(inter_mod) <= 1, "Modified signal maximum should stay within device bounds (with drift)"


# --- Tests for generate_main_interrupt ---

def test_generate_main_interrupt(sample_time_vector, sample_interrupt_ranges):
    """
    Verify generated interrupt has correct shape and expected number of sinusoids.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    interrupt_signal, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges, temp, n_sinusoids=5
    )
    assert interrupt_signal.shape == t.shape, "Generated signal shape should match time vector shape"
    assert len(params) == 5, "Number of sinusoid parameters should match requested n_sinusoids"
    assert all(key in params[0] for key in ["amp", "freq", "phase"]), "Each sinusoid should have amp, freq, phase"


def test_generate_main_interrupt_frequency_scaling(sample_time_vector, sample_interrupt_ranges):
    """
    Verify frequency scaling works when generating interrupts.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    _, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges, temp, frequency_scale=2.0
    )
    for param in params:
        assert param["freq"] >= 10, "Frequency should scale correctly (lower bound)"
        assert param["freq"] <= 30, "Frequency should scale correctly (upper bound)"


def test_generate_main_interrupt_amplitude_scaling(sample_time_vector, sample_interrupt_ranges):
    """
    Verify amplitude scaling works when generating interrupts.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    _, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges, temp, amplitude_scale=2.0
    )
    for param in params:
        assert param["amp"] >= 1.0, "Amplitude should scale correctly (lower bound)"
        assert param["amp"] <= 4.0, "Amplitude should scale correctly (upper bound)"
