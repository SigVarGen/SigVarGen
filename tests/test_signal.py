import numpy as np
import pytest
from SigVarGen import generate_signal

# -------------------------------------
# Tests for generate_signal
# -------------------------------------

def test_generate_signal_output_shape(sample_time_vector):
    """Check that the generated signal has the correct shape."""
    signal, params = generate_signal(sample_time_vector, 5, (0.1, 1.0), (5, 50))
    assert signal.shape == sample_time_vector.shape, "Signal shape should match time vector shape"

def test_generate_signal_params_length(sample_time_vector):
    """Ensure the correct number of sinusoid parameters are returned."""
    _, params = generate_signal(sample_time_vector, 5, (0.1, 1.0), (5, 50))
    assert len(params) == 5, "Number of sinusoid parameters should match n_sinusoids"

def test_generate_signal_amplitude_range(sample_time_vector):
    """Verify the signal's final amplitude is within the specified range."""
    amplitude_range = (0.1, 1.0)
    signal, _ = generate_signal(sample_time_vector, 5, amplitude_range, (5, 50))
    
    assert np.min(signal) >= amplitude_range[0], "Signal minimum should match amplitude range lower bound"
    assert np.max(signal) <= amplitude_range[1], "Signal maximum should match amplitude range upper bound"

def test_generate_signal_params_structure(sample_time_vector):
    """Ensure each sinusoid parameter set has the correct keys."""
    _, params = generate_signal(sample_time_vector, 5, (0.1, 1.0), (5, 50))

    for param in params:
        assert set(param.keys()) == {'amp', 'freq', 'phase'}, "Each sinusoid param dict should have amp, freq, and phase"

def test_generate_signal_randomness(sample_time_vector):
    """Check that calling generate_signal twice gives different signals."""
    signal1, params1 = generate_signal(sample_time_vector, 5, (0.1, 1.0), (5, 50))
    signal2, params2 = generate_signal(sample_time_vector, 5, (0.1, 1.0), (5, 50))

    assert not np.array_equal(signal1, signal2), "Two generated signals should not be identical"
    assert params1 != params2, "Two sets of sinusoid parameters should not be identical"

def test_generate_signal_frequency_range(sample_time_vector):
    """Ensure all frequencies fall within the specified frequency range."""
    frequency_range = (5, 50)
    _, params = generate_signal(sample_time_vector, 5, (0.1, 1.0), frequency_range)

    for param in params:
        assert frequency_range[0] <= param['freq'] <= frequency_range[1], "Frequency should be within specified range"
