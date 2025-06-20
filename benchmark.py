# benchmark.py
import subprocess
import time
import csv
import os

def run_serial():
    print("=== Serial ===")
    start = time.time()
    subprocess.run(["python3", "serial_mm.py"])
    end = time.time()
    return end - start

def run_distributed(hostfile, num_procs):
    print(f"=== Distributed: {num_procs} process(es) ===")
    subprocess.run([
        "mpirun", "-n", str(num_procs), "--hostfile", hostfile,
        "python3", "distributed_mm.py"
    ])
    # Only rank 0 writes perf_metrics_rank0.txt
    with open("perf_metrics_rank0.txt") as f:
        total_time, comp_time, comm_time = map(float, f.read().strip().split(","))
    return total_time, comp_time, comm_time

if __name__ == "__main__":
    hostfile = "hosts.txt"

    with open(hostfile) as f:
        host_list = [line.strip() for line in f if line.strip()]
    max_procs = len(host_list)

    results = []

    # Serial
    serial_time = run_serial()
    results.append(["Serial", 1, serial_time, serial_time, 0, 1.0])  # (Type, Procs, Total, Comp, Comm, Efficiency)

    # Distributed
    for p in range(1, max_procs + 1):
        with open("temp_hosts.txt", "w") as f:
            f.write("\n".join(host_list[:p]))

        total, comp, comm = run_distributed("temp_hosts.txt", p)
        speedup = serial_time / total
        efficiency = speedup / p
        results.append(["Distributed", p, total, comp, comm, efficiency])

    with open("benchmark_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Processes", "TotalTime", "ComputeTime", "CommTime", "Efficiency"])
        writer.writerows(results)

    print("Benchmark results saved to benchmark_results.csv")
