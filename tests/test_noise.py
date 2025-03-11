import numpy as np
import pytest
from SigVarGen import (
    generate_noise_power,
    add_colored_noise,
    envelope_linear,
    envelope_sine,
    envelope_random_walk,
    envelope_blockwise,
    apply_time_shift 
)

# Noise tests generated with OpenAI o3-mini-high 

# -------------------------------------
# Tests for generate_noise_power
# -------------------------------------

def test_generate_noise_power_range():
    """
    Verify that generate_noise_power returns noise power within a reasonable range 
    and that the SNR value is correctly selected from the provided range.
    """
    # Create a synthetic signal with unit variance
    wave = np.random.randn(1000)  # Normal distribution with mean=0, std=1
    
    # Define an SNR range
    snr_range = (-40, -10)  # Typical range for signal processing

    # Generate noise power with random SNR
    noise_power, snr_used = generate_noise_power(wave, snr_range)

    # Ensure SNR is within the expected range
    assert snr_range[0] <= snr_used <= snr_range[1], "SNR is outside the expected range"

    # Compute expected noise standard deviation based on selected SNR
    expected_noise_fraction = 10 ** (-snr_used / 20)
    expected_sigma_V = np.std(wave) * expected_noise_fraction
    expected_noise_power = expected_sigma_V ** 2

    # Ensure noise power is close to the expected computed value
    assert np.allclose(noise_power, expected_noise_power, atol=1e-8), "Noise power calculation is incorrect"

def test_generate_noise_power_zero_signal():
    """
    Verify behavior when the input signal has zero variance.
    """
    wave = np.zeros(1000)  # Zero-variance signal

    # Define an SNR range
    snr_range = (-40, -10)

    # Generate noise power
    noise_power, snr_used = generate_noise_power(wave, snr_range)

    # Ensure noise power is zero since signal_std should be zero
    assert noise_power == 0.0, "Noise power should be zero for a zero-variance signal"

def test_generate_noise_power_fixed_snr():
    """
    Check correctness when SNR is fixed at a known value.
    """
    wave = np.random.randn(1000)  # Random normal signal
    fixed_snr = -30  # Fixed SNR in dB
    snr_range = (fixed_snr, fixed_snr)  # SNR is not random, fixed at -30 dB

    # Generate noise power
    noise_power, snr_used = generate_noise_power(wave, snr_range)

    # Ensure SNR is exactly -30 dB
    assert snr_used == fixed_snr, "SNR does not match the fixed value"

    # Compute expected noise power
    expected_noise_fraction = 10 ** (-fixed_snr / 20)
    expected_sigma_V = np.std(wave) * expected_noise_fraction
    expected_noise_power = expected_sigma_V ** 2

    # Validate computed noise power
    assert np.allclose(noise_power, expected_noise_power, atol=1e-8), "Noise power calculation is incorrect for fixed SNR"


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
    
    res, _ = add_colored_noise(zero_wave, noise_power, npw, mf, color=color)
    assert res.shape == zero_wave.shape, "Output wave shape should match input wave shape."
    # Since input wave is zero, res equals noise. Its RMS should be approximately sqrt(noise_power).
    rms = np.mean(res**2)
    expected_rms = noise_power
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
    
    res_no_env, _ = add_colored_noise(zero_wave, noise_power, npw, mf, color='pink', mod_envelope=None)
    res_with_env, _ = add_colored_noise(zero_wave, noise_power, npw, mf, color='pink', mod_envelope=mod_env)
    
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
    env = envelope_linear(num_samples, npw_range, param=True)
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
