#without qiskit
import os
import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button as mplButton

# UI appearance settings
BG_COLOR = '#2c94c5'
BTN_COLOR = '#834550'
SPECIAL_BTN_COLOR = '#bc3457'
BTN_FONT = ('Arial', 18)
DISPLAY_FONT = ('Arial', 32)


class QuantumCircuit:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = np.array([1, 0], dtype=complex)  # Initial state |0>
        self.gates = []

    def x(self):
        self.gates.append(self._x_gate)

    def y(self):
        self.gates.append(self._y_gate)

    def z(self):
        self.gates.append(self._z_gate)

    def h(self):
        self.gates.append(self._h_gate)

    def s(self):
        self.gates.append(self._s_gate)

    def sdg(self):
        self.gates.append(self._sdg_gate)

    def t(self):
        self.gates.append(self._t_gate)

    def tdg(self):
        self.gates.append(self._tdg_gate)

    def rx(self, theta):
        self.gates.append(lambda: self._rx_gate(theta))

    def ry(self, theta):
        self.gates.append(lambda: self._ry_gate(theta))

    def rz(self, theta):
        self.gates.append(lambda: self._rz_gate(theta))

    def apply_gates(self):
        for gate in self.gates:
            self.state = gate() @ self.state

    def _x_gate(self):
        return np.array([[0, 1], [1, 0]], dtype=complex)

    def _y_gate(self):
        return np.array([[0, -1j], [1j, 0]], dtype=complex)

    def _z_gate(self):
        return np.array([[1, 0], [0, -1]], dtype=complex)

    def _h_gate(self):
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    def _s_gate(self):
        return np.array([[1, 0], [0, 1j]], dtype=complex)

    def _sdg_gate(self):
        return np.array([[1, 0], [0, -1j]], dtype=complex)

    def _t_gate(self):
        return np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

    def _tdg_gate(self):
        return np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]], dtype=complex)

    def _rx_gate(self, theta):
        return np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                         [-1j * np.sin(theta / 2), np.cos(theta / 2)]], dtype=complex)

    def _ry_gate(self, theta):
        return np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                         [np.sin(theta / 2), np.cos(theta / 2)]], dtype=complex)

    def _rz_gate(self, theta):
        return np.array([[np.exp(-1j * theta / 2), 0],
                         [0, np.exp(1j * theta / 2)]], dtype=complex)

    def measure(self):
        probabilities = np.abs(self.state) ** 2
        return np.random.choice([0, 1], p=probabilities)


def bloch_sphere(state):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.1)

    rho = np.outer(state, state.conj())
    x_bloch = 2 * np.real(rho[0, 1])
    y_bloch = 2 * np.imag(rho[1, 0])
    z_bloch = 1 - 2 * np.real(rho[1, 1])

    ax.quiver(0, 0, 0, x_bloch, y_bloch, z_bloch, color='r', arrow_length_ratio=0.1)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


class QuantumVisualizer:
    """Primary class for the Quantum Visualizer application."""

    def __init__(self):
        self.visualization_window = None

    @staticmethod
    def show_about():
        """Display project information."""
        about_window = tk.Tk()
        about_window.title('About')
        about_window.geometry('650x470')

        info_label = tk.Label(about_window, text="About Quantum Visualizer:", font=("Arial", 14))
        info_label.pack()

        text_widget = tk.Text(about_window, height=20, width=20)
        text_widget.pack(fill='both', expand=True)

        info_text = """
        About: Visualization tool for Single Qubit Rotation on Bloch Sphere
        BY:Team ÅvinyÅ 

        Gate buttons and their Qiskit commands:

        X: flips the state of qubit - circuit.x()
        Y: rotates the state vector about Y-axis - circuit.y()
        Z: flips the phase by PI radians - circuit.z()
        Rx: rotation about the X axis - circuit.rx()
        Ry: rotation about the Y axis - circuit.ry()
        Rz: rotation about the Z axis - circuit.rz()
        S: rotation about Z axis by PI/2 radians - circuit.s()
        T: rotation about Z axis by PI/4 radians - circuit.t()
        Sd: rotation about Z axis by -PI/2 radians - circuit.sdg()
        Td: rotation about Z axis by -PI/4 radians - circuit.tdg()
        H: creates superposition - circuit.h()

        Allowed range for theta (rotation_angle) in the app is [-2*PI, 2*PI]

        If visualization fails, the app closes automatically.
        Only ten operations can be visualized at a time.
        """
        text_widget.insert(END, info_text)

        about_window.mainloop()

    @staticmethod
    def set_theta(num, window, circuit, key):
        """Set theta value and close the input window."""
        theta = num * np.pi
        if key == 'x':
            circuit.rx(theta)
        elif key == 'y':
            circuit.ry(theta)
        else:
            circuit.rz(theta)
        window.destroy()

    def get_theta(self, circuit, key):
        """Prompt user to input rotation angle for Rx, Ry, Rz gates."""
        input_window = tk.Tk()
        input_window.title('Input Theta')
        input_window.geometry('360x160')
        input_window.resizable(0, 0)

        btns = [
            ('PI/4', 0.25), ('PI/2', 0.50), ('PI', 1.0), ('2*PI', 2.0),
            ('-PI/4', -0.25), ('-PI/2', -0.50), ('-PI', -1.0), ('-2*PI', -2.0)
        ]

        for idx, (text, val) in enumerate(btns):
            btn = tk.Button(input_window, height=2, width=10, bg=BTN_COLOR, font=("Arial", 10), text=text,
                            command=lambda v=val: self.set_theta(v, input_window, circuit, key))
            btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

        note_text = tk.Text(input_window, height=2, width=35, bg="light cyan")
        note_text.insert(END, "Provide the value for theta\nRange: [-2*PI, 2*PI]")
        note_text.grid(row=2, columnspan=4, pady=10)

        input_window.mainloop()

    def visualize(self, circuit):
        """Visualize the quantum circuit's single qubit rotations."""
        if self.visualization_window and self.visualization_window.winfo_exists():
            self.visualization_window.destroy()

        self.visualization_window = tk.Toplevel()
        self.visualization_window.title("Visualization")

        vis_frame = tk.Frame(self.visualization_window)
        vis_frame.pack(fill='both', expand=True)

        try:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x, y, z, color='b', alpha=0.1)

            circuit.apply_gates()
            state = circuit.state
            rho = np.outer(state, state.conj())
            x_bloch = 2 * np.real(rho[0, 1])
            y_bloch = 2 * np.imag(rho[1, 0])
            z_bloch = 1 - 2 * np.real(rho[1, 1])

            ax.quiver(0, 0, 0, x_bloch, y_bloch, z_bloch, color='r', arrow_length_ratio=0.1)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            canvas = FigureCanvasTkAgg(fig, master=vis_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        except Exception as e:
            print(f"Visualization failed: {e}")
            self.visualization_window.destroy()

    def main(self, testing=False):
        """Run the main Quantum Visualizer application."""
        root = tk.Tk()
        root.geometry('650x700')
        root.resizable(0, 0)
        root.configure(bg=BG_COLOR)
        root.title("ÅvinyÅ")

        current_dir = os.path.dirname(__file__)
        #root.iconbitmap(default=os.path.join(current_dir, "../logo.ico"))

        self.circuit = QuantumCircuit(1)

        top_frame = tk.Frame(root, bg=BG_COLOR)
        top_frame.pack(expand=True, fill='both')

        buttons = [
            ('H', self.circuit.h),
            ('X', self.circuit.x),
            ('Y', self.circuit.y),
            ('Z', self.circuit.z),
            ('S', self.circuit.s),
            ('T', self.circuit.t),
            ('Sd', self.circuit.sdg),
            ('Td', self.circuit.tdg),
            ('Rx', lambda: self.get_theta(self.circuit, 'x')),
            ('Ry', lambda: self.get_theta(self.circuit, 'y')),
            ('Rz', lambda: self.get_theta(self.circuit, 'z')),
            ('Visualize', lambda: self.visualize(self.circuit)),
            ('About', self.show_about)
        ]

        for idx, (text, command) in enumerate(buttons):
            btn = tk.Button(top_frame, text=text, bg=BTN_COLOR, font=BTN_FONT, command=command)
            btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

        root.mainloop()


if __name__ == "__main__":
    app = QuantumVisualizer()
    app.main()
