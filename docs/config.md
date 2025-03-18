## `config`

**Location:** `config.py`

---

## Description  
The `config.py` file provides **predefined parameter configurations** for **signal variations, noise modulation, and device-specific frequency ranges**. It defines **parameter sweeps, noise functions, and device constraints**, enabling realistic **signal augmentation and synthetic dataset generation**.

This configuration allows for:
- **Device-Specific Signal Ranges:** Defines the **frequency and amplitude constraints** for various **embedded devices, sensors, and communication systems**.
- **Parameter Sweeps:** Provides **preset variation ranges** for different transformation operations like **time shifts, gain variations, amplitude modulation, and baseline drift**.
- **Noise Functions:** Specifies **different types of envelopes** for **modulating noise over time**.
- **Noise Power and Modulation Factor Levels:** Predefined **scaling factors** for **controlling noise intensity and variability** across experiments.

---

## Embedded Device Frequency and Amplitude Ranges  
The `EMBEDDED_DEVICE_RANGES` dictionary contains **predefined amplitude and frequency constraints** for different embedded systems. These constraints ensure that **generated signals remain realistic within the operational bounds of the target device**.

### Examples:
| Device | Amplitude (V) | Frequency (Hz) |
|---------|--------------|----------------|
| **Arduino Board** | (0, 5) | (0, 12e3) |
| **Drones** | (0, 1) | Control: (2.398e9, 2.402e9) |
| **Cameras** | (0, 1) | (24, 120) (Frames per second) |
| **Smartphones** | (0, 1) | LTE: (699e6, 701e6), 5G: (38.9e9, 39.1e9) |
| **Wi-Fi Routers** | (0, 1) | WiFi 2.4 GHz: (2.395e9, 2.405e9) |
| **Smart Watches** | (0, 0.9e-3) | (2.398e9, 2.402e9) |

These **ranges ensure** that generated signals for **augmentation or simulation** remain within the **physical constraints of real-world embedded systems**.

---

## Parameter Sweeps  
The `param_sweeps` dictionary defines **predefined transformation parameters** for **different device types**. These parameters **control variations** in time shift, warping, gain, and baseline drift, allowing for **customized augmentation** of signals.

### Example: **Cameras**
| Transformation | Range |
|---------------|--------|
| `time_shift` | [1, 51, 101, 151, 201, 251, 301] |
| `time_warp` | [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07] |
| `gain_variation` | [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] |
| `baseline_drift_region` | [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4] |

### Example: **Arduino Board**
| Transformation | Range |
|---------------|--------|
| `time_shift` | [1, 51, 101, 151, 201, 251, 301] |
| `time_warp` | [0, 0.06, 0.12, 0.18] |
| `gain_variation` | [0, 0.1, 0.2, 0.3, 0.4] |
| `baseline_drift` | [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0] |

These **parameter sweeps** allow **systematic variations** in **signal transformations**, ensuring realistic **data augmentation for different device categories**.

---

## Noise Functions  
The `noise_funcs` list defines **envelope-based noise modulation** functions, controlling **how noise evolves over time**.

### Available Noise Envelopes:
| Function | Description |
|----------|------------|
| **None** | No modulation (stationary noise). |
| **envelope_linear** | Gradual increase/decrease in noise intensity. |
| **envelope_sine** | Cyclic noise modulation with sinusoidal fluctuations. |
| **envelope_random_walk** | Stochastic amplitude variations (random walk process). |
| **envelope_blockwise** | Step-like changes in noise amplitude (intermittent bursts). |

These **modulation functions** allow for **non-stationary noise effects**, making simulations **more realistic** for machine learning and signal processing applications.

---

## Noise Power and Modulation Factor Levels  
### `npw_levels`: Noise Power Scaling  
Defines **noise power variation ranges**, allowing for **controlled randomness** in noise intensity through different measurements.

| Level | Range |
|--------|--------|
| 1 | [1, 1] (No variation) |
| 2 | [0.9, 1.1] |
| 3 | [0.85, 1.2] |
| 4 | [0.8, 1.3] |
| 5 | [0.75, 1.4] |
| 6 | [0.7, 1.5] |
| 7 | [0.65, 1.6] |
| 8 | [0.6, 1.7] |

### `mf_levels`: Modulation Factor Scaling  
Controls **random fluctuations in signal amplitude**, adding variability to synthetic signals through different measurements.

| Level | Range |
|--------|--------|
| 1 | [0.75, 0.85] |
| 2 | [0.8, 0.9] |
| 3 | [1, 1] (No variation) |
| 4 | [1.0, 1.1] |
| 5 | [1.0, 1.2] |

These levels **introduce realistic signal fluctuations**, making augmented data **more robust and diverse**.

---

## Summary  
The `config.py` file **defines parameter constraints** for **signal transformations, noise modeling, and device-specific characteristics**. It provides:
1. **Device-Specific Ranges:** Ensuring generated signals stay within **real-world constraints**.
2. **Parameter Sweeps:** Predefined **ranges for augmentations** like **time shifts, warping, and gain variation**.
3. **Noise Functions:** **Modulation techniques** for introducing **realistic noise evolution**.
4. **Noise Power & Amplitude Modulation Levels:** **Randomized variability controls** for robust signal augmentation.
