import subprocess
import os
import time
import shutil


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


def generateVidFrames(input):

    input = "input/" + input

    ffmpeg = [
        'ffmpeg',
        '-i', input,
        "-vf",
        'fps=12',
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
        '-vframes', str(num),
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


generateBlackFrames(1640, 1624, 30)

time.sleep(2)

rename("blackFrames", "nframes", 11, 2, "o")

generateVidFrames("input_video.mp4")

time.sleep(2)

rename("vidFrames", "nframes", 6, 2, "e")

time.sleep(1)

moveAllFiles()


# rename("vidFrames", "nframe", 6, 2)
