## `add_complexity_to_inter`

**Location:** `signal/response_signals.py`

## Description

`add_complexity_to_inter` introduces an overlapping (secondary) interrupt within an existing main interrupt region. This function selects a portion of the `full_interrupt_signal`, applies optional modifications such as amplitude drift and offset adjustments, and blends it into the `base_signal`. The added complexity simulates realistic signal variations, making it useful for applications where multiple overlapping perturbations are expected.

This function is designed to be called within `add_main_interrupt` when `complex_iter > 0`, ensuring multiple layers of interruptions within a base signal.

---

### Parameters

- **base_signal** (`numpy.ndarray`): The full base signal, which may already contain the main interrupt.  
- **full_interrupt_signal** (`numpy.ndarray`): The full-length interrupt signal from which a portion is extracted.  
- **start_main** (`int`): The start index of the main interrupt.  
- **end_main** (`int`): The end index of the main interrupt.  
- **domain** (`str`): The key used to access amplitude and frequency ranges in `INTERRUPT_RANGES`.  
- **DEVICE_RANGES** (`dict`): A dictionary containing overall amplitude and frequency limits for the device.  
- **INTERRUPT_RANGES** (`dict`): A dictionary containing predefined amplitude and frequency ranges for each domain.  
- **drop** (`bool`):  
  - If `True`, the interrupt offset is adjusted downward.  
  - If `False`, the interrupt offset is adjusted upward.  
- **old_offset** (`float`): The offset applied to the main interrupt, which can be used for reference in secondary modifications.  
- **sinusoids_params** (`dict` or `list`): Metadata describing how the main interrupt was generated.  
- **blend_factor** (`float`, optional):  
  - The blending weight between the base and interrupt signal (default: `0.5`).  

---

### Returns

- **updated_base_signal** (`numpy.ndarray`): The modified base signal after adding the overlapping interrupt.  
- **interrupt_params** (`dict`): Metadata describing the added secondary interrupt, including:
  - `start_idx` (`int`): The start index of the overlapping interrupt.
  - `duration_idx` (`int`): The duration of the interrupt in samples.
  - `offset` (`float`): The applied amplitude offset.
  - `sinusoids_params` (`dict` or `list`): Parameters used to generate the secondary interrupt.
  - `type` (`str`): `"main_overlapping"` to indicate a secondary interrupt within the main one.
