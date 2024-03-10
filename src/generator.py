import subprocess


def executeVideo(input, output):

    ffmpeg = [
        'ffmpeg',
        '-i', input,
        output
    ]

    try:
        subprocess.run(ffmpeg, check=True)
        print('Suceeded')
    except subprocess.CalledProcessError as e:
        print("Failed")


executeVideo("test.mov", "output.mp3")
