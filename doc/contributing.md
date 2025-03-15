# Contributing to **SigVarGen**  

Thank you for considering contributing to **SigVarGen**! We welcome contributions of all kinds, whether it's bug fixes, new features, documentation improvements, or general maintenance. This guide outlines how to contribute effectively to the project.

---

## 📌 **Issue Tracking & Discussion**
- Before submitting a **new feature request or bug report**, check if an issue already exists.
- Use labels (`bug`, `enhancement`, `documentation`, etc.) when opening issues.
- For questions, start a discussion in the **Discussions** tab.

---

## 📌 **Getting Started**  
### **1. Fork the Repository**  
1. Navigate to the **SigVarGen** repository:  
   ```bash
   git clone https://github.com/SigVarGen/SigVarGen.git
   cd SigVarGen
   ```
2. Create a new branch for your feature or fix:  
   ```bash
   git checkout -b feature-branch
   ```
3. Set up the development environment:  
   ```bash
   pip install -r requirements.txt
   ```

### **2. Make Your Changes**  
- Ensure code is well-structured, readable, and follows the project's style guidelines.
- Run tests before committing your changes:
   ```bash
   pytest tests/
   ```

### **3. Submit a Pull Request (PR)**  
1. Push your branch to your fork:  
   ```bash
   git push origin feature-branch
   ```
2. Open a **Pull Request** from GitHub’s UI.
3. Provide a clear **title** and **description** explaining the change.
4. Request a review from maintainers.
5. Ensure CI tests pass before merging.

---

## 📌 **Commit Message Guidelines**  

Use a structured **commit message format**:  
```
<COMMIT_TYPE>: <Short, descriptive summary>
```

### **Commit Types**
| Type     | Description |
|----------|------------|
| **FEAT** | Adding a new feature or enhancement. Example: `FEAT: Added baseline drift and vectorized signal generation` |
| **BUG**  | Bug fixes. Example: `BUG: Corrected frequency scaling bug` |
| **TEST** | Adding or modifying tests (without changing functionality). Example: `TEST: Added unit tests for place_interrupt()` |
| **DOC**  | Documentation updates. Example: `DOC: Updated README and added example notebook` |
| **CHORE** | General maintenance, refactoring, code style, config updates, or build/CI changes. Example: `CHORE: Reformatted with Black and updated CI pipeline` |
| **SEC**  | Security fixes. Example: `SEC: Updated dependency to fix vulnerability` |
| **RELEASE** | Version bumps and release preparation. Example: `RELEASE: Prepare for 1.1.0 release` |

---

## 📌 **Testing**
- Ensure all tests pass before submitting a PR.
- Run unit tests using **pytest**:
   ```bash
   pytest tests/
   ```
- If adding new functionality, include relevant tests.

---

## 📌 **License**
By contributing to SigVarGen, you agree that your contributions will be licensed under the project's [MIT License](../LICENSE).

---

### 🎉 **Thank you for contributing to SigVarGen! Your help makes this project better.** 🚀