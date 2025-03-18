## `add_interrupt_bursts`

**Location:** `signal/response_signals.py`

## Description

`add_interrupt_bursts` introduces multiple small sinusoidal-based interrupts into a specified time window within the signal. These interruptions mimic burst-like behavior and can be constrained to a specific range of amplitudes and frequencies. The function ensures that the added interrupts do not exceed device limitations while providing flexible placement and modification options.

This function is useful for generating high-frequency perturbations within a defined time window, making it applicable for tasks such as synthetic signal generation, fault injection in testing environments, and simulating real-world signal bursts.

### Additional Notes

- The function first determines a valid frequency range based on `DEVICE_RANGES` and `temp`.  
- Each interrupt is placed randomly within the specified window (`start_idx` to `end_idx`).  
- The duration of each interrupt is randomly selected within the given `small_duration_ratio_range`.  
- Interrupts may be either **rising** or **falling**, controlled by the `drop2` parameter.  
- The final signal is clipped to respect `device_min` and `device_max` constraints.  

---

### Parameters

- **t** (`numpy.ndarray`): The time vector for the signal (usually created using `np.linspace`).  
- **base_signal** (`numpy.ndarray`): The original base signal that will be modified.  
- **domain** (`str`): The key used to retrieve amplitude and frequency ranges from `DEVICE_RANGES`.  
- **DEVICE_RANGES** (`dict`): Dictionary containing overall device amplitude and frequency limits.  
- **device_min** (`float`): The minimum allowable amplitude for the device.  
- **device_max** (`float`): The maximum allowable amplitude for the device.  
- **temp** (`int`): The index used to determine the specific frequency range from `DEVICE_RANGES`.  
- **start_idx** (`int`, optional): The minimum start index for bursts (default: `0`).  
- **end_idx** (`int`, optional): The maximum end index for bursts (default: `0`, meaning the full signal length).  
- **n_small_interrupts** (`int`, optional):  
  - The number of small interrupts to add.  
  - If `None`, a random value between `15` and `20` is chosen.  
- **non_overlap** (`bool`, optional):  
  - If `True`, prevents interrupts from overlapping with previously placed bursts.  
  - Default: `False`.  
- **small_duration_ratio_range** (`tuple` of `float`, optional):  
  - The range of possible duration ratios for small interrupts.  
  - If `None`, a random value between `0.001` and `0.005` is used.  

---

### Returns

- **updated_base_signal** (`numpy.ndarray`): The modified base signal with added burst-like interruptions.  

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Define a base signal (zero baseline)
base_signal = np.zeros_like(t)

# Define device amplitude and frequency limits
DEVICE_RANGES = {
    "device_A": {
        "amplitude": (0.0, 5.0),
        "frequency": (70, 120)
    }
}

# Apply multiple small bursts within a specific region of the signal
updated_signal = svg.add_interrupt_bursts(
    t=t,
    base_signal=base_signal,
    domain="device_A",
    DEVICE_RANGES=DEVICE_RANGES,
    device_min=0.0,
    device_max=5.0,
    temp=0,
    start_idx=300,
    end_idx=700,  # Bursts will be limited to this window
    n_small_interrupts=10,
    non_overlap=True,
    small_duration_ratio_range=(0.005, 0.01)
)

print("Updated Signal Shape:", updated_signal.shape)
```
