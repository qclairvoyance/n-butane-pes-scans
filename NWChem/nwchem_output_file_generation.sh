#!/bin/bash

START_TIME=$(date +%s)

# Set path to NWChem executable
NWCHEM_EXE= {path}/nwchem.openmpi  # Path to your NWChem executable

# Loop over the range of x from 0 to 100 with a step of 20
for angel in $(seq 0 10 360);
do
	 x=$(printf "%03d" $angel)
    # Define the input and output file names in the same directory
    INPUT_FILE="butane_rotation_${x}_HF.nw"
    OUTPUT_FILE="butane_rotation_${x}_HF_output.out"

    echo "Running NWChem calculation for input: $INPUT_FILE"

    # Run the NWChem calculation and redirect output to the output file
    $NWCHEM_EXE $INPUT_FILE > $OUTPUT_FILE
done

 grep "Total SCF energy" butane_rotation_*_HF_output.out > list_all
 awk '/Total SCF energy/ {print substr(FILENAME, 17, 3), $NF}' butane_rotation_*_HF_output.out > list


END_TIME=$(date +%s)

# Calculate total execution time
TOTAL_TIME=$((END_TIME - START_TIME))

# Convert total time to hours, minutes, and seconds
HOURS=$((TOTAL_TIME / 3600))
MINUTES=$(((TOTAL_TIME % 3600) / 60))
SECONDS=$((TOTAL_TIME % 60))

# Append total execution time to the 'list' file
echo "Total time required = ${HOURS}h ${MINUTES}m ${SECONDS}s" >> list

# Plot the results with xmgrace
xmgrace list
