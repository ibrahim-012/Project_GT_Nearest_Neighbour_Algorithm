#include <iostream>
#include <cstdlib>
#include <ctime>
#include <climits>
#include <cmath>
#include <string>
#include <iomanip>
#include <omp.h>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;

void BFS(int node, int **arr, int **vis, int n, string *v_path, string *w_path)
{
    int start_node = node;
    int min;
    int min_index;
    int visited_count = 0;
    int cost = 0;

    // mark starting node as visited
    vis[node][node] = 1;

    // increment visited nodes count --- all nodes should be visited
    visited_count++;

    // append starting vertex to v_path for printing later
    v_path[node].append(to_string(node));

    while (visited_count < n)
    {
        min = INT_MAX;

        for (int i = 0; i < n; i++)
        {
            if (arr[start_node][i] < min && start_node != i && vis[node][i] == 0)
            {
                min = arr[start_node][i];
                min_index = i;
            }
        }
        start_node = min_index;
        cost += min;
        vis[node][min_index] = 1;
        visited_count++;

        // append next visited vertex to v_path
        v_path[node].append("->");
        v_path[node].append(to_string(min_index));

        // append edge weight between last node and visited node to w_path
        w_path[node].append("->");
        w_path[node].append(to_string(min));
    }
    cost += arr[min_index][node];

    // append starting vertex to v_path to complete Hamiltonian cycle
    v_path[node].append("->");
    v_path[node].append(to_string(node));

    // append edge weight between last visited node and start node to w_path
    w_path[node].append("->");
    w_path[node].append(to_string(arr[min_index][node]));

    ofstream results("Results.txt", ios::app);
    results << endl
            << "Vertex: " << node << endl
            << "Path:     " << v_path[node] << endl
            << "Weights: " << w_path[node] << endl
            << "Cost: " << cost << endl;
    results.close();
}

// Function to check and update the metrics file
void updateMetricsFile(const string &filename, int n, double bfs_time, const string &language)
{
    ifstream infile(filename);
    string line;
    bool entryFound = false;
    vector<string> lines;

    // Read all lines and look for the existing entry
    while (getline(infile, line))
    {
        stringstream ss(line);
        int data_size;
        double existing_time;
        string lang;
        ss >> data_size >> existing_time >> lang;

        if (data_size == n && lang == language) // Check if entry exists for this data size and language
        {
            entryFound = true;
            // Store the line with the smaller time
            if (bfs_time < existing_time)
            {
                // Use ostringstream to format bfs_time with fixed and setprecision
                ostringstream time_stream;
                time_stream << fixed << setprecision(6) << bfs_time;
                line = to_string(n) + "\t" + time_stream.str() + "\t" + language;
            }
        }
        lines.push_back(line);
    }

    infile.close();

    // If the entry was found and updated, write all lines back
    ofstream outfile(filename);
    for (const auto &l : lines)
    {
        outfile << l << endl;
    }

    // If no entry found, append the new entry
    if (!entryFound)
    {
        outfile << n << "\t" << fixed << setprecision(6) << bfs_time << "\t" << language << endl;
    }

    outfile.close();
}

int main(int argc, char **argv)
{
    string filename = argv[1];
    int thread_count = atoi(argv[2]);
    string language = "O";

    // Open the file and read the adjacency matrix
    ifstream infile(filename);

    int n;
    infile >> n;

    int **arr = new int *[n];
    #pragma omp parallel for num_threads(thread_count)
    for (int i = 0; i < n; i++)
    {
        arr[i] = new int[n];
    }

// Read the adjacency matrix from the file
#pragma omp parallel for collapse(2) num_threads(thread_count)
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            infile >> arr[i][j];
        }
    }

    infile.close();

    // Allocation of visited array
    int **vis = new int *[n];
    for (int i = 0; i < n; i++)
    {
        vis[i] = new int[n];
    }

    // Allocation of arrays to hold vertices and edge weights for printing paths
    string v_path[n];
    string w_path[n];

// Initialize visited array
#pragma omp parallel for collapse(2) num_threads(thread_count)
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            vis[i][j] = 0;
        }
    }

    double bfs_start = omp_get_wtime();

// Calling BFS function for each vertex
#pragma omp parallel for num_threads(thread_count)
    for (int i = 0; i < n; i++)
    {
        BFS(i, arr, vis, n, v_path, w_path);
    }

    double bfs_end = omp_get_wtime();
    double bfs_time = bfs_end - bfs_start;

    // Print processing time
    cout << fixed << setprecision(6) << "BFS Time: " << bfs_time << " seconds." << endl;

    // Store BFS time in metrics file with check and update logic
    updateMetricsFile("Metrics.txt", n, bfs_time, language);

    // Free memory
    for (int i = 0; i < n; i++)
    {
        delete[] arr[i];
        delete[] vis[i];
    }
    delete[] arr;
    delete[] vis;

    return 0;
}
