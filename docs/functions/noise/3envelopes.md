## **Envelopes for Noise Modulation**

The **envelope functions** in the **Noise Module** modify the amplitude of noise signals over time, simulating real-world non-stationary noise patterns. These functions introduce **gradual or abrupt variations** in noise intensity, making the generated noise more realistic for applications in **signal processing, machine learning, and system testing**.

Each envelope function follows a unique pattern:
- **Linear:** Gradual increase or decrease in noise amplitude.
- **Sine:** Periodic oscillations in amplitude.
- **Random Walk:** Stochastic variations mimicking unpredictable changes.
- **Blockwise:** Sudden step-like changes in amplitude.

These envelopes allow **dynamic control** over noise behavior, enhancing the realism of simulated noisy environments.

---

## **Envelope Functions Overview**

### **`envelope_linear`**

**Location:** `noise/envelopes.py`

#### **Description**
`envelope_linear` generates a **linearly changing amplitude envelope**, transitioning smoothly between two defined noise power levels. Depending on the `param` value, the envelope either **ramps up** or **ramps down** over time.

#### **Parameters**
- **num_samples** (`int`):  
  Number of samples in the envelope (must match the signal length).
- **npw** (`tuple` of `float`):  
  `(min, max)` range of noise power values.
- **param** (`float`):  
  Controls the direction of the transition:  
  - `> 0.5` → Increasing envelope.  
  - `≤ 0.5` → Decreasing envelope.

#### **Returns**
- **envelope** (`numpy.ndarray`):  
  Linearly increasing or decreasing amplitude envelope.

#### **Example**
```python
import numpy as np
import SigVarGen as svg

env = svg.envelope_linear(num_samples=1000, npw=(0.1, 1.0), param=0.7)
print(env[:10])  # First 10 values of the envelope
```

---

### **`envelope_sine`**

**Location:** `noise/envelopes.py`

#### **Description**
`envelope_sine` applies **periodic modulation** to noise amplitude, creating fluctuations that mimic oscillatory environmental effects. This envelope is particularly useful for **simulating periodic disturbances** such as wind noise or cyclic variations in signal intensity.

#### **Parameters**
- **num_samples** (`int`):  
  Number of samples in the envelope.
- **npw** (`tuple` of `float`):  
  `(min, max)` range of noise power values.
- **param** (`float`, optional, default=`0.005`):  
  Frequency of oscillations (lower values result in slower oscillations).

#### **Returns**
- **envelope** (`numpy.ndarray`):  
  Sine wave-modulated amplitude envelope.

#### **Example**
```python
env = svg.envelope_sine(num_samples=1000, npw=(0.1, 1.0), param=0.01)
print(env[:10])  # First 10 values of the envelope
```

---

### **`envelope_random_walk`**

**Location:** `noise/envelopes.py`

#### **Description**
`envelope_random_walk` generates a **stochastic amplitude envelope**, where the noise power follows a **random walk** pattern. This mimics **unpredictable fluctuations** observed in real-world signals, such as biological noise or varying environmental conditions.

#### **Parameters**
- **num_samples** (`int`):  
  Number of samples in the envelope.
- **npw** (`tuple` of `float`):  
  `(min, max)` range of noise power values.
- **param** (`float`, optional, default=`0.01`):  
  Standard deviation of the random step size (higher values cause more variability).
  Higher value results in higher amplitude, which might be clipped.

#### **Returns**
- **envelope** (`numpy.ndarray`):  
  Stochastically varying amplitude envelope.

#### **Example**
```python
env = svg.envelope_random_walk(num_samples=1000, npw=(0.1, 1.0), param=0.02)
print(env[:10])  # First 10 values of the envelope
```

---

### **`envelope_blockwise`**

**Location:** `noise/envelopes.py`

#### **Description**
`envelope_blockwise` applies **stepwise variations** in noise power, creating **block-like intensity changes**. This is useful for simulating **sudden shifts in noise levels**, such as network congestion bursts or machine noise variations.

#### **Parameters**
- **num_samples** (`int`):  
  Number of samples in the envelope.
- **npw** (`tuple` of `float`):  
  `(min, max)` range of noise power values.
- **param** (`int`, optional, default=`100`):  
  Block size (number of samples per step).

#### **Returns**
- **envelope** (`numpy.ndarray`):  
  Stepwise amplitude envelope.

#### **Example**
```python
env = svg.envelope_blockwise(num_samples=1000, npw=(0.1, 1.0), param=50)
print(env[:10])  # First 10 values of the envelope
```
