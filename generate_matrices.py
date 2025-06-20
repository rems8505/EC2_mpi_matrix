# generate_matrices.py
import numpy as np

def generate_matrix(N):
    return np.random.rand(N, N)

if __name__ == "__main__":
    N = 500
    A = generate_matrix(N)
    B = generate_matrix(N)
    np.save("A.npy", A)
    np.save("B.npy", B)
