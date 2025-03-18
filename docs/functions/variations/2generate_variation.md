## **`generate_variation`**  

**Location:** `variations/variations.py`  

---

## **Description**  
`generate_variation` applies **a sequence of transformations** to a given waveform based on variant-specific parameters. This function enables systematic signal augmentation by introducing time shifts, time warping, amplitude modifications, and baseline drift, simulating realistic signal variations observed in biomedical signals, environmental measurements, and synthetic datasets.  

The function allows for controlled distortions by substituting segments of the signal, modifying timing characteristics, and adjusting amplitude properties.

---

### **Notes**  
- The function modifies the waveform incrementally, applying each transformation in sequence.
- **Waveform substitution (`wave_with_score`)** enables partial signal replacement.
- **Time-warping and time-shifting** introduce **timing irregularities**, mimicking **delays and non-uniform temporal distortions**.
- **Amplitude modifications** (gain variation and modulation) adjust signal intensity to reflect **sensor inconsistencies or environmental factors**.
- **Baseline drift transformations** simulate **slow signal shifts due to sensor degradation or environmental drift**.

---

### **Parameters**  

- **transformed_wave** (`numpy.ndarray`):  
  The waveform to be modified.

- **variant_params** (`dict`):  
  A dictionary containing transformation parameters. Expected keys:  
  `'time_shift'` → Amount of time shift applied.  
  `'time_warp'` → Factor for non-linear time distortion.  
  `'gain_variation'` → Multiplicative factor for global amplitude scaling.  
  `'amplitude_modulation'` → Strength of sinusoidal amplitude variation.  
  `'modulation_with_region'` → Localized amplitude modulation within a signal segment.  
  `'baseline_drift'` → Global baseline drift factor.  
  `'baseline_drift_region'` → Localized baseline drift applied within a fraction of the signal.  
  `'f_min'`, `'f_max'` → Start and end fractions defining localized transformations.  
  `'wave_with_score'` → Probability score for waveform substitution.  

- **t** (`numpy.ndarray`):  
  Time vector for the waveform.

- **n_sinusoids** (`int`):  
  Number of sinusoids in the **replacement signal** (used when `wave_with_score` is applied).

- **amplitude_range** (`tuple` of `float`):  
  Range for generating new **waveform segments** when replacing parts of the signal.

- **base_frequency_range** (`tuple` of `float`):  
  Frequency range for generating replacement signal segments.

- **interrupt_params** (`list` of `dict`):  
  List of regions defining interrupt locations in the signal, so wave with score will not substitute it.
  Example: `[{'start_idx': 100, 'duration_idx': 50}]`

---

### **Returns**  

- **transformed_wave** (`numpy.ndarray`):  
  The modified waveform after applying all transformations.

---

### **Usage Example**  
```python
import numpy as np
import SigVarGen as svg

# Generate a synthetic signal
t = np.linspace(0, 1, 1000)
wave = np.sin(2 * np.pi * 5 * t)
inter_params = [{'start_idx': 0, 'duration_idx': 0}]

# Define variation parameters
variant_params = {
    "time_shift": 20,
    "time_warp": 0.05,
    "gain_variation": 1.2,
    "amplitude_modulation": 0.4,
    "modulation_with_region": 0.3,
    "baseline_drift": 0.2,
    "baseline_drift_region": 0.15,
    "f_min": 0.1,
    "f_max": 0.8,
    "wave_with_score": 0.5
}

# Generate a signal variation
modified_wave = svg.generate_variation(
    wave, variant_params, t, 5, (0.1, 1.0), (10, 100), inter_params
)

print("Transformed Waveform Shape:", modified_wave.shape)
```