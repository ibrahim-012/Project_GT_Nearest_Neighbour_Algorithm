# Metrics_Sort.py

def sort_metrics_file():
    # Read the data from Metrics.txt
    with open("Metrics.txt", "r") as file:
        lines = file.readlines()

    # Define custom sorting order for programming languages
    language_order = {'C': 0, 'P': 1, 'O': 2}

    # Sort the lines first by the number of vertices (column 1), then by programming language (column 3)
    sorted_lines = sorted(lines, key=lambda line: (int(line.split()[0]), language_order[line.split()[2]]))

    # Write the sorted data back to Metrics.txt
    with open("Metrics.txt", "w") as file:
        file.writelines(sorted_lines)

if __name__ == "__main__":
    sort_metrics_file()
