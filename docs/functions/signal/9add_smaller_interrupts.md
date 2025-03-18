## `add_smaller_interrupts`

**Location:** `signal/response_signals.py`

## Description

`add_smaller_interrupts` inserts multiple secondary (smaller) sinusoidal-based interrupts into an existing base signal. These interrupts are placed at randomly determined positions, ensuring they do not overlap with previously occupied intervals (if `non_overlap=True`). The function applies optional modifications such as amplitude drift, baseline shifts, and controlled blending with the base signal.

This function is useful for creating complex, realistic perturbations in synthetic signals, mimicking naturally occurring variations.

---

### Parameters

- **t** (`numpy.ndarray`): The time vector for the signal (usually created using `np.linspace`).  
- **base_signal** (`numpy.ndarray`): The original base signal, which may already contain modifications.  
- **INTERRUPT_RANGES** (`dict`): Dictionary containing predefined amplitude and frequency ranges for different domains.  
- **domain** (`str`): The key used to retrieve amplitude and frequency ranges from `INTERRUPT_RANGES`.  
- **temp** (`int`): The index determining which frequency range to use.  
- **n_smaller_interrupts** (`int`): The number of smaller interrupts to insert into the base signal.  
- **occupied_intervals** (`list` of `tuple`): List of previously occupied `(start_idx, end_idx)` intervals to avoid overlap.  
- **disperse** (`bool`):  
  - If `True`, applies a varying baseline drift with a peak drift in the middle.  
- **drop** (`bool`):  
  - If `True`, shifts the interrupt downward (below the baseline).  
  - If `False`, shifts the interrupt upward (above the baseline).  
- **small_duration_ratio** (`float`): The fraction of the total signal length occupied by each small interrupt.  
- **n_sinusoids** (`int`, optional): The number of sinusoids in each interrupt. If `None`, a random number between `2` and `10` is chosen.  
- **non_overlap** (`bool`, optional):  
  - If `True`, ensures smaller interrupts do not overlap with existing intervals.  
- **buffer** (`int`, optional): The minimum number of samples to separate consecutive interrupts when `non_overlap=True` (default: `1`).

---

### Returns

- **updated_base_signal** (`numpy.ndarray`): The modified base signal after adding smaller interrupts.  
- **interrupt_params** (`list` of `dict`): Metadata for each added smaller interrupt, including:
  - `start_idx` (`int`): Start index of the interrupt.
  - `duration_idx` (`int`): Length of the interrupt in samples.
  - `offset` (`float`): Applied amplitude offset.
  - `sinusoids_params` (`dict` or `list`): Parameters used to generate the sinusoidal components.
  - `type` (`str`): `"small"` indicating a secondary interrupt.

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Define a base signal (zero baseline)
base_signal = np.zeros_like(t)

# Define predefined amplitude and frequency ranges
INTERRUPT_RANGES = {
    "device_A": {
        "amplitude": (0.5, 2.0),
        "frequency": [(5, 15), (30, 60), (70, 120)]
    }
}

# Define occupied intervals (to prevent overlap)
occupied_intervals = [(200, 300), (600, 700)]  # Example preoccupied regions

# Add 3 smaller interrupts to the signal
updated_signal, params = svg.add_smaller_interrupts(
    t=t,
    base_signal=base_signal,
    INTERRUPT_RANGES=INTERRUPT_RANGES,
    domain="device_A",
    temp=1,
    n_smaller_interrupts=3,
    occupied_intervals=occupied_intervals,
    disperse=True,
    drop=False,
    small_duration_ratio=0.05,  # Each interrupt is 5% of the total signal length
    buffer=10  # Ensure a gap of at least 10 samples between interrupts
)

print("Updated Signal Shape:", updated_signal.shape)
print("Interrupt Parameters:", params)
```