import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')

class Body:
    def __init__(self, mass, position, velocity, color):
        self.mass = mass  # mass of the body
        self.position = np.array(position, dtype='float64')  # initial position of the body in the space
        self.velocity = np.array(velocity, dtype='float64')  # initial velocity of the body
        self.color = color  # color of the body in the plot

# Define gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Define bodies in the solar system
# Positions and velocities are set so that the planets start at the positive x-axis and move in the positive y-direction
sun = Body(1.989e30, [0, 0, 0], [0, 0, 0], 'orange')
# sun = Body(1.989e30, [0, 0, 0], [0, 0, 0], 'orange', 'Sun', fixed=False)
earth = Body(5.972e24, [1.496e11, 0, 0], [0, 2.9783e4, 0], 'blue')
moon = Body(7.342e22, [1.496e11, 3.844e8, 0], [1.022e3, 2.9783e4, 0], 'grey')
mercury = Body(3.301e23, [5.791e10, 0, 0], [0, 4.736e4, 0], 'yellow')
venus = Body(4.867e24, [1.082e11, 0, 0], [0, 3.502e4, 0], 'green')
mars = Body(6.417e23, [2.279e11, 0, 0], [0, 2.407e4, 0], 'red')
jupiter = Body(1.899e27, [7.785e11, 0, 0], [0, 1.307e4, 0], 'orange')
saturn = Body(5.685e26, [1.434e12, 0, 0], [0, 9.68e3, 0], 'goldenrod')
uranus = Body(8.682e25, [2.871e12, 0, 0], [0, 6.8e3, 0], 'lightblue')
neptune = Body(1.024e26, [4.495e12, 0, 0], [0, 5.43e3, 0], 'blue')

# Put the bodies in a list
bodies = [
    sun
    , mercury
    , venus
    , earth
    , moon
    , mars
    # , jupiter
    # , saturn
    # , uranus
    # , neptune
    ]

size_dict = {
    sun: 20,
    mercury: 10,
    venus: 10,
    earth: 10,
    moon: 5,
    mars: 10,
    jupiter: 15,
    saturn: 14,
    uranus: 13,
    neptune: 12
}



# Define a function that will compute the derivatives of the position and velocity
def compute_derivatives(y, t, bodies):
    n = len(bodies)
    result = np.zeros((n, 6))
    positions = y.reshape(n, 6)

    # Loop over all bodies and calculate the acceleration due to all other bodies
    for i in range(n):
        body1 = bodies[i]
        r1 = positions[i, :3]
        v1 = positions[i, 3:]
        
        a = np.zeros(3)  # acceleration
        for j in range(n):
            if i != j:
                body2 = bodies[j]
                r2 = positions[j, :3]
                r = np.linalg.norm(r2 - r1)
                a += G * body2.mass * (r2 - r1) / r**3

        result[i, :3] = v1  # derivative of position is velocity
        result[i, 3:] = a  # derivative of velocity is acceleration

    return result.reshape(6*n)

# Combine all the positions and velocities into a single array to use as initial conditions
y0 = np.zeros((len(bodies), 6))
for i, body in enumerate(bodies):
    y0[i, :3] = body.position
    y0[i, 3:] = body.velocity
y0 = y0.reshape(6*len(bodies))

# Define the times for which we want the solution: from t=0 to t=3.154e7 (1 year) with 2000 points in-between
# t = np.linspace(0, 3.154e7, 12)
t = np.linspace(0, 10 * 3.154e7, 3650)

# Solve the system of differential equations
solution = odeint(compute_derivatives, y0, t, args=(bodies,))

max_distance = max(np.linalg.norm(body.position) for body in bodies)


# Set up the figure with a specific size (10x10 in this case)
fig, ax = plt.subplots(figsize=(10, 10))  # You can adjust the size to fit your needs
ax.set_xlim(-max_distance*1.2, max_distance*1.2)
ax.set_ylim(-max_distance*1.2, max_distance*1.2)
ax.set_aspect('equal', adjustable='box')

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Create a plot object for each body and a trail (line) for each body
points = [plt.plot([], [], color=body.color, marker='o', markersize=size_dict.get(body, 10))[0] for body in bodies]
lines = [plt.plot([], [], color=body.color)[0] for body in bodies]

# Initialize the plot objects
def init():
    for point, line in zip(points, lines):
        point.set_data([], [])
        line.set_data([], [])
    
    time_text.set_text('')  # Set the initial timestamp to empty
    return points + lines + [time_text]  # Add time_text to the returned objects

# Update function to draw each frame in the animation
def update(i):
    year = i // 12  # Calculate the current year

    # Update the time legend
    time_text.set_text('Year: {}'.format(year))

    for j, (point, line) in enumerate(zip(points, lines)):
        x = solution[:i+1, j*6]
        y = solution[:i+1, j*6+1]
        point.set_data(x[-1], y[-1])  # update the position of the body in the current frame
        line.set_data(x, y)  # update the trail of the body with all previous positions
    return points + lines + [time_text]  # Add time_text to the returned objects


# Create an animation
ani = FuncAnimation(fig, update, frames=range(0, len(t), 1), init_func=init, blit=True)

plt.show()  # display the animation
