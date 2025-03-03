import numpy as np

from SigVarGen.noise.envelopes import *

# Reduced amplitude so, interrupts are generated with higher mean 
EMBEDDED_DEVICE_RANGES_SPIKE = {
    'Arduino Board': {
        'amplitude': (0, 2),  
        'frequency': (0, 10e3)  # in Hz
    },
    'Drones': {
        'amplitude': (0, 0.35), 
        'frequency': {
            'control': (2.399e9, 2.401e9),  # in Hz
            'telemetry_low': (432.5e6, 433.5e6),  # in Hz
            'telemetry_high': (2.4e9, 5.8e9)  # in Hz
        }
    },
    'Cameras': {
        'amplitude': (0, 0.35), 
        'frequency': (24, 60)  # in Hz, as frames per second
    },
    'Smartphones': {
        'amplitude': (0, 0.35),  # (Vrms)
        'frequency': {
            'lte_low': (699.5e6, 700.5e6),  # in Hz
            'lte_high': (2.599e9, 2.601e9),  # in Hz
            '5g_low': (599.5e6, 600.5e6),  # in Hz
            '5g_high': (38.95e9, 39.05e9)  # in Hz
        }
    },
    'Wi-Fi Routers': {
        'amplitude': (0, 0.35),
        'frequency': {
            'wifi_2_4ghz': (2.399e9, 2.401e9),  # in Hz
            'wifi_5ghz': (4.995e9, 5.005e9),    # in Hz
            'wifi_6ghz': (5.995e9, 6.005e9)     # in Hz
        }
    },
    'Smart Watches': {
        'amplitude': (0, 0.3e-3),
        'frequency': (2.399e9, 2.401e9)  # in Hz
    },
    'Home Automation Devices': {
        'amplitude': (0, 0.35e-3),
        'frequency': {
            'zigbee': (2.399e9, 2.401e9),     # in Hz
            'z_wave_eu': (867.5e6, 868.5e6),  # in Hz
            'z_wave_us': (907.5e6, 908.5e6)   # in Hz
        }
    },
    'Automotive Sensors': {
        'amplitude': (0, 0.003),
        'frequency': {
            'us': (314.5e6, 315.5e6),   # in Hz
            'eu': (432.5e6, 433.5e6)    # in Hz
        }
    }
}



EMBEDDED_DEVICE_INTERRUPTS_SPIKE = {
    'Arduino Board': {
        'amplitude': (0, 5),  # Increased amplitude (2-3 times higher)
        'frequency': (0, 12e3)  # Increased upper frequency limit
    },
    'Drones': {
        'amplitude': (0, 1),  # Increased amplitude
        'frequency': {
            'control': (2.398e9, 2.402e9),      # Expanded frequency range
            'telemetry_low': (432e6, 434e6),    # Expanded frequency range
            'telemetry_high': (2.39e9, 5.9e9)   # Expanded frequency range
        }
    },
    'Cameras': {
        'amplitude': (0, 1),  # Increased amplitude
        'frequency': (24, 120)  # Increased upper frame rate limit
    },
    'Smartphones': {
        'amplitude': (0, 1),  # Increased amplitude (Vrms)
        'frequency': {
            'lte_low': (699e6, 701e6),      # Expanded frequency range
            'lte_high': (2.598e9, 2.602e9), # Expanded frequency range
            '5g_low': (599e6, 601e6),       # Expanded frequency range
            '5g_high': (38.9e9, 39.1e9)     # Expanded frequency range
        }
    },
    'Wi-Fi Routers': {
        'amplitude': (0, 1),  # Increased amplitude
        'frequency': {
            'wifi_2_4ghz': (2.395e9, 2.405e9),  # Expanded frequency range
            'wifi_5ghz': (4.990e9, 5.010e9),    # Expanded frequency range
            'wifi_6ghz': (5.990e9, 6.010e9)     # Expanded frequency range
        }
    },
    'Smart Watches': {
        'amplitude': (0, 0.9e-3),  # Increased amplitude
        'frequency': (2.398e9, 2.402e9)  # Expanded frequency range
    },
    'Home Automation Devices': {
        'amplitude': (0, 0.9e-3),  # Increased amplitude
        'frequency': {
            'zigbee': (2.398e9, 2.402e9),     # Expanded frequency range
            'z_wave_eu': (867e6, 869e6),      # Expanded frequency range
            'z_wave_us': (907e6, 909e6)       # Expanded frequency range
        }
    },
    'Automotive Sensors': {
        'amplitude': (0, 0.01),  # Increased amplitude
        'frequency': {
            'us': (314e6, 316e6),   # Expanded frequency range
            'eu': (432e6, 434e6)    # Expanded frequency range
        }
    }
}

# High idle device activity mean
EMBEDDED_DEVICE_RANGES_DROP = {
    'Arduino Board': {
        'amplitude': (3, 4), 
        'frequency': (0, 12e3)    # in Hz
    },
    'Drones': {
        'amplitude': (0.35, 0.65), 
        'control': (2.398e9, 2.402e9),      
            'telemetry_low': (432e6, 434e6),    
            'telemetry_high': (2.39e9, 5.9e9)
    },
    'Cameras': {
        'amplitude': (0.35, 0.65),
        'frequency': (24, 60)  # in Hz, as frames per second
    },
    'Smartphones': {
        'amplitude': (0.35, 0.65),  # (Vrms)
        'frequency': {
            'lte_low': (699.5e6, 700.5e6),  # in Hz
            'lte_high': (2.599e9, 2.601e9),  # in Hz
            '5g_low': (599.5e6, 600.5e6),  # in Hz
            '5g_high': (38.95e9, 39.05e9)  # in Hz
        }
    },
    'Wi-Fi Routers': {
        'amplitude': (0.35, 0.65),
        'frequency': {
            'wifi_2_4ghz': (2.399e9, 2.401e9),  # in Hz
            'wifi_5ghz': (4.995e9, 5.005e9),    # in Hz
            'wifi_6ghz': (5.995e9, 6.005e9)     # in Hz
        }
    },
    'Smart Watches': {
        'amplitude': (0.3e-3, 0.1e-3), 
        'frequency': (2.399e9, 2.401e9)  # in Hz
    },
    'Home Automation Devices': {
        'amplitude': (0.35e-3, 0.1e-3), 
        'frequency': {
            'zigbee': (2.399e9, 2.401e9),     # in Hz
            'z_wave_eu': (867.5e6, 868.5e6),  # in Hz
            'z_wave_us': (907.5e6, 908.5e6)   # in Hz
        }
    },
    'Automotive Sensors': {
        'amplitude': (0.003, 0.006), 
        'frequency': {
            'us': (314.5e6, 315.5e6),   # in Hz
            'eu': (432.5e6, 433.5e6)    # in Hz
        }
    }
}


EMBEDDED_DEVICE_INTERRUPTS_DROP = {
    'Arduino Board': {
        'amplitude': (1, 3), 
        'frequency': (0, 12e3)  
    },
    'Drones': {
        'amplitude': (0, 0.35), 
        'frequency': {
            'control': (2.398e9, 2.402e9),      
            'telemetry_low': (432e6, 434e6),    
            'telemetry_high': (2.39e9, 5.9e9)   
        }
    },
    'Cameras': {
        'amplitude': (0, 0.35),  
        'frequency': (24, 120)  
    },
    'Smartphones': {
        'amplitude': (0, 0.35),  # (Vrms)
        'frequency': {
            'lte_low': (699e6, 701e6),     
            'lte_high': (2.598e9, 2.602e9),
            '5g_low': (599e6, 601e6),      
            '5g_high': (38.9e9, 39.1e9)    
        }
    },
    'Wi-Fi Routers': {
        'amplitude': (0, 0.35),
        'frequency': {
            'wifi_2_4ghz': (2.395e9, 2.405e9),  
            'wifi_5ghz': (4.990e9, 5.010e9),    
            'wifi_6ghz': (5.990e9, 6.010e9)     
        }
    },
    'Smart Watches': {
        'amplitude': (0, 0.9e-3),  
        'frequency': (2.398e9, 2.402e9)  
    },
    'Home Automation Devices': {
        'amplitude': (0, 0.9e-3),  
        'frequency': {
            'zigbee': (2.398e9, 2.402e9),  
            'z_wave_eu': (867e6, 869e6),   
            'z_wave_us': (907e6, 909e6)    
        }
    },
    'Automotive Sensors': {
        'amplitude': (0, 0.01),  
        'frequency': {
            'us': (314e6, 316e6),  
            'eu': (432e6, 434e6)   
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

noise_funcs = [None, {'func': envelope_linear, 'param': [1, 1]}, {'func': envelope_sine, 'param': [0.0001, 0.01]}, {'func': envelope_random_walk, 'param': [0.01, 0.15]}, {'func': envelope_blockwise, 'param': [50, 1000]}]

npw_levels = [[1, 1], [0.9, 1.1], [0.85, 1.2], [0.8, 1.3], [0.75, 1.4], [0.7, 1.5], [0.65, 1.6], [0.6, 1.7]]
mf_levels = [[0.75, 0.85], [0.8, 0.9], [1, 1], [1.0, 1.1], [1.0, 1.2]]
