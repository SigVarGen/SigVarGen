## `apply_amplitude_modulation_region`

**Location:** `variations/transformations.py`

---

## Description  
`apply_amplitude_modulation_region` applies **localized amplitude modulation** to a specific portion of a signal. This is useful for **simulating partial signal fluctuations**, such as **localized interference or dynamic system responses**.

---

### Notes  
- **Modulation occurs only within the specified fraction (`f_min` to `f_max`)** of the signal length.  
- Uses **sinusoidal modulation** with a **random frequency** between `0.1 Hz` and `1.0 Hz`.  
- The **rest of the waveform remains unchanged**.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform.

- **modulation_depth** (`float`, optional):  
  Strength of the amplitude modulation.  
  **Default:** `0.5`.

- **f_min** (`float`, optional):  
  Fraction of the signal length where modulation starts.  
  **Default:** `0.1`.

- **f_max** (`float`, optional):  
  Fraction of the signal length where modulation stops.  
  **Default:** `1.0`.

---

### Returns  

- **modulated_wave** (`numpy.ndarray`):  
  The waveform with localized amplitude modulation.

---

### Usage Example  
```python
modulated_wave = svg.apply_amplitude_modulation_region(wave, 0.3, 0.2, 0.8)
```
