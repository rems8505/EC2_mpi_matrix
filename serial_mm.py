# serial_mm.py
import numpy as np
import time

def serial_matrix_multiply(A, B):
    return np.dot(A, B)

if __name__ == "__main__":
    N = 600
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    start_time = time.time()
    C = serial_matrix_multiply(A, B)
    end_time = time.time()

    print("Serial Execution Time: {:.4f} seconds".format(end_time - start_time))
