def sort_and_format_metrics(file_path):
    try:
        # Read the metrics data
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Parse the data into a list of tuples
        metrics = []
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                vertices = int(parts[0])
                time = float(parts[1])
                lang = parts[2]
                metrics.append((vertices, time, lang))
        
        # Remove duplicates, keeping only the entry with the lowest time
        unique_metrics = {}
        for vertices, time, lang in metrics:
            key = (vertices, lang)
            if key not in unique_metrics or time < unique_metrics[key]:
                unique_metrics[key] = time
        
        # Convert dictionary back to a list
        metrics = [(v, t, l) for (v, l), t in unique_metrics.items()]
        
        # Sort the data
        metrics.sort(key=lambda x: (x[0], {'C': 1, 'P': 2, 'O': 3}[x[2]]))
        
        # Format the data as required
        formatted_lines = [f"{v}\t{t:.10f}\t{l}" for v, t, l in metrics]
        
        # Ensure the last line is blank
        formatted_lines.append('')
        
        # Write the sorted and formatted data back to the same file
        with open(file_path, 'w') as file:
            file.write('\n'.join(formatted_lines))
        
        print("Metrics file sorted, updated, and formatted successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# File path to the metrics file
file_path = 'Metrics.txt'

# Call the function
sort_and_format_metrics(file_path)
