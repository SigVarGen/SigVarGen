## `get_non_overlapping_interval`

**Location:** `signal/response_signals.py`

## Description

`get_non_overlapping_interval` attempts to find a valid start index for an interrupt interval that does not overlap with any existing occupied intervals. The function ensures that newly placed interruptions maintain separation from existing ones, considering an optional buffer. If no suitable interval is found within the maximum number of tries, the function returns `None`.

This function is useful for scheduling perturbations in signals where interruptions must be placed without conflicts.

---

### Parameters

- **signal_length** (`int`): The total length of the signal (in samples).  
- **duration_idx** (`int`): The duration of the interrupt (in samples).  
- **occupied_intervals** (`list` of `tuple`): List of `(start_idx, end_idx)` pairs representing already occupied intervals.  
- **max_tries** (`int`, optional): Maximum number of attempts to find a valid interval (default: `1000`).  
- **buffer** (`int`, optional): Minimum separation between interruptions (default: `1`).

---

### Returns

- **`tuple`** (`(start_idx, end_idx)`) if a non-overlapping interval is found.  
- **`None`** if no valid interval is found after `max_tries`.

---

## Usage Example

```python
import SigVarGen as svg

# Define occupied intervals
occupied_intervals = [(100, 200), (300, 400)]

# Attempt to place a non-overlapping interval in a signal of length 1000
interval = svg.get_non_overlapping_interval(1000, duration_idx=50, occupied_intervals=occupied_intervals)

print("New Interval:", interval)  # Example output: (450, 500)
```