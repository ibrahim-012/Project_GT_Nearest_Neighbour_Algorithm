@echo off

REM Compile the C++ files before the loop
g++ TSP_Serial.cpp -o tsp_c
g++ TSP_Parallel.cpp -o tsp_o -fopenmp

REM Loop over dataset sizes from 10 to 50 with step size of 5
for /L %%i in (10,5,50) do (
    REM Run the serial, parallel, and Python versions with the appropriate dataset
    tsp_c data_%%i.txt
    tsp_o data_%%i.txt 4
    python TSP_Serial.py data_%%i.txt

)

REM Call the Python script to sort and format the metrics file
python Metrics_Sort.py

REM Optional: Clean up the executables after running each dataset
del tsp_c
del tsp_o
