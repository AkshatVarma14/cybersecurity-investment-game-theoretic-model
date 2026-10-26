# PROJECT_INSTRUCTIONS.md — Course Project Setup and Operating Instructions

## Project Title
**A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations**

---

## 1. Prerequisites
- Python 3.10 or later (verified on Python 3.12 and 3.14).
- Microsoft Visual Studio Code (optional, but recommended).
- Windows PowerShell 5.1+ or PowerShell 7+.
- Git version control.

---

## 2. Windows PowerShell Setup Guide

### 2.1 Clone / Open Workspace
Open Windows PowerShell and navigate to the project directory:
```powershell
cd C:\Users\aksha\Documents\antigravity\beautiful-pascal
```

### 2.2 Create Virtual Environment
Create an isolated Python virtual environment:
```powershell
python -m venv .venv
```

### 2.3 Activate the Virtual Environment
Activate the environment in PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell displays an `Execution_Policies` restriction, temporarily allow local scripts via: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

### 2.4 (Optional) Install Dependencies
The core simulation runs on Python's built-in standard library. If you wish to install the optional plotting utilities:
```powershell
pip install -r requirements.txt
```
Or install in editable development mode:
```powershell
pip install -e .
```

---

## 3. Running the Project

### 3.1 Via Root Entrypoint
You can execute the program directly from the repository root:
```powershell
python main.py --help
```

### 3.2 Via Package Module
Alternatively, launch as an installed Python module:
```powershell
python -m cyber_investment_sim.cli --help
```

### 3.3 Running Unit Tests
Execute the unit test discovery engine using standard library `unittest`:
```powershell
python -m unittest discover -s tests -v
```

---

## 4. Visual Studio Code Configuration

1. **Open Folder:** Open `beautiful-pascal` in VS Code (`File` -> `Open Folder...`).
2. **Select Interpreter:**
   - Press `Ctrl + Shift + P` -> `Python: Select Interpreter`.
   - Choose the virtual environment: `.\.venv\Scripts\python.exe`.
3. **Optional Workspace Settings:**
   - Copy `.vscode/settings.json.example` to `.vscode/settings.json` if you wish to enable in-editor test discovery.
   - Copy `.vscode/launch.json.example` to `.vscode/launch.json` to enable F5 debugging.

---

## 5. Coding and Academic Standards
- **Mathematical Transparency:** Functions that implement mathematical formulas must state the equation in LaTeX/KaTeX in their docstring.
- **Type Annotations:** All functions and methods must use complete type annotations (`typing.Optional`, `typing.Tuple`, `typing.Dict`, `typing.List`, etc.).
- **Immutability:** Configuration classes must use `@dataclass(frozen=True)` to prevent unintended state mutations across simulation steps.
- **Deterministic Testing:** Tests must verify edge cases (zero investment, maximal investment, symmetric vs asymmetric firms, pure vs mixed equilibria) with zero random variation.
