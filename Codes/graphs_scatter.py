# graphs.py

import matplotlib.pyplot as plt

def generate_scatter_plot():
    # Read the sorted metrics data from Metrics.txt
    data = {'C': [], 'O': [], 'P': []}
    with open("Metrics.txt", "r") as file:
        for line in file:
            parts = line.split()
            size = int(parts[0])  # Number of vertices
            time = float(parts[1])  # BFS time
            language = parts[2]  # Programming language
            if language in data:
                data[language].append((size, time))

    # Create a scatter plot for each language
    plt.figure(figsize=(10, 6))

    # Scatter plot for Serial C++ (C)
    C_data = data['C']
    sizes_C, times_C = zip(*C_data) if C_data else ([], [])
    plt.scatter(sizes_C, times_C, color='r', label='Serial C++', marker='o')

    # Scatter plot for OpenMP (O)
    O_data = data['O']
    sizes_O, times_O = zip(*O_data) if O_data else ([], [])
    plt.scatter(sizes_O, times_O, color='g', label='OpenMP', marker='s')

    # Scatter plot for Python (P)
    P_data = data['P']
    sizes_P, times_P = zip(*P_data) if P_data else ([], [])
    plt.scatter(sizes_P, times_P, color='b', label='Python', marker='^')

    # Set plot labels and title
    plt.xlabel('Number of Vertices')
    plt.ylabel('BFS Time (seconds)')
    plt.title('BFS Time vs. Number of Vertices for Different Languages')

    # Add a legend
    plt.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_scatter_plot()
