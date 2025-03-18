## `generate_semi_periodic_signal`

**Location:** `signal/response_signals.py`

## **Description**
`generate_semi_periodic_signal` creates a **semi-periodic** digital signal by repeating a given binary pattern and introducing random bit flips. This function is useful for modeling schedulled interruptions with possible delays.

---

### **Notes**
- Increasing `flip_probability` increases randomness, making the signal less periodic.
- The function repeats `base_pattern` as needed and truncates to the required `length`.
- Setting a `seed` ensures consistent signal generation across multiple runs.

---

### **Parameters**

- **length** (`int`, optional): The total length of the generated signal (default: `450`).

- **base_pattern** (`list` of `int`, optional): A binary sequence representing the repeating base pattern.  
  - If `None`, defaults to `[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]`.

- **flip_probability** (`float`, optional): The probability of flipping each bit to simulate signal variations (default: `0.1`).

- **seed** (`int`, optional): Random seed for reproducibility (default: `None`).

---

### **Returns**

- **semi_periodic_signal** (`numpy.ndarray`):  
  The generated **semi-periodic** binary signal.

---

### **Usage Example**
```python
import numpy as np
import SigVarGen as svg

# Generate a semi-periodic signal with a bit flip probability of 5%
semi_periodic_signal = svg.generate_semi_periodic_signal(length=300, flip_probability=0.05)

print("Generated Signal:", semi_periodic_signal[:20])  # Print first 20 samples
```


