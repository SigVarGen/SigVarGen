## `add_colored_noise`

**Location:** `noise/noise_addition.py`

---

## Description
`add_colored_noise` introduces noise (white, pink, or brown) into a signal, simulating realistic noisy environments. This function applies frequency-domain filtering to generate colored noise with specific spectral properties and then scales it to a defined noise power level.

Additionally, an optional modulation envelope can be applied, introducing time-dependent amplitude variations that mimic real-world non-stationary noise patterns. This makes the function valuable for signal augmentation, testing noise-robust algorithms, and creating realistic simulations of environmental interference.

---

### Notes
- **White noise** has a flat power spectrum across all frequencies.
- **Pink noise** follows a \(1/f\) spectral decay, often found in natural and biological systems.
- **Brown noise** follows a \(1/f^2\) spectral decay, emphasizing lower frequencies.
- The noise power is adjusted relative to the input signal using a **specified SNR range**.
- Applying a **modulation envelope** allows for non-stationary noise characteristics.

---

### Parameters

- **wave** (`numpy.ndarray`):  
  The original signal to which noise will be added.

- **noise_power** (`float`):  
  The base noise power level, determining the variance of the added noise.

- **npw** (`tuple` of `float`):  
  A range (`min`, `max`) defining noise power variation, allowing randomness in noise intensity between different measurements.

- **mf** (`tuple` of `float`):  
  A range (`min`, `max`) defining the modulation factor variation, slightly altering the signal amplitude between different measurements.

- **color** (`str`, optional):  
  Type of noise to add:  
  - `'white'` → Equal power at all frequencies.  
  - `'pink'` → Power decays as \(1/f\), common in speech and natural signals.  
  - `'brown'` → Power decays as \(1/f^2\), emphasizing low frequencies.  
  **Default:** `'pink'`.

- **mod_envelope** (`dict`, optional):  
  Dictionary specifying a time-varying amplitude envelope for non-stationary noise:  
  - `'func'`: The envelope function.  
  - `'param'`: Range of parameters for the envelope function.  
    If `None`, noise remains stationary. **Default:** `None`.
    Parameter examples provided in `config.py`.

---

### Returns

- **res** (`numpy.ndarray`):  
  The input signal with added colored noise.

- **noise** (`numpy.ndarray`):  
  The isolated noise component, useful for separate analysis or denoising techniques.

---

### Usage Example
```python
import numpy as np
import SigVarGen as svg

# Generate a clean sine wave
t = np.linspace(0, 1, 1000)
clean_signal = np.sin(2 * np.pi * 5 * t)

# Define noise parameters
noise_power = 0.05
npw_range = (1, 1.1)
mf_range = (1, 1) 

# Add pink noise with a sine modulation envelope
noisy_signal, noise = svg.add_colored_noise(
    wave=clean_signal,
    noise_power=noise_power,
    npw=npw_range,
    mf=mf_range,
    color="pink",
    mod_envelope={"func": svg.envelope_sine, "param": [0.01, 0.015]} 
)

print("Noisy Signal Shape:", noisy_signal.shape)
```
