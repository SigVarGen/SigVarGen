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
def sample_time_vector():
    """Fixture to provide a standard time vector for testing."""
    return np.linspace(0, 1, 1000)