## **`generate_parameter_variations`**

**Location:** `variations/variations.py`

---

## **Description**
`generate_parameter_variations` creates **randomized parameter sets** to produce multiple **signal variants**. By selecting subranges of parameter values around randomly chosen center points, the function introduces systematic yet stochastic variability, simulating real-world signal inconsistencies.

This function is useful for parameter space exploration, enabling controlled data augmentation for testing signal processing algorithms, improving machine learning model robustness, and simulating measurement variability in synthetic datasets.

---

### **Notes**
- Each parameter's values are sampled from a **randomly chosen subrange** within the provided range (`param_sweeps`).
- The function supports **multiple signal variants**, ensuring **diverse augmentations**.
- Includes **randomized frequency bounds (`f_min`, `f_max`)** to introduce **local modifications**.
- The **`wave_with_score`** parameter allows integration with the `transform_wave_with_score` function, enabling **controlled waveform substitution**.

---

### **Parameters**

- **param_sweeps** (`dict`):  
  Dictionary where keys represent parameter names, and values are arrays of possible values to select from.

- **num_variants** (`int`, optional):  
  Number of unique **parameter sets** to generate.  
  **Default:** `5`.

- **window_size** (`int`, optional):  
  Half-width of the subrange selected around a center point for each parameter.  
  **Default:** `1`.

---

### **Returns**

- **variations** (`list` of `dict`):  
  A list where each entry is a dictionary containing randomized parameter selections for one signal variant.

---

### **Usage Example**
```python
import numpy as np
import SigVarGen as svg

# Define parameter sweep ranges
param_sweeps = {
    "amplitude_range": np.linspace(0.1, 1.0, 10),
    "frequency_range": np.linspace(10, 100, 10),
    "modulation_depth": np.linspace(0.2, 0.8, 5),
}

# Generate 3 parameter variations with a window size of 2
parameter_sets = svg.generate_parameter_variations(param_sweeps, num_variants=3, window_size=2)

for i, params in enumerate(parameter_sets):
    print(f"Variant {i+1}: {params}")
```
