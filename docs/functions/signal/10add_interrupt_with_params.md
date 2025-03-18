## `add_interrupt_with_params`

**Location:** `signal/response_signals.py`

## Description

`add_interrupt_with_params` introduces a primary sinusoidal-based interrupt into a signal while optionally embedding smaller and overlapping secondary interrupts. The function ensures that all interrupts adhere to predefined amplitude and frequency constraints, and it allows for configurable properties such as baseline drift, blending, and size variation. This function is useful for generating complex, realistic perturbations in time-series data.

---

### Parameters

- **t** (`numpy.ndarray`): The time vector for the signal (usually created using `np.linspace`).  
- **base_signal** (`numpy.ndarray`): The original base signal to be modified.  
- **domain** (`str`): The key used to retrieve amplitude and frequency ranges from `INTERRUPT_RANGES`.  
- **DEVICE_RANGES** (`dict`): A dictionary containing amplitude and frequency limits for the device.  
- **INTERRUPT_RANGES** (`dict`): A dictionary containing predefined amplitude and frequency ranges for different domains.  
- **temp** (`int`): The index determining which frequency range to use.  
- **drop** (`bool`, optional):  
  - If `True`, the interrupt is offset downward.  
  - If `False`, the interrupt is offset upward.  
  - Default: `True`.  
- **disperse** (`bool`, optional):  
  - If `True`, applies a varying baseline drift with a peak drift in the middle.  
  - Default: `True`.  
- **duration_ratio** (`float`, optional):  
  - The fraction of total signal length occupied by the main interrupt.  
  - If `None`, a random value between `0.06` and `0.12` is chosen.  
- **n_smaller_interrupts** (`int`, optional):  
  - The number of smaller interrupts to add.  
  - If `None`, a random value between `0` and `2` is chosen.  
- **n_sinusoids** (`int`, optional):  
  - The number of sinusoidal components in each interrupt.  
  - If `None`, a random number between `2` and `10` is chosen.  
- **non_overlap** (`bool`, optional):  
  - If `True`, ensures that interrupts do not overlap with previously occupied intervals.  
  - Default: `True`.  
- **complex_iter** (`int`, optional):  
  - The number of smaller overlapping interrupts embedded within the main interrupt.  
  - Default: `0`.  
- **blend_factor** (`float`, optional):  
  - The weight used to blend the base and interrupt signals.  
  - Default: `0.5`.  
- **shrink_complex** (`bool`, optional):  
  - If `True`, each successive overlapping interrupt shrinks in size.  
  - Default: `False`.  
- **shrink_factor** (`float`, optional):  
  - The fraction by which each overlapping complex interrupt shrinks.  
  - Default: `0.9`.  
- **buffer** (`int`, optional):  
  - The minimum spacing (in samples) between interrupts when `non_overlap=True`.  
  - Default: `1`.

---

### Returns

- **updated_base_signal** (`numpy.ndarray`): The modified base signal with added interrupts.  
- **interrupt_params** (`list` of `dict`): A list of metadata describing each added interrupt, including:
  - `start_idx` (`int`): The start index of the interrupt.
  - `duration_idx` (`int`): The duration of the interrupt in samples.
  - `offset` (`float`): The applied amplitude offset.
  - `sinusoids_params` (`dict` or `list`): Parameters used to generate the sinusoidal components.
  - `type` (`str`):  
    - `"main"` for the primary interrupt.  
    - `"small"` for secondary smaller interrupts.  

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Define a base signal (zero baseline)
base_signal = np.zeros_like(t)

# Define device and interrupt amplitude/frequency ranges
DEVICE_RANGES = {
    "device_A": {
        "amplitude": (0.0, 5.0),
        "frequency": [(5, 15), (30, 60), (70, 120)]
    }
}

INTERRUPT_RANGES = {
    "device_A": {
        "amplitude": (0.5, 2.0),
        "frequency": [(5, 15), (10, 30), (20, 50)]
    }
}

# Add a main interrupt and optionally smaller secondary interrupts
updated_signal, params = svg.add_interrupt_with_params(
    t=t,
    base_signal=base_signal,
    domain="device_A",
    DEVICE_RANGES=DEVICE_RANGES,
    INTERRUPT_RANGES=INTERRUPT_RANGES,
    temp=1,
    drop=False,
    disperse=True,
    duration_ratio=0.08,
    n_smaller_interrupts=2,
    complex_iter=1,
    blend_factor=0.6,
    shrink_complex=True,
    buffer=10
)

print("Updated Signal Shape:", updated_signal.shape)
print("Interrupt Parameters:", params)
```
