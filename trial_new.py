#two-qubit gate at line 219
#to be tested
import os
from platform import system
import tkinter as tk
from tkinter import *
import warnings
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import visualize_transition, plot_bloch_multivector, plot_state_city, plot_histogram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Suppress warnings
warnings.simplefilter("ignore")

# Setup the quantum circuit
def setup_circuit(qubits=1):
    global circuit, simulator
    circuit = QuantumCircuit(qubits)
    simulator = AerSimulator()

setup_circuit(2)  # Change the number of qubits as needed

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
        About: Visualization tool for Quantum Gates on Multiple Qubits
        BY: Team ÅvinyÅ

        Gate buttons and their Qiskit commands:

        X: flips the state of qubit - circuit.x()
        Y: rotates the state vector about Y-axis - circuit.y()
        Z: flips the phase by PI radians - circuit.z()
        RX: rotation about the X axis - circuit.rx()
        RY: rotation about the Y axis - circuit.ry()
        RZ: rotation about the Z axis - circuit.rz()
        S: rotation about Z axis by PI/2 radians - circuit.s()
        T: rotation about Z axis by PI/4 radians - circuit.t()
        Sd: rotation about Z axis by -PI/2 radians - circuit.sdg()
        Td: rotation about Z axis by -PI/4 radians - circuit.tdg()
        H: creates superposition - circuit.h()
        CX: controlled-X (CNOT) gate - circuit.cx()

        Allowed range for theta (rotation_angle) in the app is [-2*PI, 2*PI]

        If visualization fails, the app closes automatically.
        Only ten operations can be visualized at a time.
        """
        text_widget.insert(END, info_text)

        about_window.mainloop()

    @staticmethod
    def set_theta(num, window, circuit, key, target):
        """Set theta value and close the input window."""
        global theta
        theta = num * np.pi
        if key == 'x':
            circuit.rx(theta, target)
        elif key == 'y':
            circuit.ry(theta, target)
        else:
            circuit.rz(theta, target)
        theta = 0
        window.destroy()

    def get_theta(self, circuit, key, target):
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
                            command=lambda v=val: self.set_theta(v, input_window, circuit, key, target))
            btn.grid(row=idx//4, column=idx%4, padx=5, pady=5)

        note_text = tk.Text(input_window, height=2, width=35, bg="light cyan")
        note_text.insert(END, "Provide the value for theta\nRange: [-2*PI, 2*PI]")
        note_text.grid(row=2, columnspan=4, pady=10)

        input_window.mainloop()

    def visualize(self, circuit):
        """Visualize the quantum circuit's state vector."""
        if self.visualization_window and self.visualization_window.winfo_exists():
            self.visualization_window.destroy()

        self.visualization_window = tk.Toplevel()
        self.visualization_window.title("Visualization")

        vis_frame = tk.Frame(self.visualization_window)
        vis_frame.pack(fill='both', expand=True)

        try:
            transpiled = transpile(circuit, simulator)
            fig, ax = plt.subplots(1, 3, figsize=(15, 5))

            state_vector = simulator.run(transpiled).result().get_statevector()
            plot_bloch_multivector(state_vector, ax=ax[0])
            plot_state_city(state_vector, ax=ax[1])
            ax[2].remove()

            canvas = FigureCanvasTkAgg(fig, master=vis_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

            # Create an "End" button on the Matplotlib figure
            end_ax = fig.add_axes([0.85, 0.05, 0.1, 0.075])
            end_button = Button(end_ax, 'End')

            def close_vis(event):
                self.visualization_window.destroy()

            end_button.on_clicked(close_vis)

        except Exception as e:
            print(e)
            self.visualization_window.destroy()

    def measure_and_visualize(self, circuit):
        """Measure the quantum circuit and visualize the result probabilities."""
        circuit.measure_all()
        transpiled = transpile(circuit, simulator)
        result = simulator.run(transpiled).result()
        counts = result.get_counts()

        fig = plot_histogram(counts)
        plt.show()

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
                if len(display.get()) == 10:
                    for btn in buttons:
                        btn.config(state=DISABLED)

            def clear_display(circuit):
                display.delete(0, END)
                setup_circuit(2)  # Change the number of qubits as needed
                for btn in buttons:
                    btn.config(state=NORMAL)

            buttons = []

            def create_gate_button(text, gate, cmd, row, col):
                btn = tk.Button(button_frame, font=BTN_FONT, bg=BTN_COLOR, text=text, command=lambda: [update_display(gate), cmd()])
                btn.grid(row=row, column=col, padx=5, pady=5, sticky='WE')
                buttons.append(btn)

            # Single-qubit gates
            create_gate_button('X', 'x', lambda: circuit.x(0), 0, 0)
            create_gate_button('Y', 'y', lambda: circuit.y(0), 0, 1)
            create_gate_button('Z', 'z', lambda: circuit.z(0), 0, 2)
            create_gate_button('RX', 'Rx', lambda: self.get_theta(circuit, 'x', 0), 1, 0)
            create_gate_button('RY', 'Ry', lambda: self.get_theta(circuit, 'y', 0), 1, 1)
            create_gate_button('RZ', 'Rz', lambda: self.get_theta(circuit, 'z', 0), 1, 2)
            create_gate_button('S', 's', lambda: circuit.s(0), 2, 0)
            create_gate_button('SD', 'sd', lambda: circuit.sdg(0), 2, 1)
            create_gate_button('H', 'H', lambda: circuit.h(0), 2, 2)
            create_gate_button('T', 't', lambda: circuit.t(0), 3, 0)
            create_gate_button('TD', 'td', lambda: circuit.tdg(0), 3, 1)

# Two-qubit gates
            create_gate_button('CX', 'cx', lambda: circuit.cx(0, 1), 3, 2)

            special_buttons = [
                ('Quit', root.destroy),
                ('Visualize Bloch', lambda: self.visualize(circuit)),
                ('Measure & Visualize', lambda: self.measure_and_visualize(circuit)),
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
