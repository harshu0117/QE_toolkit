# qe_runner.py
import subprocess
import os
import re

def modify_input(input_file, test_type, value):
    # Read the input file and modify it based on test type and value
    with open(input_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if test_type == "K-Point Convergence" and line.strip().startswith("K_POINTS"):
            new_lines.append("K_POINTS automatic\n")
            new_lines.append(f"{value} {value} {value} 0 0 0\n")
            break
        elif test_type == "Energy Cutoff Convergence" and "ecutwfc" in line:
            new_lines.append(f"  ecutwfc = {value},\n")
        else:
            new_lines.append(line)

    # Save the modified input file with a new name based on the value
    modified_path = f"inputs/tmp_{value}.in"
    with open(modified_path, "w") as f:
        f.writelines(new_lines)

    return modified_path

def extract_total_energy(output_path):
    # Extract total energy from the output file
    energy = None
    with open(output_path, "r") as f:
        for line in f:
            if "!    total energy" in line:
                energy = float(line.split()[-2])  # Extract energy value (in Ry)
                break
    return energy

def run_convergence_test(input_path, test_type, values, qe_path):
    energies = []
    actual_values = []

    os.makedirs("outputs", exist_ok=True)

    for v in values:
        modified_input = modify_input(input_path, test_type, v)
        output_file = modified_input.replace("inputs", "outputs").replace(".in", ".out")

        # Construct the full path for QE executable in WSL
        cmd = f"{qe_path}/bin/pw.x < {modified_input} > {output_file}"
        
        # Run the QE command inside WSL
        subprocess.run(["wsl", cmd], shell=False)

        # Extract energy value from the output file
        energy = extract_total_energy(output_file)
        if energy is not None:
            energies.append(energy)
            actual_values.append(v)

    return energies, actual_values
