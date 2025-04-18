#!/bin/bash
# Define variables for the input files and directories
XYZ_FILE="n-butane.xyz"
PYTHON_SCRIPT="./rotate_dihedral.py"
TEMPLATE="cp2k_input.inp"
ANGLE_STEP=10
OUTPUT_DIR="results"
# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"
# Loop through angles from 0 to 360 in increments of ANGLE_STEP
for angle in $(seq 0 $ANGLE_STEP 360); do
    # Format angle with zero-padding
    angle_p=$(printf "%03d" "$angle")
    # Create a new XYZ file with the rotated dihedral
    ROTATED_XYZ="${OUTPUT_DIR}/molecule_angle_${angle_p}.xyz"
    python3 "$PYTHON_SCRIPT" "$XYZ_FILE" "$angle" "$ROTATED_XYZ"
    # Check if the new XYZ file was created successfully
    if [[ ! -f "$ROTATED_XYZ" ]]; then
        echo "Error: Rotated XYZ file '$ROTATED_XYZ' not created."
        exit 1
    fi
    # Generate a new .inp file by replacing the placeholder in the template
    INP_FILE="${OUTPUT_DIR}/molecule_angle_${angle_p}.inp"
    sed "s|Reference.xyz|${ROTATED_XYZ}|g" "$TEMPLATE" > "$INP_FILE"
    # Run CP2K with the generated .inp file and save outputs, (Optional use MPI -n cores) 
    mpirun -n 2 cp2k.psmp -i "$INP_FILE" > "${OUTPUT_DIR}/cp2k_output_${angle_p}.log" 2> "${OUTPUT_DIR}/cp2k_error_${angle_p}.log"
    # Extract energy from CP2K output
    energy=$(grep "Total FORCE_EVAL ( QS ) energy" "${OUTPUT_DIR}/cp2k_output_${angle_p}.log" | awk '{print $NF}')
    echo "$angle, $energy" >> "${OUTPUT_DIR}/energy_output${OUTPUT_DIR}.txt"
    echo "Completed angle $angle"
done
echo "All calculations completed."
