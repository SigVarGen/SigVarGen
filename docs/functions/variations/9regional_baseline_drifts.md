# Regional baseline drifts

These functions introduce different baseline drift behaviors, allowing for localized  piecewise, polynomial, or middle-peak drifts. 

## `apply_baseline_drift_region`

**Location:** `variations/baseline_drift.py`

---

## Description  
`apply_baseline_drift_region` introduces **localized baseline drift** in a specific segment of a waveform.

---

### Notes  
- Drift is applied **only within a selected fraction of the signal**, defined by `start_frac` and `end_frac`.  
- Outside this region, the **original waveform remains unchanged**.  
- Uses **linear interpolation** for smooth transition within the drift region.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input signal.

- **max_drift** (`float`):  
  Maximum amplitude of the drift.

- **start_frac** (`float`, optional):  
  Fractional position where the drift starts (`0.3` = 30% into the signal).  
  **Default:** `0.3`.

- **end_frac** (`float`, optional):  
  Fractional position where the drift ends (`0.7` = 70% into the signal).  
  **Default:** `0.7`.

---

### Returns  

- **drifted_wave** (`numpy.ndarray`):  
  The waveform with **localized baseline drift**.

---

### Usage Example  
```python
import SigVarGen as svg

drifted_wave = svg.apply_baseline_drift_region(wave, max_drift=0.2, start_frac=0.4, end_frac=0.8)
```

---

## `apply_baseline_drift_polynomial`

**Location:** `variations/baseline_drift.py`

---

## Description  
`apply_baseline_drift_polynomial` introduces **a smooth, polynomial drift** across an entire signal. The drift **gradually increases or decreases**, making it ideal for **modeling slow environmental changes, power fluctuations, or long-term sensor drift**.

---

### Notes  
- Uses **polynomial scaling** (`order=2` by default, quadratic drift).  
- The **drift can be reversed**, causing it to start at the peak and return to zero.  
- A higher-order polynomial (e.g., `order=3`) introduces **nonlinear drift effects**.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input signal.

- **max_drift** (`float`):  
  Maximum amplitude of the drift.

- **reversed** (`bool`, optional):  
  If `True`, the drift **starts at its peak and decreases**.  
  **Default:** `False`.

- **order** (`int`, optional):  
  Polynomial order of the drift.  
  **Default:** `2` (quadratic).

---

### Returns  

- **drifted_wave** (`numpy.ndarray`):  
  The waveform with a **polynomial baseline drift**.

---

### Usage Example  
```python
drifted_wave = svg.apply_baseline_drift_polynomial(wave, max_drift=0.3, order=3)
```

---

## `apply_baseline_drift_piecewise`

**Location:** `variations/baseline_drift.py`

---

## Description  
`apply_baseline_drift_piecewise` introduces **stepwise drift changes**, where different sections of the waveform have **randomly varying baseline shifts**.

---

### Notes  
- Divides the waveform into **multiple segments**, each with an independent drift value.  
- The **drift values can be reversed**, starting from the maximum and decreasing.  
- The number of segments is controlled by `num_pieces`, with each piece having a **unique baseline level**.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input signal.

- **max_drift** (`float`):  
  Maximum amplitude of drift per segment.

- **reversed** (`bool`, optional):  
  If `True`, the drift **starts at its highest and gradually decreases**.  
  **Default:** `False`.

- **num_pieces** (`int`, optional):  
  Number of segments for the drift.  
  **Default:** `3`.

---

### Returns  

- **drifted_wave** (`numpy.ndarray`):  
  The waveform with **piecewise baseline drift**.

---

### Usage Example  
```python
drifted_wave = svg.apply_baseline_drift_piecewise(wave, max_drift=0.4, num_pieces=4)
```

---

## `apply_baseline_drift_middle_peak`

**Location:** `variations/baseline_drift.py`

---

## Description  
`apply_baseline_drift_middle_peak` applies a **parabolic drift that peaks in the middle of the waveform**. 

---

### Notes  
- Drift is **zero at the start and end**, with a peak at **the center of the signal**.  
- The peak can **shift downward or upward**, depending on the `direction`.  
- Works well for **short-term drift simulations**.

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input signal.

- **max_drift** (`float`):  
  Maximum amplitude of the drift.

- **direction** (`str`, optional):  
  - `'down'`: Peak drifts **downward** (negative shift).  
  - `'up'`: Peak drifts **upward** (positive shift).  
  **Default:** `'down'`.

- **min_drift** (`float`, optional):  
  Minimum drift value to **ensure drift is non-zero**.  
  **Default:** `0`.

---

### Returns  

- **drifted_wave** (`numpy.ndarray`):  
  The waveform with a **middle-peak baseline drift**.

---

### Usage Example  
```python
drifted_wave = svg.apply_baseline_drift_middle_peak(wave, max_drift=0.3, direction='up')
```

