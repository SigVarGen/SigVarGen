
## `apply_time_warp`

**Location:** `variations/transformations.py`

---

## Description  
`apply_time_warp` modifies the **time axis** of a signal, compressing or expanding sections to create **nonlinear distortions**. This function is useful for **modeling variable-speed processes, signal stretching, or real-world timing irregularities**.

---

### Notes  
- The **time axis is scaled** by a random factor in the range `[1 - max_warp_factor, 1 + max_warp_factor]`.  
- Missing parts introduced by warping are **replaced using a newly generated signal segment**, ensuring smooth continuity.  

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform to be warped.

- **max_warp_factor** (`float`):  
  The maximum factor for time warping (values close to `1` result in minimal warping).

- **t** (`numpy.ndarray`):  
  Time vector of the signal.

- **n_sinusoids** (`int`):  
  Number of sinusoids in the generated replacement signal.

- **amplitude_range** (`tuple` of `float`):  
  Amplitude range for the replacement signal.

- **base_frequency_range** (`tuple` of `float`):  
  Frequency range for the replacement signal.

---

### Returns  

- **warped_wave** (`numpy.ndarray`):  
  The time-warped waveform.

---

### Usage Example  
```python
warped_wave = svg.apply_time_warp(wave, 0.1, t, 5, (0.1, 1.0), (10, 100))
```
