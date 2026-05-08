"""
SAM3 v4.19 - Right Conoid with 12 Bridges Visualization
Simple 3D plot of the right conoid showing the 12 icosahedral bridges.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(-10, 10, 200)
v = np.linspace(0, 2*np.pi, 200)
U, V = np.meshgrid(u, v)
X = U * np.cos(V)
Y = U * np.sin(V)
Z = 1.8 * np.sin(2 * V)

ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis', linewidth=0)

# Plot the 12 bridges (rulings)
angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
for theta in angles:
    x_line = np.linspace(-8, 8, 100) * np.cos(theta)
    y_line = np.linspace(-8, 8, 100) * np.sin(theta)
    z_line = 1.8 * np.sin(2 * theta)
    ax.plot(x_line, y_line, z_line + np.zeros_like(x_line), 'r-', linewidth=2)

ax.set_title('SAM3 v4.19 - Right Conoid with 12 Icosahedral Bridges')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

print("✅ Conoid visualization complete. 12 red lines = the bridges.")
