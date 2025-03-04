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
def sample_interrupt_ranges():
    """Fixture to provide mock interrupt ranges for a test device."""
    return {
        "DeviceA": {
            "amplitude": (0.5, 2.0),
            "frequency": {
                "low": (5, 15),
                "high": (20, 50),
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
