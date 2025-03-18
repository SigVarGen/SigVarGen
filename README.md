# SigVarGen: Synthetic Signal Variation Generator

SigVarGen is a Python framework designed to create **multiple variants** of a base **1D signal** under the same environmental conditions. It allows the simulation of both **idle-state signals** and signals affected by **external perturbations**, enabling robust testing of algorithms in dynamic environments based on multiple measurements of the same event. Framework is suitable for **time-series analysis**, **signal processing**, and **synthetic data generation** in various domains such as sensor data modeling, embedded systems testing, and machine learning.

- **Documentation**: [Documentation Site](https://sigvargen.github.io/SigVarGen/)
- **Functions Overview**: [Modules](https://sigvargen.github.io/SigVarGen/modules/)
- **Tutorials**: [Tutorials](./tutorials)
- **Contributing**: [Contributing Guidelines](./doc/contributing.md)
- **Bug reports:**: [Issues](https://github.com/SigVarGen/SigVarGen/issues)


---

## Key Features

- **Signal Generation**: Synthesizes complex 1D signals by combining multiple sinusoidal components, providing realistic baseline idle signals.
- **Interrupting Signal Generation, Scheduling and Addition**: Synthesizes interrupting 1D signal and blend into original signal, mimicking real-world anomalies such as sensor glitches, external perturbations, or event-driven variations.
- **Variation and Augmentation**: Generates diverse signal variants by systematically altering signal parameters and applying a range of transformations, such as time shifting, warping, gain variation, amplitude modulation, and baseline drift.
- **Noise Generation and Addition**: Supports the addition of various types of noise (e.g., white / colored, and stationary / non-stationary noise) to the generated signals, mimicking real-world interference.

---

## Installation

SigVarGen is compatible with Python 3.8 and above. To install the framework, simply use pip:

(in progress)
```bash
pip install SigVarGen
```

Alternatively, clone the repository and install using:

```bash
git clone https://github.com/SigVarGen/SigVarGen.git
cd SigVarGen
pip install ./
```

---

## Key Examples

For hands-on examples and tutorials, please refer to the [tutorials](./tutorials) folder. The tutorials demonstrate:
- Generating idle signals and signals with interrupts using the signal generation module.
- Applying variations and augmentations to simulate realistic signal perturbations.
- Generating different noise types and integration into signal.
- Generating periodic and semi-periodic background activity.
- Generating datasets with different types of noise.

---

## Documentation

Comprehensive documentation is available on our [documentation site](https://github.io). The documentation covers:
- Algorithms used in complex functions. 
- Detailed description and code snippets.
- Best practices for integrating SigVarGen with your data processing pipelines.

---

## Module Overview

### Main Modules
- **Signal Generation**: Implements functions for synthesizing complex signals by summing sinusoidal components, and introduces logic for custom interrupting signals.
- **Variation and Augmentation**: Provides tools for systematic parameter variation and signal transformation, including time shifts, warping, amplitude modulation, and baseline drift.
- **Noise Generation and Addition**: Contains functions to generate various noise types and to integrate noise into synthetic signals, emulating real-world conditions.

### Helper Modules
- **Configure**: Contains example parameters for device ranges, variation functions, and noise modulation envelopes.
- **Utils**: Provides common utility functions such as Euclidean distance calculation, normalization, interpolation, and dividing device parameters into subranges for idle periods or in response to events.
- **Datasets**: Short samples from previously generated datasets.

---

## Contributing

We welcome contributions from the community! If you wish to contribute to SigVarGen, please:
- Fork the repository.
- Create a new branch for your feature or bugfix.
- Submit a pull request with detailed information about your changes.

For more information, please refer to our [Contributing Guidelines](./doc/contributing.md).

---

## License

SigVarGen is released under the [MIT License](./LICENSE). Please see the LICENSE file for details.

---

## Acknowledgements

This framework originated as part of my **master’s research at the Real-time Embedded Systems Lab, University of Waterloo**, where two years were dedicated to its development, refinement, and validation. The project has since evolved into an open-source initiative. I am grateful to my professor and friends, who supported me throughout this journey. I am also thankful to the Natural Sciences and Engineering Research Council of Canada, which supported my research at the University of Waterloo. 

We extend our thanks to the contributors and the open-source community for their invaluable support and feedback. Additionally, we acknowledge the **authors of related works** whose research and methodologies provided theoretical and practical foundations for various components of this project. In particular, we recognize the contributions of:  

- **Van Drongelen** (*Signal Processing for Neuroscientists*, Academic Press, 2018) [1] for introduction into signal processing,  
- **Haslwanter** (*Hands-on Signal Analysis with Python*, Springer, 2021) [2] for practical examples of Python implementations,  
- **Esakkirajan et al.** (*Digital Signal Processing: Illustration Using Python*, Springer, 2024) [3] for expanding practical and theoretical principles for signal processing,  
- **Mitrović et al.** (*Advances in Computers: Improving the Web*, Elsevier, 2010) [4] for their noise generation approach.  

For inquiries or support, please contact **[ovakulenko@uwaterloo.ca]**.

---

## References  

1. **Van Drongelen, W.** (2018). *Signal Processing for Neuroscientists*. Academic Press.  
2. **Haslwanter, T.** (2021). *Hands-on Signal Analysis with Python*. Springer.
3. **Esakkirajan, S., Veerakumar, T., & Subudhi, B. N.** (2024). *Digital Signal Processing: Illustration Using Python*. Springer.
4. **Mitrović, D., Zeppelzauer, M., & Breiteneder, C.** (2010). "Features for Content-Based Audio Retrieval." *Advances in Computers: Improving the Web* (Vol. 78), Elsevier, pp. 71-150.  

---

SigVarGen is dedicated to advancing the field of synthetic signal generation by providing a robust, flexible, and extensible toolkit for academic and industrial applications. Happy coding!

