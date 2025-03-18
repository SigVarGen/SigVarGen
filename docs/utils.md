## `utils.py`

**Location:** `utils.py`

---

## Description  
The `utils.py` module provides **helper functions** for **signal processing, normalization, interpolation, and device-specific parameter management**. These functions support the **core operations** of the framework by offering **signal evaluation, transformation, and metadata generation**.

The main functionalities include:
- **Signal quality assessment** (e.g., Signal-to-Noise Ratio, Euclidean Distance)
- **Signal normalization and interpolation**
- **Device-specific parameter management**, allowing controlled variations in **amplitude and frequency constraints**.

---

## Functions  

### `calculate_SNR`
Computes the **Signal-to-Noise Ratio (SNR)** between a **clean signal** and its **noisy version**.

**Parameters:**
- `signal` (`numpy.ndarray`): Original signal.
- `noisy_signal` (`numpy.ndarray`): Noisy version of the signal.

**Returns:**
- `snr_db` (`float`): Signal-to-noise ratio in decibels (dB).

**Example:**
```python
snr = calculate_SNR(clean_signal, noisy_signal)
print(f"SNR: {snr:.2f} dB")
```

---

### `calculate_ED`
Computes the **Euclidean Distance (ED)** between two signals.

**Parameters:**
- `X` (`numpy.ndarray`): First signal.
- `Y` (`numpy.ndarray`): Second signal.

**Returns:**
- `ed` (`float`): Euclidean distance between `X` and `Y`.

**Example:**
```python
ed = calculate_ED(signal1, signal2)
print(f"Euclidean Distance: {ed}")
```

---

### `interpoling`
Performs **linear interpolation** to adjust a signal to a **target length**.

**Parameters:**
- `res` (`numpy.ndarray`): Input signal to be interpolated.
- `target_len` (`int`, optional): Desired output length (default: `10000`).

**Returns:**
- `numpy.ndarray`: Interpolated signal.

**Example:**
```python
resampled_signal = interpoling(signal, target_len=5000)
```

---

### `normalization`
Performs **z-score normalization** on a signal, ensuring **zero mean and unit variance**.

**Parameters:**
- `signal1` (`numpy.ndarray`): Input signal.

**Returns:**
- `numpy.ndarray`: Normalized signal.

**Example:**
```python
normalized_signal = normalization(raw_signal)
```

---

### `generate_device_parameters`

`generate_device_parameters` splits the **amplitude and frequency ranges** of device configurations into two **distinct subsets**. This allows for **controlled variations** in device constraints, which is useful for **simulating different operating conditions** or **testing parameter-dependent behaviors** in signal processing tasks.

By adjusting the **split ratio**, users can control the **proportion of the parameter space assigned to each subset**. Additionally, the function can:
- **Preserve full frequency ranges** for both subsets or  
- **Split frequency ranges proportionally with amplitude constraints**.

---

#### Notes
- If `drop=False`, the **first subset** receives the **lower amplitude range**, and the **second subset** gets the **higher amplitude range**.
- If `drop=True`, the assignment is **reversed**.
- If `frequency_follows_amplitude=True`, **frequency ranges are split along with amplitude**.
- If `frequency_follows_amplitude=False`, both subsets retain the **full frequency range**.
- A `split_ratio` of `0.5` evenly distributes the parameter space between the two subsets.

---

#### Parameters  

- **device_params** (`dict`):  
  Dictionary containing device parameter configurations.  
  Each entry should include:
  - `'amplitude'`: Tuple **(min, max)** voltage levels.
  - `'frequency'`: Tuple **(min, max)** frequency range or a nested dictionary of frequency bands.

- **drop** (`bool`, optional):  
  - `False` → First dictionary gets **lower amplitude range**.  
  - `True` → First dictionary gets **upper amplitude range**.  
  **Default:** `False`.

- **frequency_follows_amplitude** (`bool`, optional):  
  - `True` → **Frequency ranges split proportionally** to amplitude.  
  - `False` → Both subsets retain **full frequency range**.  
  **Default:** `True`.

- **split_ratio** (`float`, optional):  
  Fraction **(0.0 to 1.0)** defining how much of the range is assigned to the **first subset**.  
  - `0.0` → All values go to the **second subset**.  
  - `1.0` → All values go to the **first subset**.  
  **Default:** `0.5`.

---

#### Returns  

- **lower_params** (`dict`):  
  Dictionary containing **lower-range** parameter configurations.

- **upper_params** (`dict`):  
  Dictionary containing **upper-range** parameter configurations.

---

#### Usage Example  

```python
import numpy as np
import SigVarGen.utils as utils

# Example device parameters
device_params = {
    'Arduino Board': {
        'amplitude': (0, 5),  # Voltage range
        'frequency': (0, 12e3)  # Hz
    },
    'Drones': {
        'amplitude': (0, 1),  # Voltage range
        'frequency': {
            'control': (2.398e9, 2.402e9),  # Hz
            'telemetry_low': (432e6, 434e6),  # Hz
            'telemetry_high': (2.39e9, 5.9e9)  # Hz
        }
    }
}

# Generate parameter subsets with a 60/40 split and frequency following amplitude
lower_params, upper_params = utils.generate_device_parameters(
    device_params, drop=False, split_ratio=0.6
)

print("Lower Parameter Set:", lower_params)
print("Upper Parameter Set:", upper_params)
```

---

## Summary  
The `utils.py` module provides **essential support functions** for **signal transformation, evaluation, and device-specific parameter handling**. These functions **enhance signal processing workflows** and ensure **realistic device constraints for generated signals**.