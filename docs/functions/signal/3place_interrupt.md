## `place_interrupt`

**Location:** `signal/response_signals.py`

## Description

`place_interrupt` is a utility function that determines a valid placement for an interrupt within a signal. The interrupt duration is defined as a fraction of the total signal length. The function ensures that interruptions are placed correctly, either avoiding overlaps with existing occupied intervals (when `non_overlap=True`) or allowing random placement.

This function is useful for scheduling perturbations in signals where controlled disruptions are required for testing, simulation, or augmentation.

---

### Parameters

- **signal_length** (`int`): The total length of the signal (in samples).  
- **duration_ratio** (`float`): The fraction of the signal length that the interrupt should occupy.  
- **occupied_intervals** (`list` of `tuple`): List of `(start_idx, end_idx)` pairs representing already occupied intervals.  
- **non_overlap** (`bool`, optional): If `True`, ensures the interrupt does not overlap with existing intervals (default: `True`).  
- **buffer** (`int`, optional): Minimum separation between interruptions when `non_overlap=True` (default: `1`).

---

### Returns

- **`tuple`** (`(start_idx, end_idx)`) if a valid placement is found.  
- **`None`** if no valid placement is possible.

---

## Usage Example

```python
import SigVarGen as svg

# Define occupied intervals
occupied_intervals = [(100, 200), (300, 400)]

# Attempt to place an interrupt in a signal of length 1000, occupying 5% of the signal
interrupt_interval = svg.place_interrupt(1000, duration_ratio=0.05, occupied_intervals=occupied_intervals)

print("Placed Interrupt:", interrupt_interval)  # Example output: (500, 550)
```