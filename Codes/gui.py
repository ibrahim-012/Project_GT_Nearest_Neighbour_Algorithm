import tkinter as tk
from tkinter import ttk
import os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt

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
        command = f"g++ TSP_Serial.cpp -o tsp_c.exe && tsp_c.exe {selected_file}"
    elif selected_language == "OpenMP":
        command = f"g++ -fopenmp TSP_Parallel.cpp -o tsp_o.exe && tsp_o.exe {selected_file} 4"  # Assuming 4 threads for parallel execution
    elif selected_language == "Python":
        command = f"python TSP_Serial.py {selected_file}"
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
            text=f"Program executed in {selected_language}.\nBFS Time: {bfs_time}\nView results for a specific vertex."
        )

        # Visualize the complete graph
        with open(selected_file, "r") as file:
            lines = file.readlines()
            num_vertices = int(lines[0].strip())
            matrix = [line.strip() for line in lines[1:]]

        # Display the adjacency matrix in the text box
        matrix_text.delete(1.0, tk.END)  # Clear any previous content
        for row in matrix:
            matrix_text.insert(tk.END, row + "\n")

        # Visualize the graph
        visualize_graph(matrix, num_vertices)

    except Exception as e:
        execution_label.config(text=f"Error: {str(e)}")

def visualize_graph(matrix, num_vertices):
    G = nx.Graph()
    
    # Add nodes
    for i in range(num_vertices):
        G.add_node(i)
    
    # Add edges with weights
    for i, row in enumerate(matrix):
        weights = row.split("\t")  # Handle tab separation
        for j, weight in enumerate(weights):
            if i != j:  # Avoid self-loops (diagonal entries are always 0)
                G.add_edge(i, j, weight=int(weight))
    
    # Draw the graph using circular layout
    pos = nx.circular_layout(G)  # Circular layout for node positioning
    edge_labels = nx.get_edge_attributes(G, "weight")

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight="bold", edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Title the graph as "Complete graph: K<number of vertices>"
    plt.suptitle(f"Complete graph: K{num_vertices}", fontsize=16)
    plt.show()

def display_result():
    vertex = vertex_entry.get()
    if not vertex.isdigit():
        result_label.config(text="Invalid vertex input. Enter a number.")
        return

    vertex = int(vertex)

    results_file_path = "Results.txt"

    try:
        # Open and read the Results.txt file
        with open(results_file_path, "r") as file:
            results = file.readlines()

        # Check if the vertex is within the valid range
        if vertex < 0 or vertex >= len(results) // 4:
            result_label.config(text="Vertex out of range.")
            return

        # Extract the path and cost for the selected vertex
        path_line = results[4 * vertex + 1].strip()
        path = path_line.split("Path: ")[1].split("->")

        cost_line = results[4 * vertex + 2].strip()
        cost = cost_line.split("Cost: ")[1]

        # Display the path and cost for the vertex
        result_label.config(text=f"Path and Cost for Vertex {vertex}:\n{path_line}\n{cost_line}")

        # Visualize the cycle graph based on the path
        visualize_cycle_graph(path, vertex)

    except FileNotFoundError:
        result_label.config(text="Results file not found. Run the program first.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def visualize_cycle_graph(path, vertex):
    # Fetch the number of vertices from the dataset
    selected_file = file_selector.get()
    with open(selected_file, "r") as file:
        lines = file.readlines()
        num_vertices = int(lines[0].strip())
        matrix = [line.strip().split("\t") for line in lines[1:]]
    
    # Create a graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(range(num_vertices))

    # Add edges from the cycle path with weights
    for i in range(len(path) - 1):
        u, v = int(path[i]), int(path[i + 1])
        weight = int(matrix[u][v])  # Get the weight from the matrix
        G.add_edge(u, v, weight=weight)

    # Draw the graph using circular layout
    pos = nx.circular_layout(G)  # Circular layout for node positioning
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, font_size=10, font_weight="bold", edge_color="gray")

    # Draw edge labels with weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Title the graph as "Hamiltonian cycle for vertex <vertex>"
    plt.suptitle(f"Hamiltonian cycle for vertex {vertex}")
    plt.show()

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

# Run Algorithm button
ttk.Button(root, text="Run Algorithm", command=run_program).grid(row=2, column=0, columnspan=3)

# Execution details display
execution_label = ttk.Label(root, text="", justify="left", wraplength=600)
execution_label.grid(row=3, column=0, columnspan=3)

# Vertex input
ttk.Label(root, text="Enter Vertex:").grid(row=4, column=0)
vertex_entry = ttk.Entry(root)
vertex_entry.grid(row=4, column=1)

# Display result button
ttk.Button(root, text="Display Result", command=display_result).grid(row=4, column=2)

# Result display
result_label = ttk.Label(root, text="", wraplength=400, justify="left")
result_label.grid(row=5, column=0, columnspan=3)

# Matrix display textbox (large)
matrix_text = tk.Text(root, width=60, height=15)
matrix_text.grid(row=6, column=0, columnspan=3)

root.mainloop()
