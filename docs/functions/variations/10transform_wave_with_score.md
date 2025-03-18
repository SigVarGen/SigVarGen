## `transform_wave_with_score`

**Location:** `variations/transformations.py`

---

## Description  
`transform_wave_with_score` replaces **segments of a waveform** with newly generated signal portions based on a **score-controlled probability**. This function is useful for **simulating signal corruption, feature substitution, or change in activity through different measurements**.

---

### Notes  
- The function **generates a replacement signal** using `generate_signal()`.  
- The **number and size of replacement segments** depend on the `score` value.  
- Substitution is **avoided within predefined interrupt regions**, ensuring that **important waveform segments remain intact**.

---

### Parameters  

- **original_wave** (`numpy.ndarray`):  
  The input waveform.

- **score** (`float`):  
  A factor controlling **how much of the waveform is transformed**.  
  - Higher values → More segments replaced.  
  - Lower values → Less transformation.

- **t** (`numpy.ndarray`):  
  Time vector for generating the replacement signal.

- **n_sinusoids** (`int`):  
  Number of sinusoids in the **generated replacement signal**.

- **amplitude_range** (`tuple` of `float`):  
  Amplitude range for the replacement signal.

- **base_frequency_range** (`tuple` of `float`):  
  Frequency range for the replacement signal.

- **interrupt_params** (`list` of `dict`):  
  List of dictionaries defining **interrupt regions** that should not be replaced.  
  Example: `[{'start_idx': 100, 'duration_idx': 50}]`.

---

### Returns  

- **transformed_wave** (`numpy.ndarray`):  
  The modified waveform with **score-based segment replacement**.

---

### Usage Example  
```python
transformed_wave = svg.transform_wave_with_score(
    wave, 0.5, t, n_sinusoids=10, 
    amplitude_range=(0,1), base_frequency_range=(70, 75), 
    interrupt_params=[{'start_idx': 200, 'duration_idx': 50}]
)
```