import os
import pygame
import pygame.math as math

# Constants for our simulation
# Window size
WIDTH, HEIGHT = 1000, 500
# Frames per second - this determines the "speed" of our simulation
FPS = 120
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
        "pos": math.Vector2(WIDTH / 3, HEIGHT / 2),
        # "pos": math.Vector2(1500, 800),
        "vel": math.Vector2(0, -0.3),
        "mass": 20,  # mass of the body
        "trail": [],
        "color": (255, 0, 0),
        "collided": False  # flag to check if this body has collided
    }
    ,{
        "pos": math.Vector2(WIDTH / 3 + 100, HEIGHT / 2),
        # "pos": math.Vector2(1700, 600),
        "vel": math.Vector2(0, 0.3),
        "mass": 20,  # mass of the body
        "trail": [],
        "color": (0, 255, 0),
        "collided": False  # flag to check if this body has collided
    }
    # ,{
    #     # "pos": math.Vector2(1.5 * WIDTH / 3, HEIGHT / 2),
    #     "pos": math.Vector2(350, 200),
    #     "vel": math.Vector2(0, 0.12),
    #     "mass": 2,  # mass of the body
    #     "trail": [],
    #     "color": (0, 0, 255),
    #     "collided": False  # flag to check if this body has collided
    # }
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update each body
    for body1 in bodies:
        if not body1["collided"]:  # If the body has not collided
            force = math.Vector2(0, 0)
            for body2 in bodies:
                if body1 != body2:
                    r = body2["pos"] - body1["pos"]
                    force += G * body1["mass"] * body2["mass"] / r.magnitude_squared() * r.normalize()

                    # Check for collision
                    # if r.length() <= 2 * BODY_RADIUS:
                    #     body1["collided"] = True
                    #     body2["collided"] = True

            body1["vel"] += force * TIME_SPEED / body1["mass"]
            body1["pos"] += body1["vel"] * TIME_SPEED

            body1["trail"].append((int(body1["pos"].x), int(body1["pos"].y)))
            body1["trail"] = body1["trail"][-TRAIL_LENGTH:]

    # Draw everything
    screen.fill((0, 0, 0))
    for body in bodies:
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, body["trail"], 1)
        pygame.draw.circle(screen, (255, 255, 255), (int(body["pos"].x), int(body["pos"].y)), BODY_RADIUS)

        # Saving every 3rd frame (to capture all 3 bodies) as a png for a video later on
        # if frame_count % 3 == 0:  # if the frame_count is a multiple of 3
        #     pygame.image.save(screen, f"frames/frame_{frame_count//3:05d}.png")
        # frame_count += 1

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
