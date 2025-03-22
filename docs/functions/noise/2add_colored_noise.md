Absolutely! Here's the **expanded and fully updated documentation** for `add_colored_noise`, now including the **new features** like:

- `fs` (sampling rate) for realistic frequency scaling  
- Support for **additional noise colors** (`blue`, `violet`)  
- Support for **custom spectral filters (callables)**  
- **Return of isolated noise** for analysis  
- **Time-varying envelopes**

---

## `add_colored_noise`

**Location:** `noise/noise_addition.py`

---

### Description

`add_colored_noise` introduces **colored noise** into a signal using frequency-domain filtering techniques. It simulates real-world interference by allowing users to define **spectral characteristics**, **noise intensity**, and **modulation envelopes** for **non-stationary noise**.

This function is especially useful for:
- Creating **realistic signal variations**
- **Stress-testing** algorithms under different noise conditions
- **Signal augmentation** for machine learning and data-driven modeling

---

### ✨ New Features
- **`fs` (sampling rate)** parameter ensures accurate spectral shaping
- Supports **blue** and **violet** noise profiles
- Accepts **custom frequency-domain filters** as callables
- Returns **isolated noise component** for separate inspection
- Applies **modulation envelope** to simulate time-varying noise

---

### Notes

- **White noise** → flat power across all frequencies  
- **Pink noise** → power ∝ 1/f (natural, biological systems)  
- **Brown noise** → power ∝ 1/f² (emphasizes low frequencies)  
- **Blue noise** → power ∝ f (emphasizes high frequencies)  
- **Violet noise** → power ∝ f² (extreme high-frequency boost)  
- **Custom filters** can target specific frequency patterns (e.g., harmonic peaks)

---

### Parameters

- **wave** (`np.ndarray`):  
  The input signal to which noise will be added.

- **fs** (`float`):  
  Sampling rate in Hz. Used to compute correct frequency bins for spectral shaping.

- **noise_power** (`float`):  
  Base noise power (variance). Determines energy of the added noise.

- **npw** (`tuple(float, float)`):  
  Range multiplier for noise power. Adds variability in intensity.  
  Example: `(0.8, 1.2)` allows ±20% fluctuation.

- **mf** (`tuple(float, float)`):  
  Range for amplitude modulation applied to the entire signal.  
  Simulates slight scaling due to environmental or hardware changes.

- **color** (`str` or `callable`, optional):  
  Defines the spectral profile of the noise. Options:
  - `'white'` → flat spectrum
  - `'pink'` → 1/f
  - `'brown'` → 1/f²
  - `'blue'` → f
  - `'violet'` → f²  
  - **Callable** → custom function `filter(freqs)` that returns a frequency-domain mask  
    (e.g., harmonic peaks or band-limited filters)

- **mod_envelope** (`dict`, optional):  
  Modulates the **noise amplitude over time** (non-stationary noise). Should include:
  - `'func'`: an envelope function like `envelope_sine`, `envelope_random_walk`, etc.
  - `'param'`: parameter(s) passed to the envelope function (usually a range)  
  Example: `{'func': envelope_sine, 'param': [0.01, 0.015]}`. More parameter examples provided in config.py.
  - If `None`, noise remains stationary. Default: `None`. 


---

### Returns

- **res** (`np.ndarray`):  
  Final signal with colored, possibly modulated noise added.

- **noise** (`np.ndarray`):  
  The noise component alone (useful for plotting, denoising tests, etc.)

---

### Example Usage

```python
import numpy as np
import SigVarGen as svg

# Create a clean sine wave
fs = 1000  # Hz
t = np.linspace(0, 1, fs, endpoint=False)
clean_signal = np.sin(2 * np.pi * 5 * t)

# Define parameters
noise_power = 0.05
npw_range = (1.0, 1.2)
mf_range = (1.0, 1.0)

# Add blue noise with sine-modulated envelope
noisy_signal, noise = svg.add_colored_noise(
    wave=clean_signal,
    fs=fs,
    noise_power=noise_power,
    npw=npw_range,
    mf=mf_range,
    color='blue',
    mod_envelope={'func': svg.envelope_sine, 'param': [0.01, 0.02]}
)

# Optional: plot or analyze the noise separately
print("Noisy Signal:", noisy_signal[:10])
print("Isolated Noise:", noise[:10])
```
