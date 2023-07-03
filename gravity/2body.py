import pygame
import pygame.math as math

# Constants for our simulation
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second - this determines the "speed" of our simulation
G = 1  # Gravitational constant for our simulation
TRAIL_LENGTH = 1000  # Length of the trail
TIME_SPEED = 20  # Increase the flow of time
BODY_RADIUS = 5  # Radius of the bodies (used for collision detection)

# Body properties (position, velocity, mass)
bodies = [
    {
        # "pos": math.Vector2(WIDTH / 3, HEIGHT / 2),
        "pos": math.Vector2(267, 300),
        "vel": math.Vector2(0, -0.06),
        "mass": 1,  # mass of the body
        "trail": [],
        "color": (255, 0, 0),
        "collided": False  # flag to check if this body has collided
    },
    {
        # "pos": math.Vector2(1.5 * WIDTH / 3, HEIGHT / 2),
        "pos": math.Vector2(400, 300),
        "vel": math.Vector2(0, 0.05),
        "mass": 1,  # mass of the body
        "trail": [],
        "color": (0, 255, 0),
        "collided": False  # flag to check if this body has collided
    }
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
