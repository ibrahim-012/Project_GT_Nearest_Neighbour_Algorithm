#include <iostream>
#include <fstream>
#include <vector>
#include <omp.h>
#include <climits>
#include <iomanip>
#include <string>

using namespace std;

void BFS(int node, const vector<vector<int>> &arr, vector<int> &visited, int n, string &path, int &cost)
{
    int start_node = node;
    int min_cost, next_node;
    int visited_count = 0;
    cost = 0;

    visited[start_node] = 1;
    visited_count++;

    path = to_string(node);

    while (visited_count < n)
    {
        min_cost = INT_MAX;
        next_node = -1;

        for (int i = 0; i < n; i++)
        {
            if (!visited[i] && arr[start_node][i] < min_cost)
            {
                min_cost = arr[start_node][i];
                next_node = i;
            }
        }

        if (next_node == -1)
            break;

        visited[next_node] = 1;
        visited_count++;
        cost += min_cost;
        path += "->" + to_string(next_node);
        start_node = next_node;
    }

    cost += arr[start_node][node];
    path += "->" + to_string(node);
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        cerr << "Usage: " << argv[0] << " <input_file> <threads>" << endl;
        return 1;
    }

    string filename = argv[1];
    int threads = stoi(argv[2]);

    ifstream infile(filename);
    int n;
    infile >> n;

    vector<vector<int>> arr(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            infile >> arr[i][j];

    infile.close();

    vector<string> paths(n);
    vector<int> costs(n);

    double bfs_start = omp_get_wtime();
#pragma omp parallel for num_threads(threads)
    for (int i = 0; i < n; i++)
    {
        vector<int> visited(n, 0);
        BFS(i, arr, visited, n, paths[i], costs[i]);
    }
    double bfs_end = omp_get_wtime();

    double bfs_time = bfs_end - bfs_start;

    ofstream outfile("Results.txt");
    for (int i = 0; i < n; i++)
    {
        outfile << "Vertex " << i << ":\n";
        outfile << "Path: " << paths[i] << "\n";
        outfile << "Cost: " << costs[i] << "\n\n";
    }
    outfile.close();

    ofstream metrics("Metrics.txt", ios::app);
    metrics << n << "\t" << fixed << setprecision(10) << bfs_time << "\tO" << endl;
    metrics.close();

    cout << "BFS Time: " << fixed << setprecision(10) << bfs_time << " seconds." << endl;

    return 0;
}
