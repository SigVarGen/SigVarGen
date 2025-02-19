#print("Initializing SigVarGen package...")

from .noise import *
from .signal import *
from .variations import *

from .config import *
from .utils import *

#__version__ = 1.0.0

__all__ = ['noise', 'signal', 'variations'
            'envelope_linear', 'envelope_sine', 'envelope_random_walk', 'envelope_blockwise',
            'calculate_noise_power', 'add_colored_noise',
            'get_non_overlapping_interval', 'place_interrupt', 'apply_interrupt_modifications', 
            'add_main_interrupt', 'add_smaller_interrupts', 'add_interrupt_with_params', 'add_interrupt_bursts',
            'generate_semi_periodic_signal', 'add_periodic_interrupts', 'generate_signal',
            'apply_baseline_drift_region', 'apply_baseline_drift_polynomial', 
            'apply_baseline_drift_piecewise', 'apply_baseline_drift_quadratic', 
            'apply_baseline_drift_middle_peak', 'generate_parameter_variations', 'generate_variation',
            'apply_time_shift', 'apply_time_warp', 'apply_gain_variation',
            'apply_amplitude_modulation', 'apply_baseline_drift', 
            'apply_amplitude_modulation_region', 'transform_wave_with_score',
            'apply_nonlinear_distortion', 'apply_quantization_noise',
            'EMBEDDED_DEVICE_RANGES', 'EMBEDDED_DEVICE_INTERRUPTS', 'param_sweeps',
            'noise_funcs', 'npw_levels', 'mf_levels',
            'calculate_CP', 'euclidean_distance', 'interpoling', 'normalization']

#from . import noise
#from . import signal
#from . import variations

