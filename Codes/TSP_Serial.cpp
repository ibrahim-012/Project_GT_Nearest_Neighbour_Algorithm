#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <climits>
#include <ctime>
#include <iomanip>
#include <sstream>

using namespace std;

// Function to perform BFS and calculate Hamiltonian cycle for a specific start node
void BFS(int node, const vector<vector<int>> &arr, vector<int> &visited, int n, string &path, int &cost)
{
  int start_node = node;
  int min_cost;
  int next_node;
  int visited_count = 0;

  visited[start_node] = 1; // Mark starting node as visited
  visited_count++;
  cost = 0;

  stringstream ss;
  ss << node;

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

    ss << "->" << next_node;
    start_node = next_node;
  }

  cost += arr[start_node][node];
  ss << "->" << node;

  path = ss.str();
}

// Function to update metrics file directly
void updateMetricsFile(const string &filename, int n, double bfs_time, const string &language)
{
  ofstream outfile(filename, ios::app);
  outfile << n << "\t" << fixed << setprecision(10) << bfs_time << "\t" << language << endl;
  outfile.close();
}

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    cerr << "Usage: " << argv[0] << " <input_filename>" << endl;
    return 1;
  }

  string filename = argv[1];
  ifstream infile(filename);
  if (!infile.is_open())
  {
    cerr << "Error: Unable to open file " << filename << endl;
    return 1;
  }

  int n;
  infile >> n;

  vector<vector<int>> arr(n, vector<int>(n, 0));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      infile >> arr[i][j];

  infile.close();

  vector<string> paths(n);
  vector<int> costs(n);

  clock_t bfs_start = clock();
  for (int i = 0; i < n; i++)
  {
    vector<int> visited(n, 0);
    BFS(i, arr, visited, n, paths[i], costs[i]);
  }
  clock_t bfs_end = clock();

  double bfs_time = double(bfs_end - bfs_start) / CLOCKS_PER_SEC;

  ofstream outfile("Results.txt");
  for (int i = 0; i < n; i++)
  {
    outfile << "Vertex " << i << ":\n";
    outfile << "Path: " << paths[i] << "\n";
    outfile << "Cost: " << costs[i] << "\n\n";
  }
  outfile.close();

  updateMetricsFile("Metrics.txt", n, bfs_time, "C");

  cout << "BFS Time: " << fixed << setprecision(10) << bfs_time << " seconds." << endl;

  return 0;
}