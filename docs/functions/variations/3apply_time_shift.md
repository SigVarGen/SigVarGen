## `apply_time_shift`

**Location:** `variations/transformations.py`

---

## Description  
`apply_time_shift` introduces a **random shift** in a waveform by circularly shifting the signal within a given range. This transformation is useful for **simulating sensor delays, synchronization errors, or minor misalignments** in signal acquisition.

---

### Notes  
- The waveform is shifted by a **random number of samples** within the range `[-max_shift, max_shift]`.  
- Uses **circular shifting**, meaning values that shift beyond the end of the array wrap around to the beginning.  

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform to be shifted.

- **max_shift** (`int`):  
  The maximum number of samples to shift in either direction.

---

### Returns  

- **shifted_wave** (`numpy.ndarray`):  
  The time-shifted waveform.

---

### Usage Example  
```python
import SigVarGen as svg

shifted_wave = svg.apply_time_shift(wave, max_shift=50)
```