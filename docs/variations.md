# **Variations Module**

The **Variations Module** provides transformations that introduce controlled distortions in time, amplitude, and baseline characteristics of a signal. These transformations simulate real-world variations encountered in repeated measurements due to environmental dynamics, sensor drift, and system instabilities. By incorporating parameter space exploration, this module ensures a systematic and randomized approach to generating diverse signal variants.

The module is essential for robust testing of signal processing algorithms, particularly in machine learning, adaptive filtering, and anomaly detection, where real-world data is often subject to dynamic changes.

---

## **Conceptual Overview**

### **Simulating Measurement Variability**

In real-world signal acquisition, repeated measurements of the same event often differ due to internal system variations, environmental factors, or sensor-specific perturbations. These variations can be global (affecting the entire signal)** or localized (affecting only certain segments of the signal). The Variations Module captures these effects through two key processes:

1. **Parameter-Based Transformations**  
   The `generate_parameter_variations` function selects randomized parameter values from predefined ranges to simulate natural signal variations across multiple measurements.

2. **Signal Transformations**  
   The `generate_variation` function applies a **sequence of transformations**, including:
   - **Time distortions** (shifting, warping)
   - **Amplitude variations** (gain changes, modulation)
   - **Baseline drift** (global, regional, and polynomial-based shifts)
   - **Localized distortions** (temporary amplitude changes, quantization noise)
   - **Wave Transformation with Score-Based Replacement** (controlled signal modification)

These transformations allow for the realistic augmentation of time-series data, making them well-suited for data augmentation, robustness testing, and synthetic dataset generation.

---

### **Time-Based Variations**
Time-domain transformations **modify the timing or structure** of the signal to simulate **sensor delays, data misalignment, or speed variations**.

- **Time Shift:** Circularly shifts the waveform within a defined interval, mimicking synchronization errors or acquisition delays.
- **Time Warp:** Non-linearly compresses or expands parts of the signal to replicate **speed variations** or **non-uniform time distortions**.

### **Amplitude-Based Variations**
Amplitude transformations **alter signal intensity** to model **sensor gain fluctuations, environmental effects, or periodic modulation**.

- **Gain Variation:** Randomly scales the waveform amplitude to simulate **variable sensor sensitivity**.
- **Amplitude Modulation:** Applies a sinusoidal modulation effect, replicating **cyclic variations** in signal intensity.

### **Baseline Drift Variations**
Baseline drift introduces **long-term shifts** in the signal, reflecting **slowly changing environmental factors or sensor drift**.

- **Global Drift:** Affects the entire signal with a **linear or polynomial trend**.
- **Regional Drift:** Applies drift only to specific sections of the signal, simulating **localized sensor instability**.
- **Middle Peak Drift:** Introduces a **centered peak shift**, modeling temporary disturbances.

### **Wave Transformation with Score-Based Replacement**
- **Transform Wave with Score:** Replaces parts of the original waveform with segments of newly generated signals based on a predefined probability. This allows controlled **localized waveform modification**, making it useful for simulating partial signal corruption, data loss, or adaptive feature modification in real-world signals.
