@echo off
REM Loop over dataset sizes from 10 to 50 with step size of 5
for /L %%i in (5,5,50) do (
    REM Compile the data_generator.cpp file
    g++ data_generator.cpp -o data_generator.exe

    REM Run the data generator to create the data files
    data_generator.exe %%i

    REM Clean up the executable after generating data
    del data_generator.exe
)

echo Data generation completed.
