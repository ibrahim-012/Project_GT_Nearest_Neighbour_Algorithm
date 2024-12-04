#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
using namespace std;

void generateData(int num_vertices, const string &filename)
{
    ofstream outFile(filename);
    
    // Write the number of vertices in first line of file
    outFile << num_vertices << "\n";

    // Seed the random number generator
    srand(time(NULL));

    // Create the adjacency matrix (num_vertices x num_vertices)
    vector<vector<int>> matrix(num_vertices, vector<int>(num_vertices));

    // Fill the matrix with random weights (ensuring symmetry)
    for (int i = 0; i < num_vertices; ++i)
    {
        for (int j = 0; j < num_vertices; ++j)
        {
            if (i == j)
            {
                matrix[i][j] = 0; // No loops allowed (diagonal elements are 0)
            }
            else if (i < j)
            {
                int weight = rand() % 100 + 1; // Random weight between 1 and 100
                matrix[i][j] = weight;
                matrix[j][i] = weight; // Ensure the matrix is symmetric
            }
        }
    }

    // Write the matrix to the file
    for (int i = 0; i < num_vertices; ++i)
    {
        for (int j = 0; j < num_vertices; ++j)
        {
            outFile << matrix[i][j];
            if (j < num_vertices - 1)
            {
                outFile << "\t"; // Tab separator
            }
        }
        outFile << "\n"; // Begin new line for next vertex
    }

    outFile.close();
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        cout << "Usage: " << argv[0] << " <number_of_vertices>" << endl;
        return 1;
    }

    int num_vertices = atoi(argv[1]);

    string filename = "data_" + to_string(num_vertices) + ".txt";
    generateData(num_vertices, filename);

    cout << "Data generated in file: " << filename << endl;

    return 0;
}