# **Noise Module**

The **Noise Module** provides methods for generating and adding noise to signals, enabling the simulation of realistic noisy environments for signal processing applications. Noise is an inherent part of real-world signals, originating from various sources such as electronic interference, environmental fluctuations, or stochastic variations in a system. In many cases, noise is considered an undesirable artifact that must be reduced or removed. However, noise can also carry valuable information about the system’s state or environment.

The module supports **stationary** and **non-stationary** noise models, including:

- **Colored noise synthesis** (white, pink, and brown).
- **Time-varying noise envelopes** (linear, sinusoidal, random walk, and blockwise modulation).
- **Controlled noise injection** using signal-to-noise ratio (SNR) scaling.

These methods allow users to introduce **realistic noise patterns** into their signals, useful for **testing denoising algorithms, training machine learning models, and modeling real-world scenarios**.

---

## **Conceptual Overview**

### **Understanding Noise Characteristics**

Noise can be broadly classified into **stationary** and **non-stationary** types:

- **Stationary Noise:** Statistical properties (e.g., variance, mean, and spectral density) remain constant over time.  
  Examples: Thermal noise in electrical circuits, Gaussian noise in images.  

- **Non-Stationary Noise:** Statistical properties vary over time, often due to changing environmental factors or system dynamics.  
  Examples: Wind noise in microphones, motion artifacts in biomedical signals.

Many natural noise sources follow a **power-law spectral density**, where spectral power decreases as a function of frequency. This principle, observed in fractal and chaotic systems, is the basis for colored noise synthesis.

### **Colored Noise Synthesis**

The **Noise Module** implements a **Fourier-based noise synthesis method**, introduced by Poul Bourke (1997), which follows these steps:

1. Generate a **white noise** sequence in the time domain.
2. Transform the noise into the **frequency domain** using the Fourier transform.
3. Apply a **spectral filter** to shape the noise power based on the desired frequency-dependent function \( 1/f^p \).
4. Perform an **inverse Fourier transform** to reconstruct the time-domain noise.

This approach allows the generation of **different noise types**:

- **White noise (\( p=0 \))** → Equal power at all frequencies.
- **Pink noise (\( p=1 \))** → Power decreases as \( 1/f \), common in biological signals.
- **Brown noise (\( p=2 \))** → Power decreases as \( 1/f^2 \), with stronger low-frequency components.

$$
S(f) \propto \frac{1}{f^p},
$$
where \( S(f) \) represents the spectral power density and \( p \) determines the noise color.

### **Envelope-Based Noise Modulation**

To introduce **non-stationary noise effects**, the module supports **four amplitude modulation envelopes**:

1. **Linear Envelope** → Gradually increases or decreases noise intensity over time.
2. **Sine Envelope** → Modulates noise amplitude periodically, introducing cyclic variations.
3. **Random Walk Envelope** → Introduces stochastic amplitude changes, simulating unpredictable real-world fluctuations.
4. **Blockwise Envelope** → Produces abrupt, step-like noise intensity variations.

These envelopes enable **controlled noise dynamics**, making the generated noise adaptable to **real-world non-stationary environments**.

---

## **References**

1. Celka, P. (2006). *Smoothly Time-Varying AR Models and Applications in Biomedical Signal Processing*.  
2. Vaseghi, S. (2008). *Advanced Digital Signal Processing and Noise Reduction*. Wiley.  
3. Bourke, P. (1997). *Frequency Synthesis of Landscapes (and Clouds)*.  
4. Mitrovic, D. et al. (2010). *Analysis and Generation of Synthetic Colored Noise for Machine Learning Applications*.  
