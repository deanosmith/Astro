import os
import pygame
import pygame.math as math

# Constants for our simulation
# Window size
WIDTH, HEIGHT = 1000, 600
# Frames per second - this determines the "speed" of our simulation
FPS = 100
# Gravitational constant for our simulation
G = 1
# Length of the trail
TRAIL_LENGTH = 1000
# Increase the flow of time
TIME_SPEED = 5
# Radius of the bodies (used for collision detection)
BODY_RADIUS = 5

# Body properties (position, velocity, mass)
bodies = [
    {
        "pos": math.Vector2(WIDTH / 3, HEIGHT / 2),  # initial position
        "vel": math.Vector2(0, -0.3),
        "mass": 20,  # mass of the body
        "trail": [],
        "color": (255, 0, 0),
    },
    {
        "pos": math.Vector2(1.5 * WIDTH / 3, HEIGHT / 2),  # initial position
        "vel": math.Vector2(0, 0.3),
        "mass": 20,  # mass of the body
        "trail": [],
        "color": (0, 255, 0),
    }
]


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# GIF attempt
os.makedirs("frames", exist_ok=True)
frame_count = 1

# Main loop
running = True
while running:
    # Calculate time delta
    dt = clock.tick(FPS) / 5  # time since last frame in seconds
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user closed window
            running = False

        # Update each body
    for i in range(len(bodies)):
        body1 = bodies[i]
        for j in range(i + 1, len(bodies)):
            body2 = bodies[j]
            r = body2["pos"] - body1["pos"]  # vector from body1 to body2
            # calculate gravitational force and add it to the total force
            force = G * body1["mass"] * body2["mass"] / r.magnitude_squared() * r.normalize()
            # update velocities with the total force, taking into account time and mass
            body1["vel"] += force / body1["mass"] * dt * TIME_SPEED
            body2["vel"] -= force / body2["mass"] * dt * TIME_SPEED  # subtract because force is in opposite direction

    for body1 in bodies:
        body1["pos"] += body1["vel"] * dt * TIME_SPEED  # update positions


        # Update the trail
        body1["trail"].append(body1["pos"].copy())  # append a copy of the current position
        # keep only the last TRAIL_LENGTH positions
        body1["trail"] = body1["trail"][-TRAIL_LENGTH:]

    # Calculate the average position of all bodies to determine the camera position
    avg_pos = math.Vector2(
        sum(body["pos"].x for body in bodies) / len(bodies),
        sum(body["pos"].y for body in bodies) / len(bodies)
    )
    camera_pos = avg_pos - math.Vector2(WIDTH / 2, HEIGHT / 2)  # center the camera on the average position

    # Draw everything
    screen.fill((0, 0, 0))  # clear the screen
    for body in bodies:
        # Draw trail
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, [(int(pos.x - camera_pos.x), int(pos.y - camera_pos.y)) for pos in body["trail"]], 1)
        # Draw body
        pygame.draw.circle(screen, (255, 255, 255), (int(body["pos"].x - camera_pos.x), int(body["pos"].y - camera_pos.y)), 5)


        # # Saving every 3rd frame (to capture all 3 bodies) as a png for a video later on
        # if frame_count % 3 == 0:  # if the frame_count is a multiple of 3
        #     pygame.image.save(screen, f"frames/frame_{frame_count//3:05d}.png")
        # frame_count += 1

    # Flip the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()