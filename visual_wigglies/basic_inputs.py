import pygame
import math

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up colors
black = (0, 0, 0)
line_color = (0, 255, 0) # green

# Function to draw wave
def draw_wave(screen, amplitude, frequency, offset):
    # Clear the screen
    screen.fill(black)
    
    # Define points for the wave
    points = []
    for x in range(screen_width):
        y = screen_height // 2 + int(amplitude * math.sin(frequency * (x + offset)))
        points.append((x, y))

    # Draw the wave as a line connecting the points
    pygame.draw.lines(screen, line_color, False, points, 2)

# Main loop variables
amplitude = 50  # Initial amplitude of the wave (height of peaks/valleys)
frequency = 0.05  # Frequency of the wave (how many peaks/valleys)
offset = 0  # Horizontal offset to make the wave move
speed = 2  # Speed at which the wave moves

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # Increase amplitude
                amplitude += 10  # Increase wave height
                if amplitude > screen_height // 2:  # Limit the max amplitude
                    amplitude = screen_height // 2
            elif event.key == pygame.K_d:  # Decrease amplitude
                amplitude -= 10  # Decrease wave height
                if amplitude < 0:  # Limit the min amplitude
                    amplitude = 0

    # Draw the wave
    draw_wave(screen, amplitude, frequency, offset)

    # Update the display
    pygame.display.flip()

    # Update the wave's offset to simulate movement
    offset += speed

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
