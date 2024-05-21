import tkinter as tk

def append_text(text):
    current_text = display_var.get()
    display_var.set(current_text + text)

def clear_text():
    display_var.set("")

root = tk.Tk()
root.title("Quantum Glasses")

display_var = tk.StringVar()

# Display
display = tk.Entry(root, textvariable=display_var, font=('Helvetica', 24), bg='lightblue', justify='center')
display.grid(row=0, column=0, columnspan=4, sticky='nsew')

# Button configurations
buttons = [
    ('X', 1, 0), ('Y', 1, 1), ('Z', 1, 2),
    ('RX', 2, 0), ('RY', 2, 1), ('RZ', 2, 2),
    ('S', 3, 0), ('SD', 3, 1), ('H', 3, 2),
    ('T', 4, 0), ('TD', 4, 1),
    ('Quit', 5, 0), ('Visualize', 5, 1),
    ('Clear', 6, 0), ('About', 6, 1)
]

for (text, row, col) in buttons:
    if text == 'Quit':
        button = tk.Button(root, text=text, command=root.quit, bg='red')
    elif text == 'Clear':
        button = tk.Button(root, text=text, command=clear_text, bg='red')
    else:
        button = tk.Button(root, text=text, command=lambda t=text: append_text(t), bg='brown')
    button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

# Configure row and column weights for resizing
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

root.mainloop()
