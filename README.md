# Quantum Visualizer with Qiskit functions

A graphical application that allows users to apply quantum gates to a single qubit and visualize the resulting quantum state on a **Bloch sphere** using Qiskit and Tkinter.

## Features
- **Graphical User Interface (GUI)** built with Tkinter.
- **Quantum Circuit Manipulation**:
  - Apply various **quantum gates** like X, Y, Z, H, S, T, Rx, Ry, Rz.
  - Rotation gates (Rx, Ry, Rz) support user input for angles.
- **Visualization**:
  - Displays the qubit's transformation on a Bloch sphere using Matplotlib.
  - Uses `qiskit.visualization.visualize_transition()` to animate state evolution.
- **Additional UI Components**:
  - **Gate Buttons:** Apply quantum operations.
  - **Display Area:** Shows applied gate sequence.
  - **Clear Button:** Resets the circuit.
  - **Visualize Button:** Displays the Bloch sphere.
  - **About Button:** Shows gate descriptions.
  - **Quit Button:** Exits the application.
 
### Demo
![Alt text](image-url)
![Alt text](image-url)
![Alt text](image-url)

## Installation
### Prerequisites
Make sure you have Python installed (recommended: Python 3.8+).

Install required dependencies using:
```bash
pip install qiskit qiskit-aer numpy matplotlib
```

## Usage
Run the following command to start the application:
```bash
python quantum_visualizer.py
```

### How to Use
1. Launch the application.
2. Click on quantum gate buttons to apply them to the qubit.
3. Click **Visualize** to see the quantum state transformation on the **Bloch sphere**.
4. Click **Clear** to reset the circuit.
5. Click **Quit** to exit the application.

## Quantum Gates Supported
| Gate | Description |
|------|------------|
| **X** | Flips the qubit state (NOT gate) |
| **Y** | Rotates the state vector about Y-axis |
| **Z** | Flips the phase by PI radians |
| **H** | Creates superposition |
| **S** | Rotation about Z-axis by PI/2 |
| **T** | Rotation about Z-axis by PI/4 |
| **Rx** | Rotation about X-axis (user input required) |
| **Ry** | Rotation about Y-axis (user input required) |
| **Rz** | Rotation about Z-axis (user input required) |
| **Sd** | Rotation about Z-axis by -PI/2 |
| **Td** | Rotation about Z-axis by -PI/4 |


# Quantum Visualizer without Qiskit functions

## Overview
This is a Python-based application that helps to visualize single qubit rotations without packages from the Qiskit library, using only Matplotlib

### Demo
![Alt text](image-url)
![Alt text](image-url)

## Features
- **Single-Qubit Quantum Circuit:** Simulates a qubit's state and applies quantum gates without using Qiskit.
- **Gate Operations:** Supports common quantum gates like X, Y, Z, H, S, T, and their inverse counterparts.
- **Rotation Gates:** Allows users to apply rotation gates (Rx, Ry, Rz) with user-defined angles.
- **Bloch Sphere Visualization:** Displays the qubit's state evolution on the Bloch sphere.
- **Interactive GUI:** Provides an easy-to-use interface using Tkinter.
- **Measurement:** Simulates quantum measurement to observe final probabilities.

## Dependencies
This project requires the following Python libraries:
- `numpy`
- `matplotlib`
- `tkinter`

Ensure these dependencies are installed using:
```bash
pip install numpy matplotlib
```

## How to Run
1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Run the following command:
```bash
python quantum_visualizer.py
```

## Usage
- Click gate buttons (H, X, Y, Z, etc.) to apply operations to the qubit.
- For rotation gates (Rx, Ry, Rz), select the desired angle from the prompt.
- Click "Visualize" to see the updated Bloch sphere representation.
- Use the "Measure" button to simulate quantum measurement.
- Access "About" for a summary of gate functions.

## Gate Functions
All the gates in the version with Qiskit functions are supported

## Known Limitations
- Only supports a single qubit.
- Maximum of ten operations per visualization.
- If visualization fails, the application will close automatically.

## License
This project is licensed under the MIT License.

## Authors
**Team ÅvinyÅ**

---
Enjoy exploring quantum circuits! 🚀

