import numpy as np
import pytest
from SigVarGen import generate_signal
from SigVarGen import (
    get_non_overlapping_interval,
    place_interrupt,
    blend_signal,
    apply_interrupt_modifications,
    generate_main_interrupt,
    add_main_interrupt,
    add_smaller_interrupts,
    add_interrupt_with_params,
    add_interrupt_bursts
)

# -------------------------------------
# Tests for get_non_overlapping_interval
# -------------------------------------

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
    result = get_non_overlapping_interval(1000, 50, occupied, buffer=100)

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

# -------------------------------------
# --- Tests for place_interrupt ---
# -------------------------------------

def test_place_interrupt_non_overlap(sample_signal_length):
    """
    Ensure place_interrupt finds a non-overlapping interval when non_overlap=True.
    """
    occupied = [(100, 200)]
    result = place_interrupt(sample_signal_length, 0.05, occupied, non_overlap=True, buffer=100)

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

# -------------------------------------
# --- Tests for blend_signal ---
# -------------------------------------

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

# -------------------------------------
# Tests for apply_interrupt_modifications
# -------------------------------------

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

# -------------------------------------
# Tests for generate_main_interrupt
# -------------------------------------

def test_generate_main_interrupt(sample_time_vector, sample_interrupt_ranges_drop):
    """
    Verify generated interrupt has correct shape and expected number of sinusoids.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    interrupt_signal, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges_drop, temp, n_sinusoids=5
    )
    assert interrupt_signal.shape == t.shape, "Generated signal shape should match time vector shape"
    assert len(params) == 5, "Number of sinusoid parameters should match requested n_sinusoids"
    assert all(key in params[0] for key in ["amp", "freq", "phase"]), "Each sinusoid should have amp, freq, phase"


def test_generate_main_interrupt_frequency_scaling(sample_time_vector, sample_interrupt_ranges_drop):
    """
    Verify frequency scaling works when generating interrupts.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    _, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges_drop, temp, frequency_scale=2.0
    )
    for param in params:
        assert param["freq"] >= 5, "Frequency should scale correctly (lower bound)"
        assert param["freq"] <= 15, "Frequency should scale correctly (upper bound)"


def test_generate_main_interrupt_amplitude_scaling(sample_time_vector, sample_interrupt_ranges_drop):
    """
    Verify amplitude scaling works when generating interrupts.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"
    _, params = generate_main_interrupt(
        t, domain, sample_interrupt_ranges_drop, temp, amplitude_scale=2.0
    )
    for param in params:
        assert param["amp"] >= 0.2, "Amplitude should scale correctly (lower bound)"
        assert param["amp"] <= 1.0, "Amplitude should scale correctly (upper bound)"

# -------------------------------------
# --- Tests for add_main_interrupt ---
# -------------------------------------

def test_add_main_interrupt_basic(sample_time_vector, sample_device_params, sample_interrupt_ranges_rise):
    """
    Test that add_main_interrupt successfully modifies the base signal and returns appropriate metadata.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params, occupied_intervals = add_main_interrupt(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        temp=temp,
        duration_ratio=0.1,
        disperse=False,
        drop=False,
        n_sinusoids=3,
        non_overlap=True
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert len(interrupt_params) == 1, "Should generate exactly one main interrupt"
    assert len(occupied_intervals) == 1, "One interval should be marked as occupied"

    interrupt = interrupt_params[0]
    assert interrupt['type'] == 'main', "Interrupt type should be 'main'"
    assert interrupt['start_idx'] >= 0, "Start index should be within signal bounds"
    assert interrupt['duration_idx'] > 0, "Interrupt duration should be positive"
    assert 'sinusoids_params' in interrupt, "Sinusoid params should be recorded"

def test_add_main_interrupt_with_dispersal(sample_time_vector, sample_device_params, sample_interrupt_ranges_rise):
    """
    Test the behavior when disperse=True.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params, occupied_intervals = add_main_interrupt(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        temp=temp,
        duration_ratio=0.1,
        disperse=True,
        drop=False,
        n_sinusoids=3,
        non_overlap=True
    )

    assert len(interrupt_params) == 1, "Main interrupt should still be created"
    assert np.any(modified_signal != base_signal), "Signal should be modified with dispersed content"

def test_add_main_interrupt_with_drop(sample_time_vector, sample_device_params, sample_interrupt_ranges_drop):
    """
    Test the behavior when drop=True (interrupt drops below baseline).
    """
    t = sample_time_vector
    base_signal = np.ones_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params, occupied_intervals = add_main_interrupt(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_drop,
        temp=temp,
        duration_ratio=0.1,
        disperse=False,
        drop=True,
        n_sinusoids=3,
        non_overlap=True
    )

    assert np.min(modified_signal) < np.min(base_signal), "Signal should drop below baseline when drop=True"
    assert len(interrupt_params) == 1, "Main interrupt should be created"
    assert interrupt_params[0]['type'] == 'main', "Interrupt should be classified as 'main'"

def test_add_main_interrupt_with_complex_iter(sample_time_vector, sample_device_params, sample_interrupt_ranges_rise):
    """
    Test behavior when complex_iter > 0 (additional overlapping interrupts).
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params, occupied_intervals = add_main_interrupt(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        temp=temp,
        duration_ratio=0.1,
        disperse=False,
        drop=False,
        n_sinusoids=3,
        non_overlap=True,
        complex_iter=2
    )

    assert len(interrupt_params) == 3, "Should generate 1 main and 2 complex interrupts"
    assert any(p['type'] == 'main' for p in interrupt_params), "At least one should be a main interrupt"
    assert all('sinusoids_params' in p for p in interrupt_params), "Each interrupt should have sinusoid parameters"
    assert np.any(modified_signal != base_signal), "Signal should be modified"

# -------------------------------------
# Tests for add_smaller_interrupts
# -------------------------------------

def test_add_smaller_interrupts_basic(sample_time_vector, sample_interrupt_ranges_rise):
    """
    Test adding a small interrupt to an empty signal.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"
    occupied_intervals = []

    modified_signal, interrupt_params = add_smaller_interrupts(
        t=t,
        base_signal=base_signal.copy(),
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        domain=domain,
        temp=temp,
        n_smaller_interrupts=1,
        occupied_intervals=occupied_intervals,
        disperse=False,
        drop=False,
        small_duration_ratio=0.05,
        n_sinusoids=3,
        non_overlap=True
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert len(interrupt_params) == 1, "Exactly one small interrupt should be added"
    assert len(occupied_intervals) == 1, "One interval should be occupied"
    assert interrupt_params[0]['type'] == 'small', "Interrupt should be classified as 'small'"

def test_add_smaller_interrupts_no_space(sample_time_vector, sample_interrupt_ranges_rise):
    """
    Test adding interrupts when no space is available.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"
    occupied_intervals = [(0, len(t) - 1)]  # Entire signal occupied

    modified_signal, interrupt_params = add_smaller_interrupts(
        t=t,
        base_signal=base_signal.copy(),
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        domain=domain,
        temp=temp,
        n_smaller_interrupts=1,
        occupied_intervals=occupied_intervals,
        disperse=False,
        drop=False,
        small_duration_ratio=0.1,
        n_sinusoids=3,
        non_overlap=True
    )

    assert np.array_equal(modified_signal, base_signal), "Signal should remain unchanged when no space is available"
    assert interrupt_params == [], "No interrupts should be created"
    assert len(occupied_intervals) == 1, "Occupied intervals should remain unchanged"

def test_add_smaller_interrupts_with_dispersal(sample_time_vector, sample_interrupt_ranges_rise):
    """
    Test adding smaller interrupts with dispersal (adds noise-like components).
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"
    occupied_intervals = []

    modified_signal, interrupt_params = add_smaller_interrupts(
        t=t,
        base_signal=base_signal.copy(),
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        domain=domain,
        temp=temp,
        n_smaller_interrupts=1,
        occupied_intervals=occupied_intervals,
        disperse=True,
        drop=False,
        small_duration_ratio=0.05,
        n_sinusoids=3,
        non_overlap=True
    )

    assert len(interrupt_params) == 1, "One small interrupt should be added"
    assert np.any(modified_signal != base_signal), "Signal should be modified by the interrupt"

def test_add_smaller_interrupts_with_drop(sample_time_vector, sample_interrupt_ranges_drop):
    """
    Test adding smaller interrupts with drop=True (lowering signal below baseline).
    """
    t = sample_time_vector
    base_signal = np.ones_like(t)
    domain = "DeviceA"
    temp = "low"
    occupied_intervals = []

    modified_signal, interrupt_params = add_smaller_interrupts(
        t=t,
        base_signal=base_signal.copy(),
        INTERRUPT_RANGES=sample_interrupt_ranges_drop,
        domain=domain,
        temp=temp,
        n_smaller_interrupts=1,
        occupied_intervals=occupied_intervals,
        disperse=False,
        drop=True,
        small_duration_ratio=0.05,
        n_sinusoids=3,
        non_overlap=True
    )

    assert np.min(modified_signal) < np.min(base_signal), "Signal should drop below baseline when drop=True"
    assert len(interrupt_params) == 1, "One small interrupt should be added"
    assert interrupt_params[0]['type'] == 'small', "Interrupt should be classified as 'small'"

def test_add_multiple_smaller_interrupts(sample_time_vector, sample_interrupt_ranges_rise):
    """
    Test adding multiple smaller interrupts.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"
    occupied_intervals = []

    modified_signal, interrupt_params = add_smaller_interrupts(
        t=t,
        base_signal=base_signal.copy(),
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        domain=domain,
        temp=temp,
        n_smaller_interrupts=3,
        occupied_intervals=occupied_intervals,
        disperse=False,
        drop=False,
        small_duration_ratio=0.05,
        n_sinusoids=3,
        non_overlap=True
    )

    assert len(interrupt_params) == 3, "Three smaller interrupts should be added"
    assert len(occupied_intervals) == 3, "Three intervals should be occupied"
    assert all(p['type'] == 'small' for p in interrupt_params), "All interrupts should be classified as 'small'"

# -------------------------------------
# Tests for add_interrupt_with_params
# -------------------------------------

def test_add_interrupt_with_params_basic(sample_time_vector, sample_device_params, sample_interrupt_ranges_drop):
    """
    Test basic execution of add_interrupt_with_params with all defaults.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params = add_interrupt_with_params(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_drop,
        temp=temp
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert len(interrupt_params) >= 1, "At least one main interrupt should be added"
    assert all('start_idx' in p and 'duration_idx' in p for p in interrupt_params), "Each interrupt should have basic metadata"
    assert any(p['type'] == 'main' for p in interrupt_params), "There should be exactly one main interrupt"
    assert all(p['type'] in ['main', 'small'] for p in interrupt_params), "Interrupt types should be 'main' or 'small'"

def test_add_interrupt_with_params_with_custom_values(sample_time_vector, sample_device_params, sample_interrupt_ranges_rise):
    """
    Test add_interrupt_with_params using custom duration and smaller interrupts count.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    modified_signal, interrupt_params = add_interrupt_with_params(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_rise,
        drop=False,
        temp=temp,
        duration_ratio=0.1,
        n_smaller_interrupts=2,
        non_overlap=True,
        complex_iter=1
    )

    assert len(interrupt_params) >= 1, "At least one main interrupt should be added"
    assert any(p['type'] == 'main' for p in interrupt_params), "One main interrupt should be present"
    assert len([p for p in interrupt_params if p['type'] == 'small']) == 2, "Should have exactly 2 smaller interrupts"

def test_add_interrupt_with_params_long_response(sample_time_vector, sample_device_params, sample_interrupt_ranges_drop):
    """
    Test behavior when the entire signal is pre-occupied.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    # Block the entire signal length to simulate no space available.
    modified_signal, interrupt_params = add_interrupt_with_params(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        INTERRUPT_RANGES=sample_interrupt_ranges_drop,
        temp=temp,
        duration_ratio=1.5,  # Long placement
        non_overlap=True,
        n_smaller_interrupts=2
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert len(interrupt_params) == 1, "Only one interrupt should be added"

# -------------------------------------
# --- Tests for add_interrupt_bursts ---
# -------------------------------------

def test_add_interrupt_bursts_with_drop_range(sample_time_vector, sample_device_params, sample_interrupt_ranges_drop):
    """
    Test adding small interrupt bursts using the 'drop' range and validate clipping to device limits.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    device_min = sample_interrupt_ranges_drop[domain]['amplitude'][0]
    device_max = sample_device_params[domain]['amplitude'][1]

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified when bursts are added"

    # Check amplitude boundaries (device-level limits)
    assert np.min(modified_signal) >= device_min, f"Signal should not go below device minimum {device_min}"
    assert np.max(modified_signal) <= device_max, f"Signal should not exceed device maximum {device_max}"


def test_add_interrupt_bursts_with_rise_range(sample_time_vector, sample_device_params, sample_interrupt_ranges_rise):
    """
    Test adding small interrupt bursts using the 'rise' range and validate clipping to device limits.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "high"

    device_min = sample_device_params[domain]['amplitude'][0]
    device_max = sample_interrupt_ranges_rise[domain]['amplitude'][1]

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Signal should be modified when bursts are added"

    # Check amplitude boundaries (device-level limits)
    assert np.min(modified_signal) >= device_min, f"Signal should not go below device minimum {device_min}"
    assert np.max(modified_signal) <= device_max, f"Signal should not exceed device maximum {device_max}"


def test_add_interrupt_bursts_with_window(sample_time_vector, sample_device_params):
    """
    Test adding bursts within a specified time window.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    device_min = 0
    device_max = 10

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp,
        start_idx=200,
        end_idx=800
    )

    # Check that only the specified region has changed
    assert np.all(modified_signal[:200] == base_signal[:200]), "Before start_idx should be unchanged"
    assert np.all(modified_signal[800:] == base_signal[800:]), "After end_idx should be unchanged"
    assert np.any(modified_signal[200:800] != base_signal[200:800]), "Only the specified window should be affected"

def test_add_interrupt_bursts_with_high_base_signal(sample_time_vector, sample_device_params):
    """
    Test adding bursts on top of a high-amplitude base signal.
    """
    t = sample_time_vector
    domain = "DeviceA"
    temp = "low"

    device_min = 0
    device_max = sample_device_params[domain]['amplitude'][1]

    # Pre-fill base signal near the upper device boundary
    base_signal = np.ones_like(t) * (0.8 * device_max)

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp
    )

    assert modified_signal.shape == base_signal.shape, "Signal length should remain unchanged"
    assert np.any(modified_signal != base_signal), "Base signal should be modified when bursts are added"

    # Validate boundaries (device-level limits)
    assert np.min(modified_signal) >= device_min, f"Signal should not go below device minimum {device_min}"
    assert np.max(modified_signal) <= device_max, f"Signal should not exceed device maximum {device_max}"


def test_add_interrupt_bursts_with_no_interrupts(sample_time_vector, sample_device_params):
    """
    Test adding zero bursts (edge case).
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    device_min = 0
    device_max = 10

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp,
        n_small_interrupts=0
    )

    assert np.array_equal(modified_signal, base_signal), "Signal should remain unchanged if no interrupts are added"

def test_add_interrupt_bursts_non_overlap_enforced(sample_time_vector, sample_device_params):
    """
    Test that small interrupts placed within a window respect non_overlap=True.
    """
    t = sample_time_vector
    base_signal = np.zeros_like(t)
    domain = "DeviceA"
    temp = "low"

    device_min, device_max = sample_device_params[domain]['amplitude']

    # Define a narrow window for placement, so overlap risk increases
    start_idx, end_idx = 400, 600

    modified_signal = add_interrupt_bursts(
        t=t,
        base_signal=base_signal.copy(),
        domain=domain,
        DEVICE_RANGES=sample_device_params,
        device_min=device_min,
        device_max=device_max,
        temp=temp,
        start_idx=start_idx,
        end_idx=end_idx,
        n_small_interrupts=10,  # High count to force overlap checking
        non_overlap=True
    )

    # Extract placed intervals to check for overlaps
    placed_intervals = []
    for i in range(start_idx, end_idx):
        if modified_signal[i] != base_signal[i]:
            if not placed_intervals or placed_intervals[-1][1] != i - 1:
                placed_intervals.append([i, i])
            else:
                placed_intervals[-1][1] = i

    # Ensure no overlaps (gaps between all placed intervals when non_overlap=True)
    for (prev_end, next_start) in zip(placed_intervals[:-1], placed_intervals[1:]):
        assert next_start[0] - prev_end[1] > 0, "Intervals should not overlap when non_overlap=True"

    # Ensure final signal is within device limits
    assert np.min(modified_signal) >= device_min, f"Signal should not go below device minimum {device_min}"
    assert np.max(modified_signal) <= device_max, f"Signal should not exceed device maximum {device_max}"
