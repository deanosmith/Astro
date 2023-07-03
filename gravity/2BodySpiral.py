import pygame
import pygame.math as math

# Constants for our simulation
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second - this determines the "speed" of our simulation
G = 1  # Gravitational constant for our simulation
TRAIL_LENGTH = 1000  # Length of the trail
TIME_SPEED = 20  # Increase the flow of time

# Body properties (position, velocity)
bodies = [
    {
        "pos": math.Vector2(WIDTH / 3, HEIGHT / 2),  # initial position
        "vel": math.Vector2(0, -0.06),  # initial velocity
        "trail": [],  # list to store trail positions
        "color": (255, 0, 0)  # color of the trail
    },
    {
        "pos": math.Vector2(1.5 * WIDTH / 3, HEIGHT / 2),  # initial position
        "vel": math.Vector2(0, 0.05),  # initial velocity
        "trail": [],  # list to store trail positions
        "color": (0, 255, 0)  # color of the trail
    }
]

# Initialize Pygame
pygame.init()
# Create a window of size WIDTH x HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Create a Pygame clock object to control the frame rate
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
        force = math.Vector2(0, 0)  # initialize force as 0
        for body2 in bodies:
            if body1 != body2:
                r = body2["pos"] - body1["pos"]  # vector from body1 to body2
                # calculate gravitational force and add it to the total force
                force += G / r.magnitude_squared() * r.normalize()  
        # update velocity and position with the total force, scaled by TIME_SPEED
        body1["vel"] += force * TIME_SPEED
        body1["pos"] += body1["vel"] * TIME_SPEED

        # Update the trail
        body1["trail"].append((int(body1["pos"].x), int(body1["pos"].y)))
        # keep only the last TRAIL_LENGTH positions
        body1["trail"] = body1["trail"][-TRAIL_LENGTH:]  

    # Draw everything
    screen.fill((0, 0, 0))  # clear the screen
    for body in bodies:
        # Draw trail
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, body["trail"], 1)
        # Draw body
        pygame.draw.circle(screen, (255, 255, 255), (int(body["pos"].x), int(body["pos"].y)), 5)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
