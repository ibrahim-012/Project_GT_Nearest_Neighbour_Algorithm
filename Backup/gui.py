import tkinter as tk
from tkinter import ttk
import os
import subprocess

def run_program():
    selected_file = file_selector.get()
    selected_language = language_selector.get()

    if not selected_file:
        execution_label.config(text="Select a file before running.")
        return
    if not selected_language:
        execution_label.config(text="Select a language before running.")
        return

    # Construct the command based on the selected language
    if selected_language == "C++ Serial":
        command = f"./TSP_S {selected_file}"
    elif selected_language == "OpenMP":
        command = f"./TSP_P {selected_file} 4"  # Assuming 4 threads for parallel execution
    elif selected_language == "Python":
        command = f"python3 TSP_Serial.py {selected_file}"
    else:
        execution_label.config(text="Invalid language selection.")
        return

    # Run the selected program using subprocess
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check for errors
        if process.returncode != 0:
            execution_label.config(text=f"Error running the program:\n{stderr.decode()}")
            return

        # Extract BFS time from the program's output
        output = stdout.decode()
        bfs_time_line = [line for line in output.splitlines() if "BFS Time:" in line]
        bfs_time = bfs_time_line[0].split(":")[1].strip() if bfs_time_line else "N/A"

        # Update execution details
        execution_label.config(
            text=f"Program executed in {selected_language}.\nBFS Time: {bfs_time} seconds.\nView results for a specific vertex."
        )

        # Display the adjacency matrix
        with open(selected_file, "r") as file:
            lines = file.readlines()
            num_vertices = int(lines[0].strip())
            matrix = [line.strip() for line in lines[1:]]

        # Limit matrix size to 20 lines for display
        matrix_display = "\n".join(matrix[:20]) if num_vertices <= 20 else "\n".join(matrix[:20]) + "\n..." 

        # Update matrix label
        matrix_label.config(state=tk.NORMAL)
        matrix_label.delete(1.0, tk.END)  # Clear the text field
        matrix_label.insert(tk.END, f"Adjacency Matrix (up to 20 lines shown):\n\n{matrix_display}")
        matrix_label.config(state=tk.DISABLED)

    except Exception as e:
        execution_label.config(text=f"Error: {str(e)}")

def display_result():
    vertex = vertex_entry.get()
    if not vertex.isdigit():
        result_label.config(text="Invalid vertex input. Enter a number.")
        return

    vertex = int(vertex)
    try:
        with open("Results.txt", "r") as file:
            results = file.readlines()

        if vertex < 0 or vertex >= len(results) // 4:
            result_label.config(text="Vertex out of range.")
            return

        result_label.config(text=f"Path and Cost for Vertex {vertex}:\n{results[4 * vertex + 1].strip()}\n{results[4 * vertex + 2].strip()}")
    except FileNotFoundError:
        result_label.config(text="Results file not found. Run the program first.")

# Create GUI
root = tk.Tk()
root.title("Hamiltonian Cycle Finder")

# File selection with sorted order
file_selector = ttk.Combobox(root, values=sorted([f for f in os.listdir() if f.startswith("data_") and f.endswith(".txt")]))
file_selector.grid(row=0, column=1)

ttk.Label(root, text="Select Dataset:").grid(row=0, column=0)

# Language selection
language_selector = ttk.Combobox(root, values=["C++ Serial", "OpenMP", "Python"])
language_selector.grid(row=1, column=1)
ttk.Label(root, text="Select Language:").grid(row=1, column=0)

# Run button
ttk.Button(root, text="Run", command=run_program).grid(row=0, column=2)

# Execution details display
execution_label = ttk.Label(root, text="", justify="left", wraplength=600)
execution_label.grid(row=2, column=0, columnspan=3)

# Matrix display using Text widget with wider width and scrollable
matrix_label = tk.Text(root, height=25, width=200, wrap=tk.WORD, state=tk.DISABLED)
matrix_label.grid(row=3, column=0, columnspan=3)

# Vertex input
ttk.Label(root, text="Enter Vertex:").grid(row=4, column=0)
vertex_entry = ttk.Entry(root)
vertex_entry.grid(row=4, column=1)

# Display result button
ttk.Button(root, text="Display Result", command=display_result).grid(row=4, column=2)

# Result display
result_label = ttk.Label(root, text="", wraplength=400, justify="left")
result_label.grid(row=5, column=0, columnspan=3)

root.mainloop()
