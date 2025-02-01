import numpy as np
from scipy.interpolate import interp1d

def calculate_CP(signal, noisy_signal):
    noise = noisy_signal - signal
    signal_power = np.abs(np.mean(signal ** 2))
    noise_power = np.abs(np.mean(noise ** 2))
    return 10 * np.log10(signal_power / noise_power)

def euclidean_distance(X, Y):
    return np.linalg.norm(X - Y)

def interpoling(res):
    target_indices = np.linspace(0, 1, 10000)
    original_indices = np.linspace(0, 1, len(res))
    interpolator = interp1d(original_indices, res, kind='linear')
    res1_i = interpolator(target_indices)
    return res1_i

def normalization(signal1):
    #signal1_norm = signal1 - np.mean(signal1)
    signal1_norm = (signal1 - np.mean(signal1)) / np.std(signal1)
    return signal1_norm