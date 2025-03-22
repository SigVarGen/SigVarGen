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

def generate_device_parameters(device_params, drop=False, frequency_follows_amplitude=True, split_ratios=[0.5, 0.5]):
    """
    Splits device parameters into N ranges based on split_ratios.

    Parameters
    ----------
    device_params : dict
        Dictionary of device specs. Format:
        {
            'DeviceName': {
                'amplitude': (min_amp, max_amp),
                'frequency': (min_freq, max_freq) or dict of ranges
            }
        }

    drop : bool
        If False, the first split gets the lower amplitude range.
        If True, the first split gets the upper amplitude range.

    frequency_follows_amplitude : bool
        If True, frequency ranges are split using the same logic as amplitude.
        If False, all splits receive the full frequency range.

    split_ratios : list of float
        Proportions that define how to divide the amplitude and frequency ranges.
        Must sum to 1.0.

    Returns
    -------
    List[dict]
        A list of device parameter dicts, each corresponding to a split.
    """
    if not split_ratios or not np.isclose(sum(split_ratios), 1.0):
        raise ValueError("split_ratios must be a non-empty list and sum to 1.0")

    n = len(split_ratios)
    split_param_sets = [{} for _ in range(n)]

    for device, params in device_params.items():
        amp_min, amp_max = params['amplitude']
        amp_range = amp_max - amp_min

        # Compute amplitude boundaries
        amp_bounds = [amp_min]
        for ratio in split_ratios:
            amp_bounds.append(amp_bounds[-1] + ratio * amp_range)

        if drop:
            amp_bounds = amp_bounds[::-1]

        for i in range(n):
            split_param_sets[i].setdefault(device, {})
            split_param_sets[i][device]['amplitude'] = tuple(sorted((amp_bounds[i], amp_bounds[i + 1])))

        # Frequency handling
        if 'frequency' in params:
            def split_freq_range(freq_min, freq_max):
                freq_range = freq_max - freq_min
                bounds = [freq_min]
                for ratio in split_ratios:
                    bounds.append(bounds[-1] + ratio * freq_range)
                if drop:
                    bounds = bounds[::-1]
                return [tuple(sorted((bounds[i], bounds[i + 1]))) for i in range(n)]

            if isinstance(params['frequency'], dict):
                for i in range(n):
                    split_param_sets[i][device]['frequency'] = {}

                for key, (freq_min, freq_max) in params['frequency'].items():
                    if frequency_follows_amplitude:
                        freq_splits = split_freq_range(freq_min, freq_max)
                        for i in range(n):
                            split_param_sets[i][device]['frequency'][key] = freq_splits[i]
                    else:
                        for i in range(n):
                            split_param_sets[i][device]['frequency'][key] = (freq_min, freq_max)
            else:
                freq_min, freq_max = params['frequency']
                if frequency_follows_amplitude:
                    freq_splits = split_freq_range(freq_min, freq_max)
                    for i in range(n):
                        split_param_sets[i][device]['frequency'] = freq_splits[i]
                else:
                    for i in range(n):
                        split_param_sets[i][device]['frequency'] = (freq_min, freq_max)

    return split_param_sets

