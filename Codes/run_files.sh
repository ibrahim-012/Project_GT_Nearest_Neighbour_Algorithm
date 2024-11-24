#!/bin/bash

# Loop over dataset sizes from 100 to 1000 with step size of 100
for size in {100..1000..100}
do
    make data ARG=$size
    make serial ARG="data_${size}.txt"
    make parallel ARG="data_${size}.txt"
    make py ARG="data_${size}.txt"
done

make sort_metrics
make clean_executables