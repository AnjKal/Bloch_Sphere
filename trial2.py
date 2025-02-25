import os
from platform import system
import tkinter as tk
from tkinter import *
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button

# Suppress warnings
warnings.simplefilter("ignore")

# Define a simple quantum circuit class to handle single qubit operations
class SimpleQuantumCircuit:
    def __init__(self):
        # Initial state vector for |0>
        self.state = np.array([[1], [0]], dtype=complex)
    
    def apply_gate(self, gate_matrix):
        self.state = np.dot(gate_matrix, self.state)
    
    def x(self):
        # Pauli-X gate
        x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
        self.apply_gate(x_gate)
    
    def y(self):
        # Pauli-Y gate
        y_gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.apply_gate(y_gate)
    
    def z(self):
        # Pauli-Z gate
        z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
        self.apply_gate(z_gate)
    
    def rx(self, theta):
        # Rotation around X-axis
        rx_gate = np.array([[np.cos(theta/2), -1j*np.sin(theta/2)], [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
        self.apply_gate(rx_gate)
    
    def ry(self, theta):
        # Rotation around Y-axis
        ry_gate = np.array([[np.cos(theta/2), -np.sin(theta/2)], [np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
        self.apply_gate(ry_gate)
    
    def rz(self, theta):
        # Rotation around Z-axis
        rz_gate = np.array([[np.exp(-1j*theta/2), 0], [0, np.exp(1j*theta/2)]], dtype=complex)
        self.apply_gate(rz_gate)
    
    def s(self):
        # S gate
        s_gate = np.array([[1, 0], [0, 1j]], dtype=complex)
        self.apply_gate(s_gate)
    
    def sdg(self):
        # S-dagger gate
        sdg_gate = np.array([[1, 0], [0, -1j]], dtype=complex)
        self.apply_gate(sdg_gate)
    
    def t(self):
        # T gate
        t_gate = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)
        self.apply_gate(t_gate)
    
    def tdg(self):
        # T-dagger gate
        tdg_gate = np.array([[1, 0], [0, np.exp(-1j*np.pi/4)]], dtype=complex)
        self.apply_gate(tdg_gate)
    
    def h(self):
        # Hadamard gate
        h_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        self.apply_gate(h_gate)
    
    def get_bloch_vector(self):
        # Compute the Bloch vector from the state vector
        a = self.state[0, 0]
        b = self.state[1, 0]
        x = 2 * np.real(np.conj(a) * b)
        y = 2 * np.imag(np.conj(a) * b)
        z = np.real(np.conj(a) * a - np.conj(b) * b)
        return np.array([x, y, z])

circuit = SimpleQuantumCircuit()
theta = 0

# UI appearance settings
BG_COLOR = '#2c94c5'
BTN_COLOR = '#834550'
SPECIAL_BTN_COLOR = '#bc3457'
BTN_FONT = ('Arial', 18)
DISPLAY_FONT = ('Arial', 32)

class QuantumVisualizer:
    """Primary class for the Quantum Visualizer application."""

    def __init__(self):
        self.visualization_window = None
        self.gate_sequence = []

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

        Gate buttons and their corresponding commands:

        X: flips the state of qubit
        Y: rotates the state vector about Y-axis
        Z: flips the phase by PI radians
        Rx: rotation about the X axis
        Ry: rotation about the Y axis
        Rz: rotation about the Z axis
        S: rotation about Z axis by PI/2 radians
        T: rotation about Z axis by PI/4 radians
        Sd: rotation about Z axis by -PI/2 radians
        Td: rotation about Z axis by -PI/4 radians
        H: creates superposition

        Allowed range for theta (rotation_angle) in the app is [-2*PI, 2*PI]

        If visualization fails, the app closes automatically.
        Only ten operations can be visualized at a time.
        """
        text_widget.insert(END, info_text)

        about_window.mainloop()

    @staticmethod
    def set_theta(num, window, circuit, key):
        """Set theta value and close the input window."""
        global theta
        theta = num * np.pi
        if key == 'x':
            circuit.rx(theta)
        elif key == 'y':
            circuit.ry(theta)
        else:
            circuit.rz(theta)
        theta = 0
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
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)

        note_text = tk.Text(input_window, height=2, width=35, bg="light cyan")
        note_text.insert(END, "Provide the value for theta\nRange: [-2*PI, 2*PI]")
        note_text.grid(row=2, columnspan=4, pady=10)

        input_window.mainloop()

    def visualize(self, gate_sequence):
        """Visualize the quantum circuit's single qubit rotations."""
        if self.visualization_window and self.visualization_window.winfo_exists():
            self.visualization_window.destroy()

        self.visualization_window = tk.Toplevel()
        self.visualization_window.title("Visualization")

        vis_frame = tk.Frame(self.visualization_window)
        vis_frame.pack(fill='both', expand=True)

        try:
            current_circuit = SimpleQuantumCircuit()
            for gate in gate_sequence:
                if gate == 'x':
                    current_circuit.x()
                elif gate == 'y':
                    current_circuit.y()
                elif gate == 'z':
                    current_circuit.z()
                elif gate.startswith('rx'):
                    theta = float(gate[2:])
                    current_circuit.rx(theta)
                elif gate.startswith('ry'):
                    theta = float(gate[2:])
                    current_circuit.ry(theta)
                elif gate.startswith('rz'):
                    theta = float(gate[2:])
                    current_circuit.rz(theta)
                elif gate == 's':
                    current_circuit.s()
                elif gate == 'sd':
                    current_circuit.sdg()
                elif gate == 'h':
                    current_circuit.h()
                elif gate == 't':
                    current_circuit.t()
                elif gate == 'td':
                    current_circuit.tdg()

                bloch_vector = current_circuit.get_bloch_vector()
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.quiver(0, 0, 0, bloch_vector[0], bloch_vector[1], bloch_vector[2])
                ax.set_xlim([-1, 1])
                ax.set_ylim([-1, 1])
                ax.set_zlim([-1, 1])
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                plt.title('Bloch Sphere')

                canvas = FigureCanvasTkAgg(fig, master=vis_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)

                vis_frame.after(1000, lambda: canvas.get_tk_widget().destroy())

            end_ax = fig.add_axes([0.85, 0.05, 0.1, 0.075])
            end_button = Button(end_ax, 'End')

            def close_vis(event):
                self.visualization_window.destroy()

            end_button.on_clicked(close_vis)

        except Exception as e:
            print(e)
            self.visualization_window.destroy()

    def main(self, testing=False):
        """Main application function."""
        try:
            root = tk.Tk()
            root.title('Quantum Visualizer')
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if system() == 'Windows':
                root.iconbitmap(default=os.path.join(current_dir, "../logo.ico"))

            root.geometry('420x420')
            root.resizable(0, 0)

            display_frame = tk.LabelFrame(root)
            button_frame = tk.LabelFrame(root, bg='black')
            display_frame.pack()
            button_frame.pack(fill='both', expand=True)

            display = tk.Entry(display_frame, width=120, font=DISPLAY_FONT, bg=BG_COLOR, borderwidth=2, justify=LEFT)
            display.pack(padx=3, pady=4)

            def update_display(gate):
                display.insert(END, gate)
                self.gate_sequence.append(gate)
                if len(display.get()) == 10:
                    for btn in buttons:
                        btn.config(state=DISABLED)

            buttons = [
                ('X', 'x', lambda: [circuit.x(), update_display('x')]),
                ('Y', 'y', lambda: [circuit.y(), update_display('y')]),
                ('Z', 'z', lambda: [circuit.z(), update_display('z')]),
                ('RX', 'Rx', lambda: self.get_theta(circuit, 'x')),
                ('RY', 'Ry', lambda: self.get_theta(circuit, 'y')),
                ('RZ', 'Rz', lambda: self.get_theta(circuit, 'z')),
                ('S', 's', lambda: [circuit.s(), update_display('s')]),
                ('SD', 'sd', lambda: [circuit.sdg(), update_display('sd')]),
                ('H', 'H', lambda: [circuit.h(), update_display('h')]),
                ('T', 't', lambda: [circuit.t(), update_display('t')]),
                ('TD', 'td', lambda: [circuit.tdg(), update_display('td')])
            ]

            for i, (text, display_text, cmd) in enumerate(buttons):
                btn = tk.Button(button_frame, font=BTN_FONT, bg=BTN_COLOR, text=text,
                                command=lambda d=display_text, c=cmd: [c(), update_display(d)])
                btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='WE')
                buttons[i] = btn

            def clear_display(circuit):
                display.delete(0, END)
                global circuit_instance
                circuit_instance = SimpleQuantumCircuit()
                self.gate_sequence.clear()
                for btn in buttons:
                    btn.config(state=NORMAL)

            special_buttons = [
                ('Quit', root.destroy),
                ('Visualize', lambda: self.visualize(self.gate_sequence)),
                ('Clear', lambda: clear_display(circuit)),
                ('About', self.show_about)
            ]

            for i, (text, cmd) in enumerate(special_buttons):
                btn = tk.Button(button_frame, font=BTN_FONT, bg=SPECIAL_BTN_COLOR, text=text, command=cmd)
                btn.grid(row=4+i//2, column=i%2*2, columnspan=2, sticky='WE', padx=10, pady=10)

            if testing:
                root.update_idletasks()
                root.update()
            else:
                root.mainloop()

            return True
        except Exception as e:
            raise Exception from e

if __name__ == "__main__":
    app = QuantumVisualizer()
    app.main(testing=False)
