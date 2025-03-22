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

Here's the **updated documentation** for your new generalized version of `generate_device_parameters_n_split`, which supports splitting into **N subsets** (not just two), while keeping all your original intent and style:

---

### `generate_device_parameters_n_split`

`generate_device_parameters_n_split` splits the **amplitude and frequency ranges** of device configurations into **multiple distinct subsets**. This helps to generate distinct spaces for idle and interrupting signals.

By adjusting the **split ratios**, users can precisely control how much of the amplitude and frequency range is assigned to each subset.

---

#### Notes
- The number of splits is determined by the **length of `split_ratios`** (e.g. `[0.3, 0.4, 0.3]` → 3 splits).
- If `drop=False`, the subsets are assigned from **low → high amplitude**.
- If `drop=True`, the subsets are assigned from **high → low amplitude**.
- If `frequency_follows_amplitude=True`, frequency ranges are **split proportionally** alongside amplitude.
- If `frequency_follows_amplitude=False`, **all subsets receive the full frequency range**.

---

#### Parameters  

- **device_params** (`dict`):  
  A dictionary of **device configurations**, where each key is a **device name** (e.g., `'Arduino Board'`) and each value is a dictionary with:
  - `'amplitude'`: Tuple `(min_amplitude, max_amplitude)`  
  - `'frequency'`:  
    - Either a tuple `(min_frequency, max_frequency)`  
    - Or a nested dictionary of frequency bands:
      ```python
      'frequency': {
          'band_1': (f_min1, f_max1),
          'band_2': (f_min2, f_max2),
          ...
      }
      ```

- **drop** (`bool`, optional):  
  If `True`, the first returned subset gets the **upper part** of the amplitude range.  
  If `False`, the first subset gets the **lower part**.  
  **Default:** `False`.

- **frequency_follows_amplitude** (`bool`, optional):  
  If `True`, frequency ranges are split proportionally with amplitude.  
  If `False`, each subset receives the **entire frequency range**.  
  **Default:** `True`.

- **split_ratios** (`list of float`):  
  A list of ratios (e.g., `[0.3, 0.4, 0.3]`) that determine how to divide the amplitude and frequency ranges.  
  Must sum to **1.0**.  
  **Default:** `[0.5, 0.5]`

---

#### Returns  

- **param_subsets** (`list of dict`):  
  A list of dictionaries containing parameter subsets.  
  Each corresponds to one portion of the original range, based on `split_ratios`.

---

#### Usage Example  

```python
import numpy as np
import SigVarGen.utils as utils

# Device configuration
device_params = {
    'Arduino Board': {
        'amplitude': (0, 5),
        'frequency': (0, 12e3)
    },
    'Drones': {
        'amplitude': (0, 1),
        'frequency': {
            'control': (2.398e9, 2.402e9),
            'telemetry_low': (432e6, 434e6),
            'telemetry_high': (2.39e9, 5.9e9)
        }
    }
}

# Split into 3 subsets: 30%, 40%, 30%
param_splits = utils.generate_device_parameters_n_split(
    device_params,
    drop=False,
    frequency_follows_amplitude=True,
    split_ratios=[0.3, 0.4, 0.3]
)

for i, subset in enumerate(param_splits):
    print(f"Subset {i+1}:", subset)
```

---

## Summary  
The `utils.py` module provides **essential support functions** for **signal transformation, evaluation, and device-specific parameter handling**. These functions **enhance signal processing workflows** and ensure **realistic device constraints for generated signals**.