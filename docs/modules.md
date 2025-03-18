# Modules Overview

The SigVarGen framework is modular, promoting clarity, maintainability, and scalability. It comprises the following modules:

- **[Signal](signal.md)**: Base signal generation, interruptions generation and scheduling, periodic and semi-periodic events.
- **[Noise](noise.md)**: Noise generation, modeling and addition.
- **[Variations](variations.md)**: Augmentation techniques such as baseline drift, time warping, and modulation.
- **[Configuration](config.md)**: Parameter examples for signal generation, noise modelling and chained augmentation.
- **[Utils](utils.md)**: Auxiliary functions for signal normalization, metric calculation, and device parameter generation.

---

## **Signal Module Functions Hierarchy Overview**

The table below illustrates the relationships between the functions of signal generation. Main functions for this module are `generate_signal` and `add_interrupt_with_params`.

| Level         | Function Name                  | Role & Dependencies |
|--------------|--------------------------------|-----------------------------------------------|
| **High-Level (Wrappers)** | `add_interrupt_with_params`  | Master function managing all interruptions. Calls `add_main_interrupt`, `add_smaller_interrupts` |
| | `add_main_interrupt`  | Inserts the main interrupt. Calls `generate_main_interrupt`, `place_interrupt`, `apply_interrupt_modifications`, `blend_signal`, `add_complexity_to_inter` |
| | `add_smaller_interrupts`  | Adds secondary small interrupts. Calls `generate_main_interrupt`, `place_interrupt`, `apply_interrupt_modifications`, `blend_signal` |
| | `add_interrupt_bursts`  | Adds multiple small bursts. Calls `generate_signal`, `place_interrupt`, `blend_signal` |
| | `add_periodic_interrupts`  | Adds periodic interruptions to a signal. Calls `generate_semi_periodic_signal` |
| **Mid-Level (Core Operations)** | `generate_main_interrupt` | Generates sinusoidal-based interruptions. Calls `generate_signal` |
| | `place_interrupt` | Finds placement indexes. Calls `get_non_overlapping_interval` if needed |
| | `apply_interrupt_modifications` | Modifies an interrupt (amplitude shift, drift). Calls `apply_baseline_drift_middle_peak` if `disperse=True` |
| | `add_complexity_to_inter` | Inserts small overlapping interruptions into the main interrupt |
| | `generate_semi_periodic_signal` | Generates a semi-periodic binary signal with random bit flips |
| **Low-Level (Utilities)** | `generate_signal` | Creates multi-sinusoidal signals |
| | `blend_signal` | Merges base and interrupt signals. Used across multiple functions |
| | `get_non_overlapping_interval` | Ensures new interruptions do not overlap |

---

## **Noise Module Functions Hierarchy Overview**  

The main functions for noise module are `add_colored_noise` and `generate_noise_power`, which enable controlled noise injection and spectral shaping.

| Level         | Function Name                  | Role & Dependencies |
|--------------|--------------------------------|-----------------------------------------------|
| **High-Level (Wrappers)** | `add_colored_noise` | Generates and adds noise with a specific spectral profile (white, pink, or brown) to a signal. Can apply an envelope for non-stationary noise effects. |
| **Mid-Level (Core Operations)** | `generate_noise_power` | Computes noise power based on a selected SNR. Determines variance for controlled noise injection. |
| **Low-Level (Utilities)** | `envelope_linear` | Generates a linearly increasing or decreasing noise amplitude envelope. |
| | `envelope_sine` | Applies periodic modulation to noise amplitude using a sine wave. |
| | `envelope_random_walk` | Introduces stochastic variations in noise amplitude, simulating unpredictable fluctuations. |
| | `envelope_blockwise` | Creates stepwise variations in noise intensity, mimicking abrupt environmental changes. |

---

## **Variation Module Functions Hierarchy Overview**  

The variation module applies **time, amplitude and baseline transformations with segment substitution** to introduce realistic signal variations. The primary functions are `generate_variation` and `generate_parameter_variations`, which manage systematic augmentation of signals through transformations.

| Level         | Function Name                  | Role & Dependencies |
|--------------|--------------------------------|-----------------------------------------------|
| **High-Level (Wrappers)** | `generate_variation` | Applies a sequence of transformations (time shifts, warping, amplitude modulation, drift) to create signal variations. Depends on multiple transformation functions. |
| | `generate_parameter_variations` | Generates randomized parameter sets for transformations, ensuring controlled variability across multiple signal instances. |
| **Mid-Level (Core Transformations)** | `apply_time_shift` | Introduces a random time delay or advance in the waveform. |
| | `apply_time_warp` | Modifies the time axis non-linearly, stretching or compressing signal segments. |
| | `apply_gain_variation` | Adjusts signal amplitude by applying a multiplicative gain factor. |
| | `apply_amplitude_modulation` | Introduces periodic amplitude changes across the full signal. |
| | `apply_amplitude_modulation_region` | Modulates amplitude only within a specified signal region. |
| **Low-Level (Baseline Drift Operations)** | `apply_baseline_drift` | Adds a global linear drift to the waveform, simulating gradual baseline shifts. |
| | `apply_baseline_drift_region` | Introduces localized baseline drift within a specific segment of the waveform. |
| | `apply_baseline_drift_middle_peak` | Creates a baseline drift that peaks at the center of the signal. |
| | `apply_baseline_drift_polynomial` | Applies a polynomial baseline drift across the signal for nonlinear baseline changes. |
| | `apply_baseline_drift_piecewise` | Introduces stepwise changes in baseline level across different signal segments. |
| **Low-Level (Segment Transformations)** | `transform_wave_with_score` | Replaces parts of a signal with newly generated segments based on a probability score. |
| **Low-Level (Noise & Quantization)** | `apply_quantization_noise` | Simulates digital quantization effects by reducing bit depth, introducing quantization noise. |

## **Utilities Module Functions Hierarchy Overview**  

The **utils module** contains **general-purpose signal processing functions** used for normalization, interpolation, and metric calculations.

| Level | Function Name | Role & Dependencies |
|--------|----------------------|------------------------------------------------|
| **High-Level (Device Parameter Processing)** | `generate_device_parameters` | Splits device frequency and amplitude constraints into two distinct ranges for controlled simulations. |
| **Mid-Level (Metric Computation)** | `calculate_SNR` | Computes the signal-to-noise ratio (SNR) between a clean signal and a noisy version. |
| | `calculate_ED` | Computes the Euclidean distance (ED) between two signals. |
| **Low-Level (Signal Processing & Normalization)** | `interpoling` | Interpolates a signal to a target length, ensuring uniform sampling across signals. |
| | `normalization` | Standardizes a signal by centering it at zero mean and unit variance. |

---

## **Configuration Module Overview**  

The **config module** contains predefined **device-specific amplitude and frequency constraints** and **parameter sweep definitions** for signal variation experiments. It ensures **systematic parameter selection** across different devices and experimental conditions.

| Level | Parameter Set | Role & Details |
|--------|--------------------|-----------------------------------------------|
| **Device-Specific Constraints** | `EMBEDDED_DEVICE_RANGES` | Defines amplitude and frequency constraints for various embedded devices (Arduino, drones, cameras, IoT, automotive sensors, etc.). Ensures signal generation remains within realistic ranges. |
| **Experimental Parameter Sweeps** | `param_sweeps` | Defines parameter ranges for signal variations, including time shift, time warp, amplitude modulation, baseline drift, and gain variation. Allows controlled random selection of transformation parameters for signal augmentation. |
| **Noise Envelopes** | `noise_funcs` | Defines time-varying noise envelopes (linear, sine, random walk, and blockwise modulation) used to simulate non-stationary noise conditions. |
| **Noise Power Variation Levels** | `npw_levels` | Defines multiplicative noise power variations for added noise intensity fluctuations. |
| **Modulation Factor Levels** | `mf_levels` | Defines modulation factor variations, ensuring subtle randomized amplitude fluctuations in generated signals. |
