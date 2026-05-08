"""
SAM3 v4.19 - Conoid Bridges Figure
Generates conoid_bridges.png for the paper.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate the conoid surface
u = np.linspace(-12, 12, 150)
v = np.linspace(0, 2*np.pi, 150)
U, V = np.meshgrid(u, v)
X = U * np.cos(V)
Y = U * np.sin(V)
Z = 1.8 * np.sin(2 * V)

# Plot the surface
ax.plot_surface(X, Y, Z, alpha=0.65, cmap='viridis', linewidth=0, antialiased=True)

# Plot the 12 bridge rulings (red lines)
angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
for theta in angles:
    x_line = np.linspace(-10, 10, 80) * np.cos(theta)
    y_line = np.linspace(-10, 10, 80) * np.sin(theta)
    z_line = 1.8 * np.sin(2 * theta) * np.ones_like(x_line)
    ax.plot(x_line, y_line, z_line, 'r-', linewidth=2.5, alpha=0.9)

ax.set_title('Right Conoid with 12 Icosahedral Bridge Rulings', fontsize=14)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=25, azim=-45)

plt.tight_layout()
plt.savefig('figures/conoid_bridges.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Figure saved as 'figures/conoid_bridges.png'")
