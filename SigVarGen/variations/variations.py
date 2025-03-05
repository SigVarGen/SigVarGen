import numpy as np

from SigVarGen.variations.transformations import *
from SigVarGen.variations.baseline_drift import *


def generate_parameter_variations(param_sweeps, num_variants=5, window_size=1):
    """
    Generate a set of parameter configurations for multiple variants for a signal.
    
    Parameters
    ----------
    param_sweeps : dict
        Dictionary where keys are parameter names and values are arrays of possible values.
    num_variants : int
        Number of variants to produce.
    window_size : int
        Half-width of the small window of values chosen around a randomly selected center point.
        
    Returns
    -------
    variations : list of dict
        A list of dictionaries, each dictionary representing the parameter values chosen 
        for one variant.
    """
    
    variations = []
    
    # For each parameter, choose a small sub-range of values
    chosen_subranges = {}
    for param, values in param_sweeps.items():
        center_idx = np.random.randint(0, len(values))

        start_idx = max(0, center_idx - window_size)
        end_idx = min(len(values), center_idx + window_size + 1)
        
        subrange = values[start_idx:end_idx]
        chosen_subranges[param] = subrange
    
    for _ in range(num_variants):
        variant_params = {}
        
        for param, subrange in chosen_subranges.items():
            variant_params[param] = np.random.choice(subrange)
        
        f_min = np.random.uniform(0.1, 0.9)
        f_max = np.random.uniform(0.1, 0.9)
        if f_max < f_min:
            f_min, f_max = f_max, f_min
        variant_params['f_min'] = f_min
        variant_params['f_max'] = f_max
        
        # Score for transform_wave_with_score function
        variant_params['wave_with_score'] = np.random.uniform(0.3, 0.7)
        
        variations.append(variant_params)
    
    return variations

def generate_variation(transformed_wave, variant_params, t, n_sinusoids, amplitude_range, base_frequency_range, interrupt_params):
    """
    Generate a variation of the given wave using the parameters from variant_params.
    
    Parameters
    ----------
    original_wave : np.ndarray
        The original input wave.
    variant_params : dict
        Dictionary containing the selected parameters for transformations.
        Expected keys:
            'time_shift'
            'time_warp'
            'gain_variation'
            'amplitude_modulation'
            'modulation_with_region'
            'baseline_drift'
            'baseline_drift_region'
            'f_min'
            'f_max'
            'wave_with_score'
    t, n_sinusoids, amplitude_range, base_frequency_range : parameters required by generate_signal and time_warp
    interrupt_params : list of dict
        Parameters defining the interrupt region. 
        Example: [{'start_idx': start_idx, 'duration_idx': duration}]
    
    Returns
    -------
    transformed_wave : np.ndarray
        The transformed wave after applying the selected parameters.

    Notes:
    ------
    - Recommended to choose more strictly transformations to apply 
    """

    # Substitute part of the signal with signal generated with same parameters
    if variant_params['wave_with_score'] > 0:
        print("!!!")
        transformed_wave = transform_wave_with_score(
            transformed_wave, 
            variant_params['wave_with_score'], 
            t, n_sinusoids, amplitude_range, base_frequency_range, 
            interrupt_params
        )

    if variant_params['time_warp'] > 0:
        transformed_wave = apply_time_warp(
            transformed_wave, 
            variant_params['time_warp'], 
            t, n_sinusoids, amplitude_range, base_frequency_range
        )

    if variant_params['time_shift'] > 0:
        transformed_wave = apply_time_shift(transformed_wave, variant_params['time_shift'])


    transformed_wave = apply_gain_variation(transformed_wave, variant_params['gain_variation'])

    # Apply amplitude modulation (global)
    transformed_wave = apply_amplitude_modulation(transformed_wave, variant_params['amplitude_modulation'])

    # Apply amplitude modulation in a region (using f_min and f_max as fractions of length)
    transformed_wave = apply_amplitude_modulation_region(
        transformed_wave,
        modulation_depth=variant_params['modulation_with_region'],
        f_min=variant_params['f_min'],
        f_max=variant_params['f_max']
    )

    # Apply baseline drift (global)
    transformed_wave = apply_baseline_drift(transformed_wave, variant_params['baseline_drift'])

    # Apply baseline drift in a region
    transformed_wave = apply_baseline_drift_region(transformed_wave, variant_params['baseline_drift_region'],
                                                   start_frac=variant_params['f_min'],
                                                   end_frac=variant_params['f_max'])


    return transformed_wave
