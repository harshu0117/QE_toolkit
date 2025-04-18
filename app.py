# app.py
import streamlit as st
import os
from qe_runner import run_convergence_test
from utils import plot_convergence, detect_convergence

st.set_page_config(layout="wide")
st.title("Quantum ESPRESSO Convergence Tester")

# File upload section
uploaded_file = st.file_uploader("Upload QE input file (.in)", type=["in"])
test_type = st.selectbox("Choose test type", ["K-Point Convergence", "Energy Cutoff Convergence"])
value_str = st.text_input("Enter values (comma-separated):", placeholder="e.g. 2,4,6,8")  # User input for k or ecutwfc

# WSL QE package path
qe_path = st.text_input("Enter the path to Quantum ESPRESSO executable", value="\\wsl.localhost\\Ubuntu\\home\\harsh17\\quantum_espresso")

if st.button("Run Convergence Test") and uploaded_file and qe_path:
    values = [int(x.strip()) for x in value_str.split(",")]

    # Save input file to 'inputs' folder
    os.makedirs("inputs", exist_ok=True)
    input_path = os.path.join("inputs", "base.in")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    energies, actual_values = run_convergence_test(
        input_path=input_path,
        test_type=test_type,
        values=values,
        qe_path=qe_path
    )

    if energies:
        st.subheader("Convergence Plot")
        plot_convergence(actual_values, energies)

        idx = detect_convergence(energies)
        if idx is not None:
            st.success(f"Converged at {actual_values[idx]} with ΔE ≈ 0.001 Ry")
        else:
            st.warning("No convergence detected within the given range.")
