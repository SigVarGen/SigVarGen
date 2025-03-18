# generate_signal

**Location:** `signal/signal_generation.py`

## Description

`generate_signal` constructs a composite waveform by summing multiple sinusoidal components. Each component is assigned a random amplitude, frequency, and phase from user‑defined ranges. After generation, the composite signal is normalized—centering it around zero mean and scaling to fit a specified amplitude interval. This approach mirrors real‑world signals, which often comprise numerous harmonic elements.

---

### Parameters

- **t** (`numpy.ndarray`): The time vector over which the signal is sampled.  
- **n_sinusoids** (`int`): The number of sinusoidal components.  
- **amplitude_range** (`tuple` of floats): Minimum and maximum amplitudes for each sinusoid.  
- **frequency_range** (`tuple` of floats): Minimum and maximum frequencies for each sinusoid.

### Returns

- **signal** (`numpy.ndarray`): The composite waveform.  
- **sinusoids_params** (`list` of `dict`): Contains `amp`, `freq`, and `phase` for each sinusoid.

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Generate a composite signal made up of five sinusoidal components
signal, params = svg.generate_signal(
    t,
    n_sinusoids=5,
    amplitude_range=(0.1, 1.0),
    frequency_range=(24, 120)
)

print("Generated signal shape:", signal.shape)
print("Sinusoid parameters:", params)
```