## `add_main_interrupt`

**Location:** `signal/response_signals.py`

## Description

`add_main_interrupt` inserts a sinusoidal-based interrupt into a base signal, allowing for realistic signal perturbations. The function selects an appropriate location for the main interrupt, ensuring it fits within predefined amplitude and frequency constraints. It also supports the addition of smaller overlapping secondary interrupts when `complex_iter > 0`, making it suitable for generating complex perturbation patterns. This function is useful for simulating controlled perturbating signals.

Note: Position of the interrupt mostly identified by its initial params and blend factor with idle wave. Additionally, small offset based on the drop factor might be introduced.

---

### Parameters

- **t** (`numpy.ndarray`): The time vector for the signal (typically generated using `np.linspace`).  
- **base_signal** (`numpy.ndarray`): The original base signal, which may already contain modifications.  
- **domain** (`str`): Key used to access amplitude and frequency ranges from `RANGES`.  
- **DEVICE_RANGES** (`dict`): A dictionary containing overall amplitude and frequency limits for the device (helps to identify device min and max).  
- **INTERRUPT_RANGES** (`dict`): A dictionary containing amplitude and frequency ranges for each domain.  
- **temp** (`int`): Index used to determine which frequency range to select.  
- **duration_ratio** (`float`): The fraction of the total signal length occupied by the main interrupt.  
- **disperse** (`bool`, optional):  
  - If `True`, applies a baseline drift with a peak drift in the middle (default: `True`).  
- **drop** (`bool`, optional):  
  - If `True`, modifies the signal to dip below the baseline instead of rising above. Impacts disperse direction. 
- **n_sinusoids** (`int`, optional): The number of sinusoids composing the interrupt signal. If `None`, a random value between `2` and `10` is selected.  
- **non_overlap** (`bool`, optional):  
  - If `True`, ensures that the main interrupt does not overlap with existing intervals.  
- **complex_iter** (`int`, optional):  
  - The number of smaller overlapping interrupts to be added inside the main interrupt (default: `0`).  
- **blend_factor** (`float`, optional):  
  - The blending weight between the base and interrupt signal (default: `0.5`).  
- **shrink_complex** (`bool`, optional):  
  - If `True`, each successive smaller interrupt is shorter than the previous one.  
- **shrink_factor** (`float`, optional):  
  - The fraction by which the duration of each smaller interrupt shrinks (default: `0.9`).  

---

### Returns

- **updated_base_signal** (`numpy.ndarray`): The modified base signal after adding the main and optional complex interrupts.  
- **interrupt_params** (`list` of `dict`): Metadata describing the added interrupts, including:
  - `start_idx` (`int`): The start index of the interrupt.
  - `duration_idx` (`int`): The duration of the interrupt in samples.
  - `offset` (`float`): The applied amplitude offset.
  - `sinusoids_params` (`dict`): Parameters used to generate the sinusoids.
  - `type` (`str`): `"main"` for the primary interrupt, `"complex"` for secondary overlapping interrupts.
- **occupied_intervals** (`list` of `tuple`): Updated list of `(start_idx, end_idx)` intervals representing occupied regions in the signal.

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Define a base signal
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
        "amplitude": (4.0, 5.5),
        "frequency": [(15, 25), (40, 70), (80, 130)]
    }
}

# Add a main interrupt with optional complexity
updated_signal, params, occupied_intervals = svg.add_main_interrupt(
    t=t,
    base_signal=base_signal,
    domain="device_A",
    DEVICE_RANGES=DEVICE_RANGES,
    INTERRUPT_RANGES=INTERRUPT_RANGES,
    temp=1,
    duration_ratio=0.1,
    complex_iter=2,
    blend_factor=0.6,
    shrink_complex=True
)

print("Updated Signal Shape:", updated_signal.shape)
print("Interrupt Parameters:", params)
print("Occupied Intervals:", occupied_intervals)
```