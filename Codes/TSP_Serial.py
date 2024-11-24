import time
import math
from collections import defaultdict

# Function to perform BFS and calculate Hamiltonian cycle for a specific start node
def bfs(node, arr, visited, n):
    start_node = node
    visited_count = 1
    visited[node] = True
    cost = 0
    path = [node]

    while visited_count < n:
        min_cost = math.inf
        next_node = -1

        for i in range(n):
            if not visited[i] and arr[start_node][i] < min_cost:
                min_cost = arr[start_node][i]
                next_node = i

        if next_node == -1:
            break  # No valid next node (shouldn't happen for a complete graph)

        visited[next_node] = True
        visited_count += 1
        cost += min_cost
        path.append(next_node)
        start_node = next_node

    # Return to the starting node to complete the cycle
    cost += arr[start_node][node]
    path.append(node)

    return path, cost

# Function to update or append metrics
def update_metrics(num_vertices, bfs_time, language):
    metrics_map = defaultdict(dict)

    # Read existing metrics from the file
    try:
        with open("Metrics.txt", "r") as metrics_file:
            for line in metrics_file:
                size, time_taken, lang = line.split()
                size = int(size)
                time_taken = float(time_taken)
                lang = lang.strip()
                metrics_map[size][lang] = time_taken
    except FileNotFoundError:
        pass  # No existing metrics file

    # Update the metrics
    if language not in metrics_map[num_vertices] or metrics_map[num_vertices][language] > bfs_time:
        metrics_map[num_vertices][language] = bfs_time

    # Write back updated metrics to the file
    with open("Metrics.txt", "w") as metrics_out:
        for size, languages in sorted(metrics_map.items()):
            for lang, time_taken in languages.items():
                metrics_out.write(f"{size}\t{time_taken:.6f}\t{lang}\n")

def main(filename):
    # Read adjacency matrix from file
    try:
        with open(filename, "r") as infile:
            n = int(infile.readline().strip())
            arr = [list(map(int, infile.readline().split())) for _ in range(n)]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except ValueError:
        print(f"Error: Invalid file format in '{filename}'.")
        return

    visited = [False] * n
    paths = []
    costs = []

    # Measure BFS execution time
    bfs_start = time.time()
    for i in range(n):
        visited = [False] * n
        path, cost = bfs(i, arr, visited, n)
        paths.append(path)
        costs.append(cost)
    bfs_end = time.time()

    bfs_time = bfs_end - bfs_start

    # Write results to an output file
    try:
        with open("Results.txt", "w") as outfile:
            for i in range(n):
                outfile.write(f"Vertex {i}:\n")
                outfile.write(f"Path: {'->'.join(map(str, paths[i]))}\n")
                outfile.write(f"Cost: {costs[i]}\n\n")
    except IOError:
        print("Error: Unable to write results to 'Results.txt'.")
        return

    # Update metrics
    update_metrics(n, bfs_time, 'P')  # Use 'p' instead of 'Python'

    print("Execution complete. Results written to 'Results.txt' and metrics to 'Metrics.txt'.")
    print(f"BFS Time: {bfs_time:.6f} seconds.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Error: No input file provided.")
    else:
        main(sys.argv[1])
