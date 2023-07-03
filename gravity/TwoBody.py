import pygame
import pygame.math as math

# Constants for our simulation
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 120  # Frames per second - this determines the "speed" of our simulation
G = 1  # Gravitational constant for our simulation
TRAIL_LENGTH = 50  # Length of the trail

# Body properties (position, velocity)
bodies = [
    {
        "pos": math.Vector2(WIDTH / 3, HEIGHT / 2),
        # SPEED SEEMS TO BE EVERYTHING (OBVIOSULY)
        "vel": math.Vector2(0, -0.05),
        "trail": [],
        "color": (255, 0, 0)
    },
    {
        "pos": math.Vector2(1.5 * WIDTH / 3, HEIGHT / 2),
        "vel": math.Vector2(0, 0.05),
        "trail": [],
        "color": (0, 255, 0)
    }
]

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user closed window
            running = False

    # Update each body
    for body1 in bodies:
        force = math.Vector2(0, 0)
        for body2 in bodies:
            if body1 != body2:
                r = body2["pos"] - body1["pos"]  # vector from body1 to body2
                force += G / r.magnitude_squared() * r.normalize()  # gravitational force
        body1["vel"] += force  # body is pulled towards other bodies
        body1["pos"] += body1["vel"]

        # Update the trail
        # body1["trail"].append(body1["pos"])
        # body1["trail"] = body1["trail"][-TRAIL_LENGTH:]  # keep only the last TRAIL_LENGTH positions

        body1["trail"].append([int(body1["p"][0]), int(body1["p"][1])])
        body1["trail"] = body1["trail"]#[-500:]

    # Draw everything
    screen.fill((0, 0, 0))  # clear the screen
    for body in bodies:
        # Draw trail
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, [(int(pos.x), int(pos.y)) for pos in body["trail"]], 1)
        # Draw body
        pygame.draw.circle(screen, (255, 255, 255), (int(body["pos"].x), int(body["pos"].y)), 5)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
