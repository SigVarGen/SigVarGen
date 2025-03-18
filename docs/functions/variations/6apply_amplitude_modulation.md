## `apply_amplitude_modulation`

**Location:** `variations/transformations.py`

---

## Description  
`apply_amplitude_modulation` introduces **periodic variations** in a waveform's amplitude using **sinusoidal modulation**. This transformation simulates **oscillatory changes in signal intensity**, such as **fading, interference, or natural rhythmic fluctuations**.

---

### Notes  
- The **modulation depth** controls the strength of the amplitude variations.  
- Uses a **random modulation frequency** within `[0.1, 1.0] Hz`.  
- The **original signal is preserved**, with only its amplitude varying over time.  

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform.

- **modulation_depth** (`float`):  
  Strength of amplitude modulation.

---

### Returns  

- **modulated_wave** (`numpy.ndarray`):  
  The amplitude-modulated waveform.

---

### Usage Example  
```python
modulated_wave = svg.apply_amplitude_modulation(wave, 0.5)
```