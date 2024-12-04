import csv

def process_metrics(input_file, output_file):
    # Initialize a dictionary to store processing times
    data = {}

    # Read the Metrics.txt file
    with open(input_file, "r") as file:
        for line in file:
            # Split each line into input size, time, and language
            size, time, language = line.split()
            size = int(size)
            time = float(time)

            # Organize the data by input size and language
            if size not in data:
                data[size] = {"C": None, "P": None, "O": None}
            
            if language == "C":
                data[size]["C"] = time
            elif language == "P":
                data[size]["P"] = time
            elif language == "O":
                data[size]["O"] = time

    # Write the data to a CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(["Input Size", "C++ Serial", "Python", "OpenMP"])
        
        # Write the data
        for size in sorted(data.keys()):
            writer.writerow([size, data[size]["C"], data[size]["P"], data[size]["O"]])

# Specify the input and output file paths
input_file = "Metrics.txt"
output_file = "Metrics.csv"

# Process the metrics and generate the CSV
process_metrics(input_file, output_file)

print(f"Metrics have been successfully written to {output_file}.")
