# utils.py
import matplotlib.pyplot as plt
import streamlit as st

def plot_convergence(x_vals, energies):
    # Plot the convergence graph
    fig, ax = plt.subplots()
    ax.plot(x_vals, energies, marker="o", linestyle="-", color="blue")
    ax.set_xlabel("K-point Grid" if len(x_vals) > 0 and isinstance(x_vals[0], int) else "ecutwfc (Ry)")
    ax.set_ylabel("Total Energy (Ry)")
    ax.set_title("Convergence Plot")
    ax.grid(True)
    st.pyplot(fig)

def detect_convergence(energies, threshold=0.001):  # in Ry
    # Check for convergence (difference between consecutive energies < threshold)
    for i in range(1, len(energies)):
        delta = abs(energies[i] - energies[i-1])
        if delta < threshold:
            return i
    return None
