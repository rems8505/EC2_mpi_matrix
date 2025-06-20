# distributed_mm.py
from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 500  # Matrix dimension
assert N % size == 0, f"Matrix size {N} not divisible by number of processes {size}"
rows_per_proc = N // size

# Initialize matrices at root
if rank == 0:
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)
    start_total = time.time()
else:
    A = None
    B = None

# Communication timing starts
comm_start = time.time()

# Broadcast matrix B to all processes
B = comm.bcast(B, root=0)

# Scatter rows of A
A_sub = np.zeros((rows_per_proc, N))
comm.Scatter([A, MPI.DOUBLE], [A_sub, MPI.DOUBLE], root=0)

comm_end = time.time()
comm_time = comm_end - comm_start

# Compute timing
comp_start = time.time()
C_sub = np.dot(A_sub, B)
comp_end = time.time()
comp_time = comp_end - comp_start

# Gather results
comm_start2 = time.time()
if rank == 0:
    C = np.zeros((N, N))
else:
    C = None
comm.Gather([C_sub, MPI.DOUBLE], [C, MPI.DOUBLE], root=0)
comm_end2 = time.time()

comm_time += (comm_end2 - comm_start2)

# Finalize
if rank == 0:
    total_time = time.time() - start_total
    # Log values to a temp file for collection by benchmark.py
    with open("perf_metrics_rank0.txt", "w") as f:
        f.write(f"{total_time},{comp_time},{comm_time}")
    print(f"Distributed Execution Time: {total_time:.4f} s, Compute: {comp_time:.4f} s, Comm: {comm_time:.4f} s")
