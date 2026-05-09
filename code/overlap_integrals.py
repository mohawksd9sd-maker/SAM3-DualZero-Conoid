"""
SAM3 v4.20 - Geometric Overlap Integrals for Yukawa / CKM / PMNS
"""

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

NUM_BRIDGES = 12
THETA = np.linspace(0, 2*np.pi, NUM_BRIDGES, endpoint=False)

def projector_overlap(i, j, u_max=8.0):
    def integrand(u):
        dist = np.abs(i - j) * u * 0.15
        kernel = 1.0 / (1.0 + dist**2) * (1 + 0.4 * np.cos(12*(THETA[i]-THETA[j])))
        return kernel
    overlap, _ = quad(integrand, 0, u_max)
    return overlap / u_max

print("Computing 12×12 overlap matrix...\n")
overlap_matrix = np.zeros((NUM_BRIDGES, NUM_BRIDGES))
for i in range(NUM_BRIDGES):
    for j in range(NUM_BRIDGES):
        overlap_matrix[i,j] = projector_overlap(i, j)

overlap_matrix = (overlap_matrix + overlap_matrix.T) / 2
overlap_matrix /= np.max(np.abs(overlap_matrix))

print("Overlap Matrix (rounded):")
print(np.round(overlap_matrix, decimals=4))

plt.figure(figsize=(8,6))
plt.imshow(overlap_matrix, cmap='viridis')
plt.colorbar(label='Geometric Overlap')
plt.title('SAM3 v4.20 - 12-Bridge Projector Overlaps')
plt.xlabel('Bridge Index')
plt.ylabel('Bridge Index')
plt.savefig('overlap_matrix.png', dpi=200, bbox_inches='tight')
plt.show()

print("\n✅ Overlap matrix computed and figure saved.")
