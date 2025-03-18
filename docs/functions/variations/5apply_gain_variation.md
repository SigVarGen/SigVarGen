## `apply_gain_variation`

**Location:** `variations/transformations.py`

---

## Description  
`apply_gain_variation` **randomly scales** the amplitude of a signal by applying a **multiplicative gain factor**. This transformation simulates **changes in sensor sensitivity, varying signal strengths, or environmental gain fluctuations**.

---

### Notes  
- The gain factor is selected **randomly** in the range `[1 - max_gain_variation, 1 + max_gain_variation]`.  
- The **waveform shape remains unchanged**, only the amplitude is affected.  

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform.

- **max_gain_variation** (`float`):  
  The maximum deviation in gain factor.

---

### Returns  

- **modified_wave** (`numpy.ndarray`):  
  The gain-modified waveform.

---

### Usage Example  
```python
modified_wave = svg.apply_gain_variation(wave, max_gain_variation=0.2)
```
