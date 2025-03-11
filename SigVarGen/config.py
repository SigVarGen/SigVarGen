import numpy as np

from SigVarGen.noise.envelopes import *

EMBEDDED_DEVICE_RANGES = {
    'Arduino Board': {
        'amplitude': (0, 5),  # V
        'frequency': (0, 12e3)  # Hz
    },
    'Drones': {
        'amplitude': (0, 1),  # V
        'frequency': {
            'control': (2.398e9, 2.402e9),  # Hz
            'telemetry_low': (432e6, 434e6),  # Hz
            'telemetry_high': (2.39e9, 5.9e9)  # Hz
        }
    },
    'Cameras': {
        'amplitude': (0, 1),  # V
        'frequency': (24, 120)  # Hz, as frames per second
    },
    'Smartphones': {
        'amplitude': (0, 1),  # Vrms
        'frequency': {
            'lte_low': (699e6, 701e6),  # Hz
            'lte_high': (2.598e9, 2.602e9),  # Hz
            '5g_low': (599e6, 601e6),  # Hz
            '5g_high': (38.9e9, 39.1e9)  # Hz
        }
    },
    'Wi-Fi Routers': {
        'amplitude': (0, 1),  # V
        'frequency': {
            'wifi_2_4ghz': (2.395e9, 2.405e9),  # Hz
            'wifi_5ghz': (4.990e9, 5.010e9),  # Hz
            'wifi_6ghz': (5.990e9, 6.010e9)  # Hz
        }
    },
    'Smart Watches': {
        'amplitude': (0, 0.9e-3),  # V
        'frequency': (2.398e9, 2.402e9)  # Hz
    },
    'Home Automation Devices': {
        'amplitude': (0, 0.9e-3),  # V
        'frequency': {
            'zigbee': (2.398e9, 2.402e9),  # Hz
            'z_wave_eu': (867e6, 869e6),  # Hz
            'z_wave_us': (907e6, 909e6)  # Hz
        }
    },
    'Automotive Sensors': {
        'amplitude': (0, 0.01),  # V
        'frequency': {
            'us': (314e6, 316e6),  # Hz
            'eu': (432e6, 434e6)  # Hz
        }
    }
}

param_sweeps = {
    'Cameras': {
        'time_shift': np.arange(1, 301, 50),
        'time_warp': np.linspace(0, 0.07, 8),
        'gain_variation': np.linspace(0, 0.8, 9),
        'amplitude_modulation': np.linspace(0, 0.7, 8),
        'modulation_with_region': np.linspace(0, 3.0, 11),
        'baseline_drift': np.linspace(0, 0.7, 8), # current optimal 0.7
        'baseline_drift_region': np.linspace(0, 1.4, 8), # current optimal 1.4
        'baseline_drift_piecewise_drift': np.linspace(0, 3.5, 8), # current optimal 3.5
        'baseline_drift_piecewise_pieces': np.linspace(1, 6, 6) # current optimal 6
    },
    'Arduino Board': {
        'time_shift': np.arange(1, 301, 50),  
        'time_warp': np.linspace(0, 0.18, 4),  
        'gain_variation': np.linspace(0, 0.4, 7),
        'amplitude_modulation': np.linspace(0, 0.3, 8),
        'modulation_with_region': np.linspace(0, 0.4, 7),
        'baseline_drift': np.linspace(0, 3.0, 11),
        'baseline_drift_region': np.linspace(0, 3.4, 11),
        'baseline_drift_piecewise_drift': np.linspace(0, 6, 7),
        'baseline_drift_piecewise_pieces': np.linspace(1, 6, 6)
    }
}

noise_funcs = [None, {'func': envelope_linear, 'param': [True, False]}, {'func': envelope_sine, 'param': [0.0001, 0.01]}, {'func': envelope_random_walk, 'param': [0.01, 0.15]}, {'func': envelope_blockwise, 'param': [50, 1000]}]

npw_levels = [[1, 1], [0.9, 1.1], [0.85, 1.2], [0.8, 1.3], [0.75, 1.4], [0.7, 1.5], [0.65, 1.6], [0.6, 1.7]]
mf_levels = [[0.75, 0.85], [0.8, 0.9], [1, 1], [1.0, 1.1], [1.0, 1.2]]
