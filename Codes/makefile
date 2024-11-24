# Rule to compile serial cpp file
serial:
	g++ TSP_Serial.cpp -o TSP_S
	./TSP_S $(ARG)

# Rule to compile parallel cpp file
parallel:
	g++ -fopenmp TSP_Parallel.cpp -o TSP_P
	./TSP_P $(ARG) 4

# Rule to run serial python
py:
	python3 TSP_Serial.py $(ARG)

# Rule to generate data files
data:
	g++ data_generator.cpp -o data_generator
	./data_generator $(ARG)

# Rule to run gui interface
gui:
	g++ TSP_Serial.cpp -o TSP_S
	g++ -fopenmp TSP_Parallel.cpp -o TSP_P
	python3 gui.py

# Rule to sort metrics file
sort_metrics:
	python3 Metrics_Sort.py

# Rule to automate running of files - input size 100 to 1000 - step size 1000
run_files:
	./run_files.sh

# Rule to create line graph - metrics file will be sorted first
graphs_line:
	make sort_metrics
	python3 graphs_line.py

# Rule to create scatter plot - metrics file will be sorted first
graphs_scatter:
	make sort_metrics
	python3 graphs_scatter.py

# Rule to create bar graph - metrics file will be sorted first
graphs_bar:
	make sort_metrics
	python3 graphs_bar.py

# Rule to remove the executable and object files created by g++ compilation
clean_executables:
	@rm -f TSP_S TSP_P data_generator *.o

clean_data:
	@rm -f d*.txt
