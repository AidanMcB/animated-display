import pygame
import math
import pyaudio
import numpy as np
import argparse

# Initialize Pygame
pygame.init()

# Used for smoothing
previous_amplitude = 0

# Set up screen dimensions
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up colors
black = (0, 0, 0)
sun_color = (255, 255, 0)  # Yellow for the sun
ring_color = (255, 165, 0)  # Orange for the rings

# Function to draw sun shape with rings
def draw_sun(screen, amplitude):
    # Clear the screen
    screen.fill(black)

    # Center of the screen
    center_x, center_y = screen_width // 2, screen_height // 2

    # Draw the sun (central circle)
    pygame.draw.circle(screen, sun_color, (center_x, center_y), int(amplitude))

    # Draw rings around the sun
    num_rings = 5  # Number of rings
    for i in range(num_rings):
        radius = int(amplitude * (1.2 + i * 0.3))  # Adjust size of rings based on amplitude
        pygame.draw.circle(screen, ring_color, (center_x, center_y), radius, 2)  # Draw ring with thickness 2

# Function to get the average volume from the microphone
def get_volume(input_device_index):
    CHUNK = 1024  # Number of audio samples per frame
    RATE = 44100  # Sampling rate in Hz

    # Open the stream
    p = pyaudio.PyAudio()
    try:
        # Specify index of sound input
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=input_device_index)

        # Read data from the stream
        data = stream.read(CHUNK)
        # Convert the data to an array of integers
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Calculate the average volume
        volume = np.abs(audio_data).mean()

    except Exception as e:
        print("Error accessing microphone:", e)
        volume = 0  # Set volume to zero on error

    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

    return volume

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Visualize sound wave as a sun shape.")
parser.add_argument('--input_device_index', type=int, default=1, help="Index of the audio input device (default is 1).")
args = parser.parse_args()

# Main loop variables
max_amplitude = 100  # Maximum amplitude of the sun
min_amplitude = 20   # Minimum amplitude to ensure the sun is always visible
frequency = 0.05  # Frequency of the wave (not used here)
offset = 0  # Horizontal offset to make the wave move (not used here)
speed = 2  # Speed at which the wave moves (not used here)

# Main loop
running = True
last_time = pygame.time.get_ticks()
while running:
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current volume level
    volume = get_volume(args.input_device_index)

    # Normalize volume to amplitude (adjust this as needed)
    sensitivity = 50  # Adjust this value as needed
    amplitude = max((volume / 32768) * max_amplitude * sensitivity, min_amplitude)  # Ensure amplitude is not less than min_amplitude

    # Smoothing with linear interpolation
    alpha = 0.1
    amplitude = (1 - alpha) * previous_amplitude + alpha * amplitude
    previous_amplitude = amplitude

    # Draw the sun shape
    draw_sun(screen, amplitude)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
