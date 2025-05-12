from scipy.interpolate import interp1d
import numpy as np

def interpoling(res, target_len=10000):
    """
    Linearly interpolates a signal to a desired target length.

    Parameters
    ----------
    res : np.ndarray
        Input 1D array or list to be interpolated.
    target_len : int, optional
        The desired length of the output interpolated signal. Default is 10,000.

    Returns
    -------
    res1_i : np.ndarray
        The interpolated array of length `target_len`.
    """
    target_indices = np.linspace(0, 1, target_len)
    original_indices = np.linspace(0, 1, len(res))
    interpolator = interp1d(original_indices, res, kind='linear')
    res1_i = interpolator(target_indices)
    return res1_i

def normalization(signal1):
    """
    Standardizes a signal to have zero mean and unit variance.

    Parameters
    ----------
    signal1 : np.ndarray
        Input 1D array or list to be normalized.

    Returns
    -------
    signal1_norm : np.ndarray
        The normalized signal with mean 0 and standard deviation 1.
    """
    signal1_norm = (signal1 - np.mean(signal1)) / np.std(signal1)
    return signal1_norm

def randomize_trace(
    trace,
    adjust_mean = True,
    mean_min = None,
    mean_max = None,
    mean_std = None,
    adjust_var = False,
    var_mean = None,
    var_min = None,
    var_max = None,
    var_std = None):
    """
    Randomize a trace by optionally rescaling its variance and/or shifting its mean.

    Parameters
    ----------
    trace : np.ndarray
        1D input time series, original signal.
    mean_min : float, optional
        Lower clip bound for sampled target mean.
    mean_max : float, optional
        Upper clip bound for sampled target mean.
    mean_std : float, optional
        Stddev for sampling target mean around (mean_min+mean_max)/2.
    var_mean : float, optional
        Mean for sampling target variance.
    var_std : float, optional
        Stddev for sampling target variance.
    var_min : float, optional
        Lower clip bound for sampled target variance.
    var_max : float, optional
        Upper clip bound for sampled target variance.
    adjust_mean : bool, default=True
        Whether to shift the mean of the trace.
    adjust_var : bool, default=False
        Whether to rescale the variance of the trace.

    Returns
    -------
    out : np.ndarray
        The signal with randomised mean/var.
    """
    out = trace.astype(float)

    # ===== VARIANCE ADJUSTMENT =====
    if adjust_var:
        if None in (var_std, var_min, var_max):
            raise ValueError("To adjust variance, must provide var_mean, var_std, var_min, var_max")
        current_var = np.var(out)
        # sample and clip target variance
        var_mean = (var_min + var_max) / 2.0
        target_var = np.random.normal(loc=var_mean, scale=var_std)
        target_var = np.clip(target_var, var_min, var_max)
        # scale to match target variance
        factor = np.sqrt(target_var / (current_var + 1e-12))
        out = out * factor

    # ===== MEAN ADJUSTMENT =====
    if adjust_mean:
        if None in (mean_min, mean_max, mean_std):
            raise ValueError("To adjust mean, must provide mean_min, mean_max, mean_std")
        # center current trace
        out = out - np.mean(out)
        # sample and clip target mean
        mean_center = (mean_min + mean_max) / 2.0
        target_mean = np.random.normal(loc=mean_center, scale=mean_std)
        target_mean = np.clip(target_mean, mean_min, mean_max)
        # shift to target mean
        out = out + target_mean

    return out
