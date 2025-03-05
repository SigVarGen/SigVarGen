import numpy as np
import pytest
from SigVarGen import (
    apply_time_shift,
    apply_time_warp,
    apply_gain_variation,
    apply_amplitude_modulation,
    apply_baseline_drift,
    apply_amplitude_modulation_region,
    apply_nonlinear_distortion,
    apply_quantization_noise,
    transform_wave_with_score, generate_signal
)

def test_apply_time_shift(sample_wave):
    """
    Test time shift applies circular shift within bounds.
    """
    max_shift = 50
    shifted_wave = apply_time_shift(sample_wave, max_shift)

    assert shifted_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(shifted_wave, sample_wave), "Wave should be modified by time shift"


def test_apply_time_warp(sample_wave, sample_time_vector):
    """
    Test time warping modifies the wave.
    """
    warped_wave = apply_time_warp(
        sample_wave.copy(),
        max_warp_factor=0.1,
        t=sample_time_vector,
        n_sinusoids=5,
        amplitude_range=(0.1, 1.0),
        base_frequency_range=(10, 100)
    )

    assert warped_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(warped_wave, sample_wave), "Wave should be modified by time warp"


def test_apply_gain_variation(sample_wave):
    """
    Test gain variation applies scaling to wave.
    """
    max_gain_variation = 0.3
    modified_wave = apply_gain_variation(sample_wave, max_gain_variation)

    assert modified_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(modified_wave, sample_wave), "Wave should be modified by gain variation"


def test_apply_amplitude_modulation(sample_wave):
    """
    Test amplitude modulation applies periodic gain.
    """
    modulation_depth = 0.5
    modulated_wave = apply_amplitude_modulation(sample_wave, modulation_depth)

    assert modulated_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(modulated_wave, sample_wave), "Wave should be modulated"


def test_apply_baseline_drift(sample_wave):
    """
    Test linear baseline drift is applied.
    """
    max_drift = 0.5
    drifted_wave = apply_baseline_drift(sample_wave.copy(), max_drift)

    assert drifted_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(drifted_wave, sample_wave), "Wave should be modified by baseline drift"


def test_apply_baseline_drift_reversed(sample_wave):
    """
    Test reversed baseline drift starts high and returns to baseline.
    """
    max_drift = 0.5
    drifted_wave = apply_baseline_drift(sample_wave.copy(), max_drift, reversed=True)

    assert drifted_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(drifted_wave, sample_wave), "Wave should be modified by reversed drift"
    assert drifted_wave[0] != sample_wave[0], "Reversed drift should modify the start"
    assert drifted_wave[-1] == pytest.approx(sample_wave[-1], abs=1e-5), "Reversed drift should return to baseline at the end"


def test_apply_amplitude_modulation_region(sample_wave):
    """
    Test regional amplitude modulation only modifies the specified range.
    """
    modulated_wave = apply_amplitude_modulation_region(sample_wave.copy(), 0.5, f_min=0.3, f_max=0.7)

    assert modulated_wave.shape == sample_wave.shape, "Wave length should remain unchanged"

    start_idx = int(0.3 * len(sample_wave))
    end_idx = int(0.7 * len(sample_wave))

    # Before and after region should be the same
    assert np.array_equal(modulated_wave[:start_idx], sample_wave[:start_idx]), "Before modulated region should be unchanged"
    assert np.array_equal(modulated_wave[end_idx:], sample_wave[end_idx:]), "After modulated region should be unchanged"
    
    # Check modification within region
    assert not np.array_equal(modulated_wave[start_idx:end_idx], sample_wave[start_idx:end_idx]), "Region should be modulated"


def test_apply_nonlinear_distortion(sample_wave):
    """
    Test nonlinear distortion applies tanh transformation.
    """
    distortion_level = 2.0
    distorted_wave = apply_nonlinear_distortion(sample_wave.copy(), distortion_level)

    assert distorted_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(distorted_wave, sample_wave), "Wave should be modified by distortion"

    # Check that values are compressed toward -1 and 1 (effect of tanh)
    assert np.max(distorted_wave) <= 1.0, "Tanh distortion should compress within [-1, 1]"
    assert np.min(distorted_wave) >= -1.0, "Tanh distortion should compress within [-1, 1]"


def test_apply_quantization_noise(sample_wave):
    """
    Test quantization reduces precision.
    """
    num_bits = 4
    quantized_wave = apply_quantization_noise(sample_wave.copy(), num_bits)

    assert quantized_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(quantized_wave, sample_wave), "Wave should be modified by quantization"

    # Check that quantized values match expected resolution
    max_amp = np.max(np.abs(sample_wave))
    quant_levels = 2**num_bits
    step_size = max_amp / (quant_levels / 2)
    unique_values = np.unique(quantized_wave)

    assert all(np.isclose(unique_values % step_size, 0, atol=1e-5)), "Quantized values should align to step size"


def test_transform_wave_with_score_zero_score(sample_wave, sample_time_vector, sample_interrupt_params, signal_generation_params):
    """
    Test that with score=0, the wave should remain unchanged.
    """
    score = 0.0  # No transformation should happen

    transformed_wave = transform_wave_with_score(
        sample_wave,
        score,
        sample_time_vector,
        signal_generation_params['n_sinusoids'],
        signal_generation_params['amplitude_range'],
        signal_generation_params['base_frequency_range'],
        sample_interrupt_params
    )

    assert np.array_equal(transformed_wave, sample_wave), "With score=0, the wave should remain unchanged"


def test_transform_wave_with_score_basic(sample_wave, sample_time_vector, sample_interrupt_params, signal_generation_params):
    """
    Test that the transformation avoids replacing the defined interrupt region.
    """
    score = 0.6  # Moderate transformation

    transformed_wave = transform_wave_with_score(
        sample_wave,
        score,
        sample_time_vector,
        signal_generation_params['n_sinusoids'],
        signal_generation_params['amplitude_range'],
        signal_generation_params['base_frequency_range'],
        sample_interrupt_params
    )

    assert transformed_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(transformed_wave, sample_wave), "High score should cause significant transformation"


def test_transform_wave_with_score_low_score(sample_wave, sample_time_vector, sample_interrupt_params, signal_generation_params):
    """
    Test that with a low score, only a small part of the wave is replaced.
    """
    score = 0.2  # Very low transformation rate

    transformed_wave = transform_wave_with_score(
        sample_wave,
        score,
        sample_time_vector,
        signal_generation_params['n_sinusoids'],
        signal_generation_params['amplitude_range'],
        signal_generation_params['base_frequency_range'],
        sample_interrupt_params
    )

    num_differences = np.sum(transformed_wave != sample_wave)
    assert num_differences > 0, "There should still be some replacement with non-zero score"
    assert num_differences < len(sample_wave) * 0.3, "With low score, only a small portion should change"


def test_transform_wave_with_score_edge_case_full_interrupt(sample_wave, sample_time_vector, signal_generation_params):
    """
    Test edge case where interrupt region covers the entire wave.
    """
    full_interrupt_params = [{'start_idx': 0, 'duration_idx': len(sample_wave)}]
    score = 0.5  # Moderate transformation

    transformed_wave = transform_wave_with_score(
        sample_wave,
        score,
        sample_time_vector,
        signal_generation_params['n_sinusoids'],
        signal_generation_params['amplitude_range'],
        signal_generation_params['base_frequency_range'],
        full_interrupt_params
    )

    # If interrupt covers the whole wave, no transformation should occur
    assert np.array_equal(transformed_wave, sample_wave), "Full interrupt coverage should block all transformation"

