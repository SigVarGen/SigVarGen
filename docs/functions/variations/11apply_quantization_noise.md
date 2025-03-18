## `apply_quantization_noise`

**Location:** `variations/transformations.py`

---

## Description  
`apply_quantization_noise` simulates quantization effects that occur when a continuous signal is converted into a digitized form. This function reduces the bit depth of a waveform, introducing quantization noise, which is commonly encountered in low-resolution ADCs (Analog-to-Digital Converters).

---

### Notes  
- Lower **`num_bits`** results in more quantization noise, reducing signal fidelity.  
- The function scales and rounds the waveform based on the number of quantization levels.  

---

### Parameters  

- **wave** (`numpy.ndarray`):  
  The input waveform to be quantized.

- **num_bits** (`int`):  
  Number of bits for quantization.  
  - **Higher values** (e.g., `16-bit, 24-bit`) → Less noise, better resolution.  
  - **Lower values** (e.g., `4-bit, 8-bit`) → More distortion, reduced accuracy.

---

### Returns  

- **quantized_wave** (`numpy.ndarray`):  
  The **digitally quantized** version of the input waveform.

---

### Usage Example  
```python
import SigVarGen as svg

# Generate a sine wave and apply 8-bit quantization
quantized_wave = svg.apply_quantization_noise(wave, num_bits=2)
```
