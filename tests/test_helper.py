import pytest
import numpy as np

from SigVarGen.helper import generate_device_parameters, calculate_ED, calculate_SNR, interpoling, normalization, randomize_trace


# -------------------------------------
# Tests for generate_device_parameters 
# -------------------------------------

def test_basic_split(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratios=[0.5,0.5])

    # Amplitude should be split in half
    assert lower["DeviceA"]["amplitude"] == (0, 5)
    assert upper["DeviceA"]["amplitude"] == (5, 10)

    assert lower["DeviceB"]["amplitude"] == (5, 10)
    assert upper["DeviceB"]["amplitude"] == (10, 15)

    # Frequencies should follow amplitude split
    assert lower["DeviceA"]["frequency"]["low"] == (100, 150)
    assert upper["DeviceA"]["frequency"]["low"] == (150, 200)

    assert lower["DeviceB"]["frequency"] == (50, 100)
    assert upper["DeviceB"]["frequency"] == (100, 150)

def test_drop_param(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=True, split_ratios=[0.5,0.5])

    # Amplitudes should be reversed
    assert lower["DeviceA"]["amplitude"] == (5, 10)
    assert upper["DeviceA"]["amplitude"] == (0, 5)

    assert lower["DeviceB"]["amplitude"] == (10, 15)
    assert upper["DeviceB"]["amplitude"] == (5, 10)

def test_full_split_to_lower(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratios=[0.0,1.0])

    # Lower should get the full range, upper should be minimal
    assert lower["DeviceA"]["amplitude"] == (0, 0)
    assert upper["DeviceA"]["amplitude"] == (0, 10)

def test_full_split_to_upper(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratios=[1.0,0.0])

    # Upper should get the full range, lower should be minimal
    assert lower["DeviceA"]["amplitude"] == (0, 10)
    assert upper["DeviceA"]["amplitude"] == (10, 10)

def test_frequency_follows_amplitude_false(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, frequency_follows_amplitude=False)

    # Frequencies should remain the same in both
    assert lower["DeviceA"]["frequency"]["low"] == (100, 200)
    assert upper["DeviceA"]["frequency"]["low"] == (100, 200)

def test_invalid_split_ratio():
    with pytest.raises(ValueError):
        generate_device_parameters({}, split_ratios=[0.3,0.2])

    with pytest.raises(ValueError):
        generate_device_parameters({}, split_ratios=[0.5,0.7])


# -------------------------------------
# --- Tests for calculate_ED ---
# -------------------------------------

def test_euclidean_distance():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    result = calculate_ED(x, y)
    assert result == pytest.approx(5.196, rel=1e-3)

# -------------------------------------
# --- Tests for calculate_SNR ---
# -------------------------------------

def test_calculate_SNR():
    signal = np.ones(100)
    noisy_signal = signal + np.random.normal(0, 0.1, size=100)
    cp = calculate_SNR(signal, noisy_signal)
    assert cp > 0  # Basic check: CP should be > 0 if noise is present but signal dominates

# -------------------------------------
# --- Tests for interpoling ---
# -------------------------------------

def test_interpoling():
    res = np.array([0, 1, 2, 3])
    interpolated = interpoling(res, target_len=10)
    assert len(interpolated) == 10  # Ensure target length is correct


# -------------------------------------
# --- Tests for normalization ---
# -------------------------------------

def test_normalization():
    signal = np.array([1, 2, 3, 4, 5])
    norm_signal = normalization(signal)
    assert np.isclose(np.mean(norm_signal), 0, atol=1e-5)
    assert np.isclose(np.std(norm_signal), 1, atol=1e-5)

# -------------------------------------
# --- Tests for randomize_trace ---
# -------------------------------------

def test_randomize_trace_mean_only(sample_wave):
    """
    Test that only mean is changed when adjust_var=False.
    """
    result = randomize_trace(
        sample_wave,
        adjust_mean=True,
        mean_min=5.0,
        mean_max=10.0,
        mean_std=1.0,
        adjust_var=False
    )
    mean = np.mean(result)
    assert 5.0 <= mean <= 10.0, f"Mean {mean} not within expected range."


def test_randomize_trace_variance_only(sample_wave):
    """
    Test that only variance is changed when adjust_mean=False.
    """
    result = randomize_trace(
        sample_wave,
        adjust_mean=False,
        adjust_var=True,
        var_mean=None,  # These will be internally replaced inside function
        var_min=0.5,
        var_max=1.5,
        var_std=0.2
    )
    variance = np.var(result)
    assert 0.5 <= variance <= 1.5, f"Variance {variance} not within expected range."


def test_randomize_trace_mean_and_var(sample_wave):
    """
    Test that both mean and variance are adjusted.
    """
    result = randomize_trace(
        sample_wave,
        adjust_mean=True,
        mean_min=-2.0,
        mean_max=2.0,
        mean_std=0.5,
        adjust_var=True,
        var_mean=None,
        var_min=0.1,
        var_max=0.5,
        var_std=0.05
    )
    mean = np.mean(result)
    variance = np.var(result)
    assert -2.0 <= mean <= 2.0, f"Mean {mean} not within expected range."
    assert 0.1 <= variance <= 0.5, f"Variance {variance} not within expected range."


def test_randomize_trace_raises_error_on_missing_params(sample_wave):
    """
    Test that ValueError is raised if required parameters are missing.
    """
    with pytest.raises(ValueError):
        # Missing mean_min, mean_max, mean_std
        randomize_trace(
            sample_wave,
            adjust_mean=True,
            adjust_var=False
        )

    with pytest.raises(ValueError):
        # Missing var_min, var_max, var_std
        randomize_trace(
            sample_wave,
            adjust_mean=False,
            adjust_var=True
        )
