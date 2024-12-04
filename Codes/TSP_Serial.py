import time
import math

# Perform BFS for Hamiltonian cycle
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
            break

        visited[next_node] = True
        visited_count += 1
        cost += min_cost
        path.append(next_node)
        start_node = next_node

    cost += arr[start_node][node]
    path.append(node)

    return path, cost

# Update metrics file
def update_metrics(num_vertices, bfs_time, language):
    with open("Metrics.txt", "a") as metrics_out:
        metrics_out.write(f"{num_vertices}\t{bfs_time:.10f}\t{language}\n")

def main(filename):
    try:
        with open(filename, "r") as infile:
            n = int(infile.readline().strip())
            arr = [list(map(int, infile.readline().split())) for _ in range(n)]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    paths, costs = [], []
    start_time = time.time()
    for i in range(n):
        visited = [False] * n
        path, cost = bfs(i, arr, visited, n)
        paths.append(path)
        costs.append(cost)
    end_time = time.time()

    bfs_time = end_time - start_time

    with open("Results.txt", "w") as outfile:
        for i in range(n):
            outfile.write(f"Vertex {i}:\n")
            outfile.write(f"Path: {'->'.join(map(str, paths[i]))}\n")
            outfile.write(f"Cost: {costs[i]}\n\n")

    update_metrics(n, bfs_time, "P")
    print(f"BFS Time: {bfs_time:.10f} seconds.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Error: No input file provided.")
    else:
        main(sys.argv[1])
