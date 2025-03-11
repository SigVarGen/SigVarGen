import numpy as np

from SigVarGen.variations.transformations import apply_time_shift

def envelope_linear(num_samples, npw, param):
    start, end = npw
    if param > 0.5:
        envelope = np.linspace(start, end, num=num_samples)
    else:
        envelope = np.linspace(end, start, num=num_samples)
    return envelope

def envelope_sine(num_samples, npw, param=0.005):

    frequency = param

    low, high = npw
    amplitude = (high - low) / 2.0
    offset = (high + low) / 2.0
    
    x = np.arange(num_samples)
    # sine wave oscillates in [-1, 1], so scale and offset
    envelope = offset + amplitude * np.sin(2.0 * np.pi * frequency * x)

    envelope = apply_time_shift(envelope, 500)
    
    return envelope

def envelope_random_walk(num_samples, npw, param=0.01):

    step_std = param

    low, high = npw
    envelope = np.zeros(num_samples)
    
    # Start somewhere in the middle
    envelope[0] = (low + high) / 2.0
    
    for i in range(1, num_samples):
        envelope[i] = envelope[i-1] + np.random.normal(0, step_std)
        # Clip to ensure we stay in [low, high]
        envelope[i] = np.clip(envelope[i], low, high)
    
    return envelope

def envelope_blockwise(num_samples, npw, param=100):

    block_size = int(param)

    envelope = np.zeros(num_samples)
    low, high = npw
    
    n_blocks = num_samples // block_size
    remainder = num_samples % block_size
    
    idx = 0
    for _ in range(n_blocks):
        val = np.random.uniform(low, high)
        envelope[idx: idx+block_size] = val
        idx += block_size
    
    if remainder > 0:
        val = np.random.uniform(low, high)
        envelope[idx:] = val
    
    return envelope