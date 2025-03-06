import numpy as np
import pytest

@pytest.fixture
def sample_device_params():
    """Provides dictionary containing amplitude and frequencies for two devices"""
    return {
        "DeviceA": {
            "amplitude": (0, 10),
            "frequency": {
                "low": (100, 200),
                "high": (500, 1000),
            }
        },
        "DeviceB": {
            "amplitude": (5, 15),
            "frequency": (50, 150)
        }
    }

@pytest.fixture
def sample_interrupt_ranges_drop():
    """Fixture to provide mock interrupt ranges for a test device."""
    return {
        "DeviceA": {
            "amplitude": (0.2, 1.0),
            "frequency": {
                "low": (5, 15),
                "high": (20, 50),
            }
        }
    }

@pytest.fixture
def sample_interrupt_ranges_rise():
    """Fixture to provide mock interrupt ranges for a test device."""
    return {
        "DeviceA": {
            "amplitude": (9.0, 10.0),
            "frequency": {
                "low": (205, 215),
                "high": (1020, 1500),
            }
        }
    }

@pytest.fixture
def sample_signal_length():
    """Fixture to provide a standard signal length for tests."""
    return 1000


@pytest.fixture
def sample_time_vector():
    """Fixture to provide a standard time vector for tests."""
    return np.linspace(0, 1, 1000)

@pytest.fixture
def sample_wave():
    return np.sin(np.linspace(0, 2 * np.pi, 1000))

@pytest.fixture
def zero_wave():
    return np.zeros(1000)


@pytest.fixture
def sample_param_sweeps():
    return {
        'time_shift': np.arange(0, 50),
        'time_warp': np.linspace(0.05, 0.2, 10),
        'gain_variation': np.linspace(0.1, 0.5, 5),
        'amplitude_modulation': np.linspace(0.2, 0.6, 5),
        'modulation_with_region': np.linspace(0.2, 0.5, 5),
        'baseline_drift': np.linspace(0.1, 0.5, 5),
        'baseline_drift_region': np.linspace(0.1, 0.5, 5)
    }

@pytest.fixture
def sample_interrupt_params():
    return [{'start_idx': 300, 'duration_idx': 100}]

@pytest.fixture
def signal_generation_params():
    """Example parameters needed for `generate_signal`."""
    return {
        'n_sinusoids': 5,
        'amplitude_range': (0.1, 1.0),
        'base_frequency_range': (10, 100)
    }