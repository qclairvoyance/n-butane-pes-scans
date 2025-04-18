#!/bin/bash
# Loop over the range of theta angles (0 to 360 degrees in steps of 20)
for angle in $(seq 000 010 360); do
	 x=$(printf "%03d" $angle)
    # Define the output file name based on the angle
    output_file="butane_rotation_${x}_HF.nw"
    
    # Run the Python script and capture the output in the specified file
    python3 generate_nwchem_input_HF.py $x > "$output_file"

    # Check if the file was created successfully
    if [[ -f "$output_file" ]]; then
        echo "Generated NWChem input file: $output_file"
    else
        echo "Error: Failed to create $output_file"
    fi
done
