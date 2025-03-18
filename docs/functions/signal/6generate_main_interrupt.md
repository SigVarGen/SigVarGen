## `generate_main_interrupt`

**Location:** `signal/response_signals.py`

## Description

`generate_main_interrupt` creates a sinusoidal-based interrupt signal by wrapping around the `generate_signal` function. The function dynamically selects frequency and amplitude ranges from a given `interrupt_ranges` dictionary. Additionally, optional scaling factors enable users to fine-tune amplitude and frequency variations. Note: Scaling factors results in prioritization of specific region of predefined range, and shouldn't be used to go beyond initial range. 

---

### Parameters

- **t** (`numpy.ndarray`): The time vector for the signal (typically generated using `np.linspace`).  
- **domain** (`str`): The key used to access amplitude and frequency ranges from `interrupt_ranges`.  
- **interrupt_ranges** (`dict`): A dictionary containing predefined amplitude and frequency ranges for different domains.  
- **temp** (`int`): Determines which frequency index to use within the frequency range.  
- **n_sinusoids** (`int`, optional): Number of sinusoids to sum in the interrupt signal. If `None`, a random value between `2` and `10` is chosen.  
- **amplitude_scale** (`float`, optional): Scaling factor applied to amplitude values (default: `1.0`).  
- **frequency_scale** (`float`, optional): Scaling factor applied to frequency values (default: `1.0`).  

---

### Returns

- **interrupt_signal** (`numpy.ndarray`): The generated interrupt signal composed of sinusoidal components.  
- **interrupt_params** (`list` of `dict`): A list containing dictionaries with the parameters (`amp`, `freq`, `phase`) of each generated sinusoid.  

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Define a time vector from 0 to 1 second with 1000 samples
t = np.linspace(0, 1, 1000)

# Define predefined amplitude and frequency ranges
interrupt_ranges = {
    "device_A": {
        "amplitude": (0.5, 2.0),
        "frequency": [(5, 15), (30, 60), (70, 120)]  # Example frequency options
    }
}

# Generate an interrupt signal for domain "device_A" using frequency index 1
interrupt_signal, params = svg.generate_main_interrupt(
    t,
    domain="device_A",
    interrupt_ranges=interrupt_ranges,
    temp=1,  # Selects the second frequency range (10-30 Hz)
    n_sinusoids=5,
    amplitude_scale=1.2,
    frequency_scale=0.9
)

print("Generated Interrupt Signal Shape:", interrupt_signal.shape)
print("Sinusoid Parameters:", params)
```
