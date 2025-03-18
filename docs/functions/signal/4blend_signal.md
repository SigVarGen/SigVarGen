## `blend_signal`

**Location:** `signal/response_signals.py`

## Description

`blend_signal` combines a base signal segment with an interrupt segment using a linear blending factor. This function allows controlled integration of an interrupt into an existing signal, where the `blend` parameter determines how much of the base signal is preserved versus how much of the interrupt is applied.

This technique is useful for smooth signal modifications, ensuring better alignment with device amplitude and frequency boundaries.

---

### Parameters

- **base_slice** (`numpy.ndarray`): The base signal segment to be modified.  
- **interrupt_slice** (`numpy.ndarray`): The interrupt signal segment to be blended into the base signal.  
- **blend** (`float`, optional): The blending factor between `0` and `1` (default: `0.5`).
  - A value closer to `1` retains more of the base signal.
  - A value closer to `0` retains more of the interrupt signal.

---

### Returns

- **blended_signal** (`numpy.ndarray`): The resulting signal segment after blending.

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create example base and interrupt slices
base_slice = np.array([1, 2, 3, 4, 5])
interrupt_slice = np.array([10, 9, 8, 7, 6])

# Blend the two slices with a factor of 0.7 (favoring base signal)
blended = svg.blend_signal(base_slice, interrupt_slice, blend=0.7)

print("Blended Signal:", blended)  
# Example Output: [3.3, 3.9, 4.5, 5.1, 5.7]
```