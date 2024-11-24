#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <climits>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <map>

using namespace std;

// Function to perform BFS and calculate Hamiltonian cycle for a specific start node
void BFS(int node, vector<vector<int>> &arr, vector<int> &visited, int n, string &path, int &cost)
{
  int start_node = node;
  int min_cost;
  int next_node;
  int visited_count = 0;

  // Mark starting node as visited
  visited[start_node] = 1;
  visited_count++;
  cost = 0;

  // Append starting vertex to the path
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
      break; // No valid next node (shouldn't happen for a complete graph)

    visited[next_node] = 1;
    visited_count++;
    cost += min_cost;

    ss << "->" << next_node;
    start_node = next_node;
  }

  // Return to the starting node to complete the cycle
  cost += arr[start_node][node];
  ss << "->" << node;

  path = ss.str();
}

// Function to check and update the metrics file
void updateMetricsFile(const string &filename, int n, double bfs_time, string language)
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

int main(int argc, char *argv[])
{
  string filename = argv[1];
  string language = "C";
  
  ifstream infile(filename);
  if (!infile.is_open())
  {
    cerr << "Error: Unable to open file " << filename << endl;
    return 1;
  }

  int n;
  infile >> n;

  vector<vector<int>> arr(n, vector<int>(n, 0));
  vector<int> visited(n, 0);
  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < n; j++)
    {
      infile >> arr[i][j];
    }
  }
  infile.close();

  vector<string> paths(n);
  vector<int> costs(n);

  clock_t bfs_start = clock();
  for (int i = 0; i < n; i++)
  {
    fill(visited.begin(), visited.end(), 0);
    BFS(i, arr, visited, n, paths[i], costs[i]);
  }
  clock_t bfs_end = clock();

  double bfs_time = double(bfs_end - bfs_start) / CLOCKS_PER_SEC;

  // Write results to an output file
  ofstream outfile("Results.txt");
  if (outfile.is_open())
  {
    for (int i = 0; i < n; i++)
    {
      outfile << "Vertex " << i << ":\n";
      outfile << "Path: " << paths[i] << "\n";
      outfile << "Cost: " << costs[i] << "\n\n";
    }
    outfile.close();
  }
  else
  {
    cerr << "Error: Unable to write results to file.\n";
  }

  // Store BFS time in metrics file with check and update logic
  updateMetricsFile("Metrics.txt", n, bfs_time, language);

  cout << fixed << setprecision(6) << "BFS Time: " << bfs_time << " seconds." << endl;

  return 0;
}
