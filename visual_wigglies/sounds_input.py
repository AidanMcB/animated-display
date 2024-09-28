import pygame
import math
import pyaudio
import numpy as np
import argparse

###### About ########
#####################
#####################
#
#
# By default, this runs using audio input 1.
# To specify a different audio device, add as an argument:
#       `python your_script.py --input_device_index 2`
#
#####################
#####################
#####################

# Initialize Pygame
pygame.init()

# Used for smoothing
previous_amplitude = 0

# Set up screen dimensions
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up colors
black = (0, 0, 0)
line_color = (0, 255, 0)

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
parser = argparse.ArgumentParser(description="Visualize sound wave from microphone.")
parser.add_argument('--input_device_index', type=int, default=1, help="Index of the audio input device (default is 1).")
args = parser.parse_args()

# Main loop variables
max_amplitude = 100  # Maximum amplitude of the wave
frequency = 0.05  # Frequency of the wave
offset = 0  # Horizontal offset to make the wave move
speed = 2  # Speed at which the wave moves

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
    amplitude = (volume / 32768) * max_amplitude * sensitivity

    # Smoothing with linear interpolation
    alpha = 0.1
    amplitude = (1 - alpha) * previous_amplitude + alpha * amplitude
    previous_amplitude = amplitude

    # Draw the wave
    draw_wave(screen, amplitude, frequency, offset)

    # Update the display
    pygame.display.flip()

    # Update the wave's offset to simulate movement
    offset += speed * delta_time * 100  # Speed multiplied by delta_time

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
