import numpy as np
from scipy.interpolate import interp1d

def calculate_SNR(signal, noisy_signal):
    noise = noisy_signal - signal
    signal_power = np.abs(np.mean(signal ** 2))
    noise_power = np.abs(np.mean(noise ** 2))
    return 10 * np.log10(signal_power / noise_power)

def calculate_ED(X, Y):
    return np.linalg.norm(X - Y)

def interpoling(res, target_len=10000):
    target_indices = np.linspace(0, 1, target_len)
    original_indices = np.linspace(0, 1, len(res))
    interpolator = interp1d(original_indices, res, kind='linear')
    res1_i = interpolator(target_indices)
    return res1_i

def normalization(signal1):
    signal1_norm = (signal1 - np.mean(signal1)) / np.std(signal1)
    return signal1_norm

def generate_device_parameters(device_params, drop=False, frequency_follows_amplitude=True, split_ratio=0.5):
    """
    Splits device parameters into two ranges.

    Parameters:
        device_params (dict): Device parameter dictionary in the described format.
        drop (bool): If False, first dict gets lower amplitude, if True, first gets upper.
        frequency_follows_amplitude (bool): If True, frequencies split with amplitude.
                                             If False, both ranges get the full frequency range.
        split_ratio (float): Proportion of the range assigned to the first dictionary (0.0 to 1.0).

    Returns:
        tuple: (lower_params, upper_params)
    """
    if not (0 <= split_ratio <= 1):
        raise ValueError("split_ratio must be between 0.0 and 1.0")

    lower_params = {}
    upper_params = {}

    for device, params in device_params.items():
        amplitude_min, amplitude_max = params['amplitude']

        split_point_amplitude = amplitude_min + split_ratio * (amplitude_max - amplitude_min)

        if drop:
            lower_params[device] = {'amplitude': (split_point_amplitude, amplitude_max)}
            upper_params[device] = {'amplitude': (amplitude_min, split_point_amplitude)}
        else:
            lower_params[device] = {'amplitude': (amplitude_min, split_point_amplitude)}
            upper_params[device] = {'amplitude': (split_point_amplitude, amplitude_max)}

        if 'frequency' in params:
            if isinstance(params['frequency'], dict):
                lower_params[device]['frequency'] = {}
                upper_params[device]['frequency'] = {}

                for key, (freq_min, freq_max) in params['frequency'].items():
                    if frequency_follows_amplitude:
                        split_point_freq = freq_min + split_ratio * (freq_max - freq_min)
                        if drop:
                            lower_params[device]['frequency'][key] = (split_point_freq, freq_max)
                            upper_params[device]['frequency'][key] = (freq_min, split_point_freq)
                        else:
                            lower_params[device]['frequency'][key] = (freq_min, split_point_freq)
                            upper_params[device]['frequency'][key] = (split_point_freq, freq_max)
                    else:
                        lower_params[device]['frequency'][key] = (freq_min, freq_max)
                        upper_params[device]['frequency'][key] = (freq_min, freq_max)
            else:
                freq_min, freq_max = params['frequency']
                if frequency_follows_amplitude:
                    split_point_freq = freq_min + split_ratio * (freq_max - freq_min)
                    if drop:
                        lower_params[device]['frequency'] = (split_point_freq, freq_max)
                        upper_params[device]['frequency'] = (freq_min, split_point_freq)
                    else:
                        lower_params[device]['frequency'] = (freq_min, split_point_freq)
                        upper_params[device]['frequency'] = (split_point_freq, freq_max)
                else:
                    lower_params[device]['frequency'] = (freq_min, freq_max)
                    upper_params[device]['frequency'] = (freq_min, freq_max)

    return lower_params, upper_params
