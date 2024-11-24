import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_graph():
    # Read the sorted Metrics.txt into a pandas DataFrame
    df = pd.read_csv("Metrics.txt", sep="\t", header=None, names=["Vertices", "BFS Time", "Language"])

    # Mapping the language codes to full names for the legend
    language_map = {
        'C': 'Serial C++',
        'P': 'Python',
        'O': 'OpenMP'
    }

    # Create a plot
    plt.figure(figsize=(10, 6))

    # Get the unique input sizes (vertices)
    input_sizes = sorted(df["Vertices"].unique())

    # Set the bar width and position of the bars
    bar_width = 0.25
    index = np.arange(len(input_sizes))

    # Plot the bars for each language (C, P, O)
    for i, language in enumerate(['C', 'P', 'O']):
        language_data = df[df["Language"] == language]
        bfs_times = [language_data[language_data["Vertices"] == size]["BFS Time"].values[0] for size in input_sizes]
        
        # Create bars for each language
        plt.bar(index + i * bar_width, bfs_times, bar_width, label=language_map[language])

    # Customize the graph
    plt.xlabel("Number of Vertices")
    plt.ylabel("BFS Time (seconds)")
    plt.title("BFS Time vs. Number of Vertices (Bar Chart)")
    plt.xticks(index + bar_width, input_sizes)  # Set the x-ticks to the input sizes
    plt.legend(title="Programming Language")
    plt.grid(True, axis='y')

    # Show the graph
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_graph()
    print("Bar graph has been generated.")
