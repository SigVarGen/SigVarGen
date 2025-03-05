import numpy as np
import pytest
from SigVarGen import (
    apply_baseline_drift_region,
    apply_baseline_drift_polynomial,
    apply_baseline_drift_piecewise,
    apply_baseline_drift_quadratic,
    apply_baseline_drift_middle_peak,
)

def test_apply_baseline_drift_region_basic(sample_wave):
    """
    Test basic application of regional linear drift.
    """
    max_drift = 5.0
    modified_wave = apply_baseline_drift_region(sample_wave.copy(), max_drift)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by the drift"

    start_idx = int(0.3 * len(sample_wave))
    end_idx = int(0.7 * len(sample_wave))

    assert np.all(modified_wave[:start_idx] == sample_wave[:start_idx]), "Outside drift region should be unchanged"
    assert np.any(modified_wave[start_idx:end_idx] != sample_wave[start_idx:end_idx]), "Drift region should be modified"


def test_apply_baseline_drift_polynomial_basic(sample_wave):
    """
    Test polynomial drift application.
    """
    max_drift = 3.0
    modified_wave = apply_baseline_drift_polynomial(sample_wave.copy(), max_drift)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by polynomial drift"

def test_apply_baseline_drift_polynomial_reversed(sample_wave):
    """
    Test polynomial drift with reversed=True.
    """
    max_drift = 3.0
    modified_wave = apply_baseline_drift_polynomial(sample_wave.copy(), max_drift, reversed=True)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified when reversed=True"

def test_apply_baseline_drift_piecewise_basic(sample_wave):
    """
    Test piecewise drift with default segments.
    """
    max_drift = 4.0
    modified_wave = apply_baseline_drift_piecewise(sample_wave.copy(), max_drift)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by piecewise drift"

def test_apply_baseline_drift_piecewise_reversed(sample_wave):
    """
    Test piecewise drift with reversed=True.
    """
    max_drift = 4.0
    modified_wave = apply_baseline_drift_piecewise(sample_wave.copy(), max_drift, reversed=True)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified when reversed=True"

def test_apply_baseline_drift_piecewise_custom_pieces(sample_wave):
    """
    Test piecewise drift with non-default piece count.
    """
    max_drift = 4.0
    modified_wave = apply_baseline_drift_piecewise(sample_wave.copy(), max_drift, num_pieces=5)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified when num_pieces=5"

def test_apply_baseline_drift_quadratic_basic(sample_wave):
    """
    Test quadratic drift application.
    """
    max_drift = 6.0
    modified_wave = apply_baseline_drift_quadratic(sample_wave.copy(), max_drift)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by quadratic drift"

def test_apply_baseline_drift_quadratic_reversed(sample_wave):
    """
    Test quadratic drift with reversed=True.
    """
    max_drift = 6.0
    normal_wave = apply_baseline_drift_quadratic(sample_wave.copy(), max_drift, reversed=False)
    reversed_wave = apply_baseline_drift_quadratic(sample_wave.copy(), max_drift, reversed=True)

    assert normal_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(normal_wave != sample_wave), "Normal drift should modify wave"
    assert np.any(reversed_wave != sample_wave), "Reversed drift should modify wave"

    # In normal drift, final value is at the end; in reversed, final value is at the start.
    assert reversed_wave[0] != sample_wave[0], "Reversed drift should modify the start of the wave"
    assert normal_wave[-1] != sample_wave[-1], "Normal drift should modify the end of the wave"

    # The reversed drift should trend down toward the end (closer to 0)
    assert reversed_wave[-1] == pytest.approx(sample_wave[-1], abs=1e-5), "Reversed drift should decay back to baseline at the end"


def test_apply_baseline_drift_middle_peak_up(sample_wave):
    """
    Test middle peak drift, upward direction.
    """
    max_drift = 5.0
    modified_wave = apply_baseline_drift_middle_peak(sample_wave.copy(), max_drift, direction='up')

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by middle peak drift"

    mid_idx = len(sample_wave) // 2
    assert modified_wave[mid_idx] > sample_wave[mid_idx], "Upward drift should raise the middle of the wave"


def test_apply_baseline_drift_middle_peak_down(sample_wave):
    """
    Test middle peak drift, downward direction.
    """
    max_drift = 5.0
    modified_wave = apply_baseline_drift_middle_peak(sample_wave.copy(), max_drift, direction='down')

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by middle peak drift"

    mid_idx = len(sample_wave) // 2
    assert modified_wave[mid_idx] < sample_wave[mid_idx], "Downward drift should lower the middle of the wave"

    # The ends should remain close to the original baseline
    assert modified_wave[0] == pytest.approx(sample_wave[0], abs=1e-5), "Drift should return to baseline at the start"
    assert modified_wave[-1] == pytest.approx(sample_wave[-1], abs=1e-5), "Drift should return to baseline at the end"


def test_apply_baseline_drift_middle_peak_empty():
    """
    Edge case: empty wave should remain unchanged.
    """
    empty_wave = np.array([])
    max_drift = 5.0
    modified_wave = apply_baseline_drift_middle_peak(empty_wave, max_drift)

    assert modified_wave.size == 0, "Empty wave should remain unchanged"

def test_apply_baseline_drift_middle_peak_min_drift(sample_wave):
    """
    Test middle peak drift with non-zero minimum drift.
    """
    max_drift = 5.0
    min_drift = 2.0
    modified_wave = apply_baseline_drift_middle_peak(sample_wave.copy(), max_drift, min_drift=min_drift)

    assert np.min(modified_wave) <= -min_drift, "Minimum drift should be respected in downward direction"

def test_apply_baseline_drift_region_no_effect_outside_region(sample_wave):
    """
    Check that outside the specified region, the wave remains unchanged.
    """
    max_drift = 5.0
    modified_wave = apply_baseline_drift_region(sample_wave.copy(), max_drift, start_frac=0.2, end_frac=0.8)

    assert np.all(modified_wave[:200] == sample_wave[:200]), "First 20% should remain unchanged"
    assert np.all(modified_wave[800:] == sample_wave[800:]), "Last 20% should remain unchanged"
    assert np.any(modified_wave[200:800] != sample_wave[200:800]), "Central region should be modified"

def test_apply_baseline_drift_polynomial_custom_order(sample_wave):
    """
    Test polynomial drift with a non-default polynomial order.
    """
    max_drift = 4.0
    modified_wave = apply_baseline_drift_polynomial(sample_wave.copy(), max_drift, order=3)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert np.any(modified_wave != sample_wave), "Wave should be modified by polynomial drift"

