# plot_benchmark.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("benchmark_results.csv")

# Filter
serial_time = df[df["Type"] == "Serial"]["TotalTime"].values[0]
dist = df[df["Type"] == "Distributed"]

# Speedup
dist["Speedup"] = serial_time / dist["TotalTime"]

# --- Execution Time ---
plt.figure(figsize=(10,6))
plt.plot(dist["Processes"], dist["TotalTime"], marker='o', label='Distributed')
plt.axhline(serial_time, color='r', linestyle='--', label='Serial')
plt.xlabel("Processes")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Processes")
plt.grid(True)
plt.legend()
plt.savefig("execution_time_plot.png")
plt.show()

# --- Speedup ---
plt.figure(figsize=(10,6))
plt.plot(dist["Processes"], dist["Speedup"], marker='s', color='green')
plt.xlabel("Processes")
plt.ylabel("Speedup")
plt.title("Speedup vs Processes")
plt.grid(True)
plt.savefig("speedup_plot.png")
plt.show()

# --- Efficiency ---
plt.figure(figsize=(10,6))
plt.plot(dist["Processes"], dist["Efficiency"], marker='^', color='purple')
plt.xlabel("Processes")
plt.ylabel("Efficiency")
plt.title("Efficiency vs Processes")
plt.grid(True)
plt.savefig("efficiency_plot.png")
plt.show()

# --- Compute vs Communication Time (Stacked Bar) ---
plt.figure(figsize=(10,6))
plt.bar(dist["Processes"], dist["ComputeTime"], label='Compute Time')
plt.bar(dist["Processes"], dist["CommTime"], bottom=dist["ComputeTime"], label='Communication Time')
plt.xlabel("Processes")
plt.ylabel("Time (s)")
plt.title("Compute vs Communication Time Breakdown")
plt.legend()
plt.grid(True)
plt.savefig("comp_comm_plot.png")
plt.show()
