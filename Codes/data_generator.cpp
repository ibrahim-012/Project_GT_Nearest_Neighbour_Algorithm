#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <string>
using namespace std;

void generateData(int num_vertices, const string &filename)
{
    ofstream outFile(filename);
    
    // Write the number of vertices in first line of file
    outFile << num_vertices << "\n";

    // Seed the random number generator
    srand(time(NULL));

    // Generate the adjacency matrix
    for (int i = 0; i < num_vertices; ++i)
    {
        for (int j = 0; j < num_vertices; ++j)
        {
            if (i == j)
            {
                outFile << "0"; // No loops allowed
            }
            else
            {
                int weight = rand() % 100 + 1; // Random weight between 1 and 100
                outFile << weight;
            }
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
    int num_vertices = atoi(argv[1]);

    string filename = "data_" + to_string(num_vertices) + ".txt";
    generateData(num_vertices, filename);

    return 0;
}
