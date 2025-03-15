import pytest
import numpy as np

from SigVarGen.utils import generate_device_parameters, calculate_ED, calculate_SNR, interpoling, normalization

def test_basic_split(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratio=0.5)

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
    lower, upper = generate_device_parameters(sample_device_params, drop=True, split_ratio=0.5)

    # Amplitudes should be reversed
    assert lower["DeviceA"]["amplitude"] == (5, 10)
    assert upper["DeviceA"]["amplitude"] == (0, 5)

    assert lower["DeviceB"]["amplitude"] == (10, 15)
    assert upper["DeviceB"]["amplitude"] == (5, 10)

def test_full_split_to_lower(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratio=0.0)

    # Lower should get the full range, upper should be minimal
    assert lower["DeviceA"]["amplitude"] == (0, 0)
    assert upper["DeviceA"]["amplitude"] == (0, 10)

def test_full_split_to_upper(sample_device_params):
    lower, upper = generate_device_parameters(sample_device_params, drop=False, split_ratio=1.0)

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
        generate_device_parameters({}, split_ratio=-0.1)

    with pytest.raises(ValueError):
        generate_device_parameters({}, split_ratio=1.1)


def test_euclidean_distance():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    result = calculate_ED(x, y)
    assert result == pytest.approx(5.196, rel=1e-3)

import numpy as np
import pytest
from SigVarGen.utils import calculate_SNR, interpoling, normalization

def test_calculate_SNR():
    signal = np.ones(100)
    noisy_signal = signal + np.random.normal(0, 0.1, size=100)
    cp = calculate_SNR(signal, noisy_signal)
    assert cp > 0  # Basic check: CP should be > 0 if noise is present but signal dominates

def test_interpoling():
    res = np.array([0, 1, 2, 3])
    interpolated = interpoling(res, target_len=10)
    assert len(interpolated) == 10  # Ensure target length is correct

def test_normalization():
    signal = np.array([1, 2, 3, 4, 5])
    norm_signal = normalization(signal)
    assert np.isclose(np.mean(norm_signal), 0, atol=1e-5)
    assert np.isclose(np.std(norm_signal), 1, atol=1e-5)
