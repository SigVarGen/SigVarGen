## `apply_interrupt_modifications`

**Location:** `signal/response_signals.py`

## Description

`apply_interrupt_modifications` applies amplitude shifting and optional baseline drift on the interrupt segment, and later blend it into a base signal. By controlling drift behavior (`disperse=True/False`) and specifying whether the signal should drop or rise, the function ensures that interruptions remain realistic while conforming to system limitations. Finally,it adjusts an interrupt signal segment to fit within predefined device constraints.

---

### Parameters

- **inter_part** (`numpy.ndarray`): The segment of the interrupt signal to be modified.  
- **base_part** (`numpy.ndarray`): The corresponding segment of the base signal.  
- **device_min** (`float`): Minimum allowed amplitude of the device.  
- **device_max** (`float`): Maximum allowed amplitude of the device.  
- **drop** (`bool`):  
  - If `True`, shifts the interrupt signal downward (drops below baseline).  
  - If `False`, shifts the interrupt signal upward.  
- **disperse** (`bool`, optional):  
  - If `True`, applies a varying baseline drift with peak drift in the middle (default: `False`).  
- **blend_factor** (`float`, optional):  
  - The blending factor between `0` and `1` (default: `0.5`).  
  - A higher value retains more of the base signal.  
  - A lower value retains more of the interrupt signal.

---

### Returns

- **modified_inter_part** (`numpy.ndarray`): The modified interrupt signal segment after drift and offset adjustments.  
- **offset** (`float`): The amount by which the interrupt signal was shifted.

---

## Usage Example

```python
import numpy as np
import SigVarGen as svg

# Create example base and interrupt signal segments
base_part = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
inter_part = np.array([10.0, 9.5, 9.0, 8.5, 8.0])

# Define device amplitude limits
device_min, device_max = 0.0, 10.0

# Apply modifications to the interrupt segment
modified_inter, offset = svg.apply_interrupt_modifications(
    inter_part, base_part, device_min, device_max, drop=True, disperse=True, blend_factor=0.7
)

print("Modified Interrupt:", modified_inter)
print("Applied Offset:", offset)
```