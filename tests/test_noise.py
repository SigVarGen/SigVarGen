import numpy as np
import pytest
from SigVarGen import (
    calculate_noise_power,
    add_colored_noise,
    envelope_linear,
    envelope_sine,
    envelope_random_walk,
    envelope_blockwise,
    apply_time_shift 
)

# Noise tests generated with OpenAI o3-mini-high 

# -------------------------------------
# Tests for calculate_noise_power
# -------------------------------------

def test_calculate_noise_power_basic():
    """
    Verify that calculate_noise_power returns expected tuples
    for a given start, stop, and step in mV.
    """
    start_mV = 0
    stop_mV = 10
    step_mV = 5
    # Expected mV values: 0, 5, 10.
    # sigma_V = mV / 1000 and noise_power = sigma_V**2.
    expected = [
        (0, 0.0, 0.0),
        (5, 0.005, 0.005**2),
        (10, 0.01, 0.01**2)
    ]
    
    result = calculate_noise_power(start_mV, stop_mV, step_mV)
    assert len(result) == len(expected), "Unexpected number of entries returned."
    for res, exp in zip(result, expected):
        # Use np.allclose for floating point comparisons.
        assert res[0] == exp[0], "mV value mismatch."
        assert np.allclose(res[1], exp[1], atol=1e-8), "Sigma (V) value mismatch."
        assert np.allclose(res[2], exp[2], atol=1e-8), "Noise power value mismatch."

# -------------------------------------
# Tests for add_colored_noise
# -------------------------------------

@pytest.mark.parametrize("color", ["white", "pink", "brown"])
def test_add_colored_noise_basic(zero_wave, color):
    """
    Test that add_colored_noise produces an output of the same shape as the input.
    When the input is zero, the output should be purely the noise with RMS ~ sqrt(noise_power).
    """
    noise_power = 0.01  # variance
    npw = (0.8, 1.2)     # (not used in current code, but still provided)
    mf = (1.0, 1.0)      # fixed modulation factor (i.e. 1)
    
    res = add_colored_noise(zero_wave, noise_power, npw, mf, color=color, plot=False)
    assert res.shape == zero_wave.shape, "Output wave shape should match input wave shape."
    # Since input wave is zero, res equals noise. Its RMS should be approximately sqrt(noise_power).
    rms = np.sqrt(np.mean(res**2))
    expected_rms = np.sqrt(noise_power)
    assert np.isclose(rms, expected_rms, rtol=0.2), f"RMS of noise ({rms}) not within tolerance of expected ({expected_rms})."

def test_add_colored_noise_with_mod_envelope(zero_wave):
    """
    Test that when a modulation envelope is provided, the output differs from when it is not.
    Here we use envelope_linear as a simple, deterministic envelope.
    """
    noise_power = 0.01
    npw = (0.8, 1.2)
    mf = (1.0, 1.0)
    
    # Use envelope_linear as the modulating envelope.
    mod_env = {
        'func': envelope_linear,
        'param': (1,1)  
    }
    
    res_no_env = add_colored_noise(zero_wave, noise_power, npw, mf, color='pink', plot=False, mod_envelope=None)
    res_with_env = add_colored_noise(zero_wave, noise_power, npw, mf, color='pink', plot=False, mod_envelope=mod_env)
    
    # The two outputs should be different because the noise is multiplied by a non-constant envelope.
    assert not np.allclose(res_no_env, res_with_env), "Output with mod envelope should differ from without it."

# -------------------------------------
# Tests for envelope functions
# -------------------------------------

def test_envelope_linear():
    """
    Test that envelope_linear returns a linear ramp between the given npw bounds.
    """
    num_samples = 10
    npw_range = (0, 1)
    # param is not used for envelope_linear.
    env = envelope_linear(num_samples, npw_range, param=None)
    expected = np.linspace(npw_range[0], npw_range[1], num_samples)
    assert env.shape[0] == num_samples, "Envelope length mismatch."
    assert np.allclose(env, expected, atol=1e-8), "Envelope values do not match expected linear ramp."

def test_envelope_sine():
    """
    Test that envelope_sine returns an envelope of the correct shape and within the specified bounds.
    """
    np.random.seed(42)  # For reproducibility (affects apply_time_shift)
    num_samples = 100
    npw_range = (0, 1)
    param = 0.005
    env = envelope_sine(num_samples, npw_range, param=param)
    assert env.shape[0] == num_samples, "Envelope length mismatch."
    # Check that all envelope values are within [low, high]
    assert np.all(env >= npw_range[0] - 1e-8) and np.all(env <= npw_range[1] + 1e-8), "Envelope values exceed specified bounds."
    # Check that envelope is not constant
    assert np.ptp(env) > 0, "Envelope variation should be non-zero."

def test_envelope_random_walk():
    """
    Test that envelope_random_walk produces an envelope that starts at the midpoint and remains within bounds.
    """
    np.random.seed(123)  # For reproducibility
    num_samples = 50
    npw_range = (0, 1)
    param = 0.01
    env = envelope_random_walk(num_samples, npw_range, param=param)
    expected_start = (npw_range[0] + npw_range[1]) / 2.0
    assert env[0] == pytest.approx(expected_start), "Envelope should start at the midpoint."
    assert np.all(env >= npw_range[0]) and np.all(env <= npw_range[1]), "Envelope values should be within bounds."
    assert env.shape[0] == num_samples, "Envelope length mismatch."
    # Ensure variability
    assert np.ptp(env) > 0, "Envelope should vary over time."

def test_envelope_blockwise():
    """
    Test that envelope_blockwise returns an envelope with piecewise constant segments.
    """
    np.random.seed(456)  # For reproducibility
    num_samples = 55
    npw_range = (0, 1)
    block_size = 10 
    env = envelope_blockwise(num_samples, npw_range, param=block_size)
    assert env.shape[0] == num_samples, "Envelope length mismatch."
    
    # For each full block, check that all values are constant.
    n_full_blocks = num_samples // block_size
    for i in range(n_full_blocks):
        block = env[i*block_size:(i+1)*block_size]
        assert np.allclose(block, block[0], atol=1e-8), f"Block {i} is not constant."
    
    # Check remainder block (if any)
    remainder = num_samples % block_size
    if remainder > 0:
        block = env[n_full_blocks*block_size:]
        assert np.allclose(block, block[0], atol=1e-8), "Remainder block is not constant."
    
    # Check that each block's value is within the specified range.
    assert np.all(env >= npw_range[0]) and np.all(env <= npw_range[1]), "Envelope block values should be within bounds."
