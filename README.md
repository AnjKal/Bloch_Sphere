# Quantum Visualizer with QIskit functions

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

## Potential Enhancements
- Add support for **multi-qubit circuits**.
- Implement an **undo last operation** feature.
- Display **probability distributions** for measurement outcomes.

## License
This project is licensed under the MIT License.

## Authors
**Team ÅvinyÅ**

---
Enjoy exploring quantum circuits! 🚀

