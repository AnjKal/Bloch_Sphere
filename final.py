import os
from platform import system
import tkinter as tk
from tkinter import *
import numpy as np
from qiskit import QuantumCircuit
from qiskit.visualization import visualize_transition, plot_bloch_vector
from qiskit.quantum_info import Statevector
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

# Ignore unnecessary warnings
import warnings
warnings.simplefilter("ignore")
warnings.simplefilter("always")

def initialize_circuit():
    global circuit
    circuit = QuantumCircuit(1)

initialize_circuit()

theta = 0

class Quantum_Visualisation:
    

    def __init__(self):
        pass

    @staticmethod
    def about():
        """Displays information about the project."""
        about_window = tk.Tk()
        about_window.title('About Quantum Glasses')
        about_window.geometry('650x470')

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
        """

        info_label = tk.Label(about_window, text=info_text, font=("Arial", 12), justify='left')
        info_label.pack(expand=True, fill='both')

        about_window.mainloop()

    @staticmethod
    def change_theta(num, window, circuit, key):
        """Changes the global variable theta and destroys the window."""
        global theta
        theta = num * np.pi
        if key == 'x':
            circuit.rx(theta, 0)
        elif key == 'y':
            circuit.ry(theta, 0)
        else:
            circuit.rz(theta, 0)
        theta = 0
        window.destroy()

    def user_input(self, circuit, key):
        """Prompt user to input rotation angle for parameterized rotation gates Rx, Ry, Rz."""
        input_window = tk.Tk()
        input_window.title('Input Theta')
        input_window.geometry('360x160')

        btns = [
            ('PI/4', 0.25), ('PI/2', 0.50), ('PI', 1.0), ('2*PI', 2.0),
            ('-PI/4', -0.25), ('-PI/2', -0.50), ('-PI', -1.0), ('-2*PI', -2.0)
        ]

        for idx, (text, val) in enumerate(btns):
            btn = tk.Button(input_window, height=2, width=10, bg='#834558', font=("Arial", 10), text=text,
                            command=lambda v=val: self.change_theta(v, input_window, circuit, key))
            btn.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

        note_text = tk.Text(input_window, height=2, width=35, bg="light cyan")
        note_text.insert(tk.END, "Provide the value for theta\nRange: [-2*PI, 2*PI]")
        note_text.grid(row=2, columnspan=4, pady=10)

        input_window.mainloop()

    @staticmethod
    def Visualise(circuit):
        """Visualizes the quantum circuit's single qubit rotations."""
        try:
            fig, ax = plt.subplots()
            visualize_transition(circuit=circuit)
            
            # Adding the legend
            legend_elements = [
                Line2D([0], [0], marker='o', color='w', label='Initial State', markerfacecolor='b', markersize=10),
                Line2D([0], [0], marker='o', color='w', label='Rotating Qubit', markerfacecolor='r', markersize=10),
                # Add more as needed for different actions/colors
            ]
            ax.legend(handles=legend_elements, loc='upper right')

            plt.show()
        except Exception as e:
            print(e)

    def main(self):
        """Main application function."""
        try:
            root = tk.Tk()
            root.title('Quantum Glasses')

            # Set the icon
            current_directory = os.path.dirname(os.path.abspath(__file__))
            if system() == 'Windows':
                logo_path = os.path.join(current_directory, "../logo.ico")
                root.iconbitmap(default=logo_path)

            root.geometry('399x410')
            root.resizable(0, 0)  # Blocking the resizing feature

            # Define Layout
            display_frame = tk.LabelFrame(root, bg='#2c94c8')
            button_frame = tk.LabelFrame(root, bg='black')
            display_frame.pack()
            button_frame.pack(fill='both', expand=True)

            display = tk.Entry(display_frame, width=120, font=("Arial", 32), bg='#2c94c8', borderwidth=2, justify=LEFT)
            display.pack(padx=3, pady=4)

            def display_gate(gate_input):
                """Adds a corresponding gate notation in the display to track the operations."""
                display.insert(tk.END, gate_input)
                num_gates_pressed = len(display.get())
                if num_gates_pressed == 10:
                    for btn in gate_buttons:
                        btn.config(state=DISABLED)

            gate_buttons = [
                ('X', lambda: [display_gate('X'), circuit.x(0)]),
                ('Y', lambda: [display_gate('Y'), circuit.y(0)]),
                ('Z', lambda: [display_gate('Z'), circuit.z(0)]),
                ('RX', lambda: [display_gate('RX'), self.user_input(circuit, 'x')]),
                ('RY', lambda: [display_gate('RY'), self.user_input(circuit, 'y')]),
                ('RZ', lambda: [display_gate('RZ'), self.user_input(circuit, 'z')]),
                ('S', lambda: [display_gate('S'), circuit.s(0)]),
                ('SD', lambda: [display_gate('SD'), circuit.sdg(0)]),
                ('H', lambda: [display_gate('H'), circuit.h(0)]),
                ('T', lambda: [display_gate('T'), circuit.t(0)]),
                ('TD', lambda: [display_gate('TD'), circuit.tdg(0)])
            ]

            for i, (text, cmd) in enumerate(gate_buttons):
                btn = tk.Button(button_frame, font=("Arial", 18), bg='#834558', text=text, command=cmd)
                btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky='WE')

            def clear_display():
                """Clears the display and reinitializes the Quantum Circuit."""
                display.delete(0, END)
                initialize_circuit()
                for btn in gate_buttons:
                    btn.config(state=NORMAL)

            special_buttons = [
                ('Quit', root.destroy),
                ('Visualize', lambda: self.Visualise(circuit)),
                ('Clear', lambda: clear_display()),
                ('About', self.about)
            ]

            for i, (text, cmd) in enumerate(special_buttons):
                btn = tk.Button(button_frame, font=("Arial", 18), bg='#bc3454', text=text, command=cmd)
                btn.grid(row=4 + i // 2, column=i % 2 * 2, columnspan=2, sticky='WE', padx=10, pady=10)

            root.mainloop()

            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    app = Quantum_Visualisation()
    app.main()


