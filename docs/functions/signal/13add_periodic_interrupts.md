## `add_periodic_interrupts`

**Location:** `signal/response_signals.py`

## **Description**
`add_periodic_interrupts` introduces periodic digital interruptions into a base signal. It applies binary modulated interruptions in two distinct phases:
1. Before and after the main interruption.
2. During the main interruption.

---

### **Parameters**

- **base_signal** (`numpy.ndarray`): The original signal to which periodic interruptions will be added.

- **amplitude_range** (`tuple` of `float`): The `(min, max)` amplitude range of the device.

- **inter_sig** (`numpy.ndarray`): The interrupt signal to be modulated and inserted into the base signal.

- **start_idx** (`int`): The start index of the **main interruption**.

- **duration_idx** (`int`): The **duration** (in samples) of the main interruption.

- **length** (`int`, optional): The default length of the periodic signals if `base_pattern` is `None` (default: `450`).

- **base_pattern, base_pattern_2** (`list` of `int`, optional): Binary sequences representing the **two periodic interruption patterns**.  
  - If `None`, defaults to `[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]`.

- **flip_probability, flip_probability_2** (`float`, optional): The probability of flipping bits in **each periodic pattern** (default: `0.1`).

- **offset** (`float`): The **amplitude offset** applied to interruptions.

---

### **Returns**

- **modified_signal** (`numpy.ndarray`): The modified base signal containing **periodic interruptions**.

---

### **Usage Example**
```python
import numpy as np
import SigVarGen as svg

# Example base signal
base_signal = np.ones(1000)

# Example periodic interrupt waveform
inter_sig = np.sin(np.linspace(0, np.pi, 1000))

# Apply periodic interruptions
modified_signal = svg.add_periodic_interrupts(
    base_signal=base_signal,
    length=1000,
    amplitude_range=(0, 2),
    inter_sig=inter_sig,
    start_idx=300,
    duration_idx=100,
    offset=0.5
)

print("Modified Signal (First 350 Samples):", modified_signal[:350])
```
