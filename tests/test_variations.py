import numpy as np
import pytest
from SigVarGen import (
    generate_parameter_variations,
    generate_variation,
    apply_time_shift,              
    apply_time_warp,
    apply_gain_variation,
    apply_amplitude_modulation,
    apply_baseline_drift,
    apply_amplitude_modulation_region,
    apply_baseline_drift_region,
    transform_wave_with_score,
    generate_signal                  
)


def test_generate_parameter_variations_basic(sample_param_sweeps):
    """
    Test basic generation of parameter variations.
    """
    variations = generate_parameter_variations(sample_param_sweeps, num_variants=5, window_size=2)

    assert len(variations) == 5, "Should generate the specified number of variants"
    for variant in variations:
        assert isinstance(variant, dict), "Each variation should be a dictionary of parameters"
        for key in sample_param_sweeps.keys():
            assert key in variant, f"Missing parameter: {key}"
        assert 'f_min' in variant and 'f_max' in variant, "f_min and f_max should be included"
        assert 0.1 <= variant['f_min'] <= 0.9, "f_min should be within expected bounds"
        assert 0.1 <= variant['f_max'] <= 0.9, "f_max should be within expected bounds"
        assert variant['f_min'] <= variant['f_max'], "f_min should not exceed f_max"




def test_generate_variation_applies_all_transforms(sample_wave, sample_time_vector, sample_interrupt_params):
    """
    Test generate_variation applies all transformations from parameters.
    """
    variant_params = {
        'time_shift': 10,
        'time_warp': 0.1,
        'gain_variation': 0.2,
        'amplitude_modulation': 0.3,
        'modulation_with_region': 0.4,
        'baseline_drift': 0.2,
        'baseline_drift_region': 0.3,
        'f_min': 0.2,
        'f_max': 0.7,
        'wave_with_score': 0.5
    }

    transformed_wave = generate_variation(
        transformed_wave=sample_wave.copy(),
        variant_params=variant_params,
        t=sample_time_vector,
        n_sinusoids=5,
        amplitude_range=(0.1, 1.0),
        base_frequency_range=(10, 100),
        interrupt_params=sample_interrupt_params
    )

    assert transformed_wave.shape == sample_wave.shape, "Wave length should remain unchanged"
    assert not np.array_equal(transformed_wave, sample_wave), "Wave should be modified by the applied transformations"


def test_generate_variation_respects_modulation_region(sample_wave, sample_time_vector, sample_interrupt_params):
    """
    Test that modulation_with_region only affects f_min to f_max.
    """
    variant_params = {
        'time_shift': 0,
        'time_warp': 0,
        'gain_variation': 0,
        'amplitude_modulation': 0,
        'modulation_with_region': 0.5,
        'baseline_drift': 0,
        'baseline_drift_region': 0,
        'f_min': 0.3,
        'f_max': 0.6,
        'wave_with_score': 0.0
    }

    transformed_wave = generate_variation(
        transformed_wave=sample_wave.copy(),
        variant_params=variant_params,
        t=sample_time_vector,
        n_sinusoids=5,
        amplitude_range=(0.1, 1.0),
        base_frequency_range=(10, 100),
        interrupt_params=sample_interrupt_params
    )

    start_idx = int(0.3 * len(sample_wave))
    end_idx = int(0.6 * len(sample_wave))

    assert np.array_equal(transformed_wave[:start_idx], sample_wave[:start_idx]), "Before modulation region should be unchanged"
    assert np.array_equal(transformed_wave[end_idx:], sample_wave[end_idx:]), "After modulation region should be unchanged"
    assert not np.array_equal(transformed_wave[start_idx:end_idx], sample_wave[start_idx:end_idx]), "Region should be modulated"


def test_generate_variation_respects_interrupt_region(sample_wave, sample_time_vector, sample_interrupt_params):
    """
    Test that generated signal replaces parts of the wave respecting interrupt region.
    """
    variant_params = {
        'time_shift': 0,
        'time_warp': 0,
        'gain_variation': 0,
        'amplitude_modulation': 0,
        'modulation_with_region': 0,
        'baseline_drift': 0,
        'baseline_drift_region': 0,
        'f_min': 0.3,
        'f_max': 0.6,
        'wave_with_score': 0.95
    }

    original_wave = sample_wave.copy()

    transformed_wave = generate_variation(
        transformed_wave=original_wave,
        variant_params=variant_params,
        t=sample_time_vector,
        n_sinusoids=5,
        amplitude_range=(0.1, 1.0),
        base_frequency_range=(10, 100),
        interrupt_params=sample_interrupt_params
    )

    start_idx = sample_interrupt_params[0]['start_idx']
    end_idx = start_idx + sample_interrupt_params[0]['duration_idx']

    assert np.array_equal(transformed_wave[start_idx:end_idx], original_wave[start_idx:end_idx]), \
        "Interrupt region shouldn't have been replaced by generated signal"

    assert not np.array_equal(transformed_wave[end_idx:], original_wave[end_idx:]), \
        "Interrupt region shouldn't have been replaced by generated signal"


def test_generate_variation_handles_zero_transformations(sample_wave, sample_time_vector, sample_interrupt_params):
    """
    Test generate_variation does no change when all params are zero.
    """
    variant_params = {
        'time_shift': 0,
        'time_warp': 0,
        'gain_variation': 0,
        'amplitude_modulation': 0,
        'modulation_with_region': 0,
        'baseline_drift': 0,
        'baseline_drift_region': 0,
        'f_min': 0.0,
        'f_max': 1.0,
        'wave_with_score': 0.0
    }

    transformed_wave = generate_variation(
        transformed_wave=sample_wave.copy(),
        variant_params=variant_params,
        t=sample_time_vector,
        n_sinusoids=5,
        amplitude_range=(0.1, 1.0),
        base_frequency_range=(10, 100),
        interrupt_params=sample_interrupt_params
    )

    assert np.array_equal(transformed_wave, sample_wave), "Wave should remain unchanged when all transformations are zero"

    
