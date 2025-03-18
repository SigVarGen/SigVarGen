## `generate_noise_power`

**Location:** `noise/noise.py`

---

## Description
`generate_noise_power` calculates the noise power (variance) for a given signal based on a randomly selected signal-to-noise ratio (SNR) from a specified range. This function enables controlled noise injection, allowing for precise simulation of noisy environments in signal processing applications.

By selecting an SNR value and computing the corresponding noise power, the function ensures that the noise level is appropriately scaled relative to the signal's amplitude. This is useful for testing denoising algorithms, simulating real-world measurement noise, and augmenting synthetic datasets.

---

### Notes
- The function selects an SNR value (in dB) randomly within the specified range.
- A higher SNR results in lower noise power, preserving signal clarity.
- A lower SNR introduces stronger noise, making the signal more distorted.
- The noise power is computed as the variance of the noise signal required to achieve the selected SNR.
- Colored and non-stationary noise can introduce frequency-selective distortions or dynamic fluctuations that are not reflected by a simple SNR value. 

---

### Parameters

- **wave** (`numpy.ndarray`):  
  The input signal from which noise power will be computed.

- **snr_range** (`tuple` of `int`, optional):  
  The range of SNR values (in dB) from which a value is randomly selected.  
  - Default: `(-20, 30)` (low to high SNR scenarios).  
  - Example: `(-10, 20)` simulates moderate noise levels.

---

### Returns

- **noise_power** (`float`):  
  The computed noise power (variance) based on the selected SNR.

- **selected_snr_db** (`float`):  
  The randomly selected SNR (in dB), useful for reference.

---

### Usage Example
```python
import numpy as np
import SigVarGen as svg

# Generate a synthetic sine wave
t = np.linspace(0, 1, 1000)
clean_signal = np.sin(2 * np.pi * 5 * t)

# Compute noise power with a random SNR in the range (-10, 20) dB
noise_power, snr_db = svg.generate_noise_power(clean_signal, snr_range=(-10, 20))

print(f"Selected SNR: {snr_db} dB")
print(f"Computed Noise Power: {noise_power}")
```
