import numpy as np
import matplotlib.pyplot as plt

# Define the constants
G = 6.67408e-11
dt = 0.00001

# Initialize the bodies
bodies = np.zeros((3, 3))
bodies[0, :] = [1, 0, 0]
bodies[1, :] = [0, 1, 0]
bodies[2, :] = [0, 0, 1]

# Calculate the forces
forces = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        if i != j:
            distance = np.linalg.norm(bodies[i, :] - bodies[j, :]) ** 3
            forces[i, :] += G * bodies[i, :] * bodies[j, :] / distance

# Update the positions
bodies += forces * dt

# Plot the bodies
plt.plot(bodies[:, 0], bodies[:, 1], 'o-')
plt.show()
