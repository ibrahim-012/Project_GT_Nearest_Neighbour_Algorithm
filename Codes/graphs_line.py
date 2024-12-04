import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

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

    # Plot each programming language as a separate line
    for language in df["Language"].unique():
        language_data = df[df["Language"] == language]
        # Use the mapped language name for the legend
        plt.plot(language_data["Vertices"], language_data["BFS Time"], label=language_map.get(language, language))

    # Customize the graph
    plt.xlabel("Number of Vertices")
    plt.ylabel("BFS Time (seconds)")
    plt.title("BFS Time vs. Number of Vertices")
    plt.legend(title="Programming Language")
    plt.grid(True)

    # Set x-axis ticks at intervals of 5
    plt.gca().xaxis.set_major_locator(MultipleLocator(5))

    # Show the graph
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_graph()
    print("Graph has been generated.")
