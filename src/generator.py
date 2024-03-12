import subprocess
import os
import time
import shutil
from moviepy.editor import VideoFileClip
import sys


def appendZero(i, length):

    string = str(i)
    while len(string) < length:
        string = "0" + string
    return string


def convert(string, length, increment, offset):

    originalVal = int(string)
    newVal = (originalVal * increment)
    return appendZero(newVal + offset, length)


def rename(directory, name, zLoc, increment, type):

    offset = 0
    if type == 'o':
        offset = -1
    directory = directory + "/"
    filenames = sorted(os.listdir(directory))
    filenames.pop(0)
    for filename in filenames:
        try:
            print("current file name: " + filename)
            updatedFileName = name + "_" + \
                convert(filename[zLoc:zLoc + 6], 6, increment, offset) + ".png"
            os.rename(directory + filename, directory + updatedFileName)
        except:
            print("invalid file")


def generateVidFrames(input, frameRate):

    input = "input/" + input
    ffmpeg = [
        'ffmpeg',
        '-i', input,
        "-vf",
        f'fps={frameRate // 2}',
        "vidFrames/frame_%06d.png"
    ]
    try:
        subprocess.run(ffmpeg, check=True)
        print('Suceeded')
    except subprocess.CalledProcessError as e:
        print("Failed")


def generateBlackFrames(h, w, num):

    ffmpeg = [
        "ffmpeg",
        '-f',
        'lavfi',
        '-i',
        'color=c=black:s=' + str(h) + 'x' + str(w),
        '-vframes', str(num // 2),
        "blackFrames/blackframe_%06d.png"
    ]
    try:
        subprocess.run(ffmpeg, check=True)
        print('Suceeded')
    except subprocess.CalledProcessError as e:
        print("Failed")


def moveAllFiles():

    sources = ["vidFrames/", "blackFrames/"]
    outLocation = "allFrames/"
    for source in sources:
        for filename in os.listdir(source):
            try:
                if 'n' == filename[0]:
                    shutil.move(source + filename, outLocation)
            except:
                print('operation is invalid')


def compileVideo(frameRate, output):

    ffmpeg = [
        "ffmpeg",
        "-framerate", f"{frameRate}",
        "-i", "allFrames/nframes_%06d.png",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        f"output/{output}"
    ]
    try:
        subprocess.run(ffmpeg, check=True)
        print('Suceeded')
    except subprocess.CalledProcessError as e:
        print("Failed")


def resetFolders():

    folder_path = 'allFrames'
    if os.path.exists(folder_path):
        print("path exists")
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    else:
        print(f"The folder {folder_path} does not exist.")


def findDuration(inputName):

    video_path = f'input/{inputName}'
    clip = VideoFileClip(video_path)
    return clip.duration


def findFrameRate(outputName):

    video_path = f'output/{outputName}'
    clip = VideoFileClip(video_path)
    print(f'Frame Rate: {clip.fps}')


def getHeight(inputName):

    video_path = f'input/{inputName}'
    video_clip = VideoFileClip(video_path)
    height = video_clip.h
    video_clip.close()
    return height


def getWidth(inputName):

    video_path = f'input/{inputName}'
    video_clip = VideoFileClip(video_path)
    width = video_clip.w
    video_clip.close()
    return width


def main():

    print(sys.argv)
    # or (not len(sys.argv) == 3) or (not len(sys.argv) == 4)

    if int(sys.argv[2]) < 1:
        print("Invalid args")
    else:

        inputName = "input.mov"
        frameRate = 60
        outputName = "output.mov"

        inputName = sys.argv[1]
        frameRate = int(sys.argv[2])

        if len(sys.argv) == 4:
            outputName = sys.argv[3]

        start_time = time.perf_counter()
        print(getHeight(inputName), getWidth(inputName))
        generateBlackFrames(getWidth(inputName), getHeight(inputName),
                            findDuration(inputName) * frameRate)
        time.sleep(2)
        rename("blackFrames", "nframes", 11, 2, "o")
        generateVidFrames(inputName, frameRate)
        time.sleep(2)
        rename("vidFrames", "nframes", 6, 2, "e")
        time.sleep(1)
        moveAllFiles()
        time.sleep(1)
        compileVideo(frameRate, outputName)
        resetFolders()
        findFrameRate(outputName)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Program took {total_time} seconds to run.")


if __name__ == "__main__":
    main()
