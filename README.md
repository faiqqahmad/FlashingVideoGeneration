#### FlashingVideoGeneration

## Purpose

This script is designed to add a flickering effect to videos for the purpose of Brain-Computer-Interface research.

## Dependencies

# ffmpeg:

    Homebrew installation

    $ brew install ffmpeg

# moviepy:

    $ pip install moviepy

## Running Generator

1. Place relevant video file in the input folder.
2. Navigate to the src folder.
3. Run

   python3 generator.py [FULL NAME OF VIDEO FILE INCLUDING FORMAT] [FRAMERATE VALUE AS AN INT] [OUTPUT FILE NAME (is optional)]

   ex. python3 generator.py input_movie.mp4 60 output.mov
   ex. python3 generator.py input_movie.mp4 60

4. The finished video will be in the output folder.
