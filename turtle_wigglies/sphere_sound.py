import turtle
import math
import pyaudio
import numpy as np
import argparse

# Set up the screen
screen = turtle.Screen()
screen.title("Sound Reactive Sun")
screen.bgcolor("black")
screen.setup(width=800, height=400)

# Create a turtle for drawing the sun
sun_turtle = turtle.Turtle()
sun_turtle.speed(0)  # Fastest drawing speed
sun_turtle.hideturtle()  # Hide the turtle

# Function to draw the sun shape
def draw_sun(amplitude):
    # Clear previous drawing
    sun_turtle.clear()
    
    # Center position
    sun_turtle.penup()
    sun_turtle.goto(0, -amplitude)  # Start at the bottom of the circle
    sun_turtle.pendown()
    
    # Draw the sun (central circle)
    sun_turtle.color("yellow")
    sun_turtle.begin_fill()
    sun_turtle.circle(amplitude)  # Draw the circle with radius = amplitude
    sun_turtle.end_fill()
    
    # Draw rings around the sun
    num_rings = 5  # Number of rings
    for i in range(num_rings):
        sun_turtle.penup()
        radius = amplitude * (1.2 + i * 0.3)  # Adjust size of rings based on amplitude
        sun_turtle.goto(0, -radius)  # Move to the bottom of the ring
        sun_turtle.pendown()
        sun_turtle.color("orange")
        sun_turtle.circle(radius, 360)  # Draw a full circle for the ring

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
previous_amplitude = 0  # For smoothing

# Main loop
running = True
while running:
    # Get the current volume level
    volume = get_volume(args.input_device_index)

    # Normalize volume to amplitude
    sensitivity = 50  # Adjust this value as needed
    amplitude = max((volume / 32768) * max_amplitude * sensitivity, min_amplitude)  # Ensure amplitude is not less than min_amplitude

    # Smoothing with linear interpolation
    alpha = 0.1
    amplitude = (1 - alpha) * previous_amplitude + alpha * amplitude
    previous_amplitude = amplitude

    # Draw the sun shape
    draw_sun(amplitude)

    # Update the screen
    screen.update()

# Close the turtle graphics window
turtle.done()
