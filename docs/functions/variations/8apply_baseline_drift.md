## `apply_baseline_drift`

**Location:** `variations/transformations.py`

---

## Description  
`apply_baseline_drift` introduces a **linear shift** in a signal’s baseline, simulating **gradual sensor drift, environmental changes, or instrument degradation**. The drift can **increase or decrease over time**, depending on the selected parameters.

---

### Notes  
- The **maximum drift amplitude** is randomly chosen within the range `[-max_drift, max_drift]`.  
- If `reversed=True`, the drift **starts at its peak** and returns to zero.  
- When `reversed=False`, the drift **gradually increases** from zero.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform.

- **max_drift** (`float`):  
  The maximum drift applied to the signal’s baseline.

- **reversed** (`bool`, optional):  
  If `True`, the drift **starts at its maximum** and reduces to zero.  
  **Default:** `False`.

---

### Returns  

- **drifted_wave** (`numpy.ndarray`):  
  The waveform with the applied baseline drift.

---

### Usage Example  
```python
import SigVarGen as svg

drifted_wave = svg.apply_baseline_drift(wave, 0.1, reversed=True)
```
