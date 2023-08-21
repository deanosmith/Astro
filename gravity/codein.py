import numpy as np

class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.force = np.zeros(3)

def compute_forces(bodies, G):
    for body in bodies:
        body.force = np.zeros(3)
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            r = bodies[j].position - bodies[i].position
            mag = G * bodies[i].mass * bodies[j].mass / np.linalg.norm(r)**3
            bodies[i].force += mag * r
            bodies[j].force -= mag * r

def integrate(bodies, dt):
    for body in bodies:
        body.velocity += body.force / body.mass * dt
        body.position += body.velocity * dt

def simulate(bodies, G, dt, steps):
    for _ in range(steps):
        compute_forces(bodies, G)
        integrate(bodies, dt)
