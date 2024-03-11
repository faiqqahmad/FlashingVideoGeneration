import subprocess
import os
import time
import shutil
from moviepy.editor import VideoFileClip

inputName = "input_video.mp4"
frameRate = 60


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


def compileVideo():

    ffmpeg = [
        "ffmpeg",
        "-framerate", f"{frameRate}",
        "-i", "allFrames/nframes_%06d.png",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "output/output_video.mp4"
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


def findDuration():

    video_path = f'input/{inputName}'
    clip = VideoFileClip(video_path)
    return clip.duration


def findFrameRate():

    video_path = f'output/output_video.mp4'
    clip = VideoFileClip(video_path)
    print(f'Frame Rate: {clip.fps}')


def getHeight():

    video_path = f'input/{inputName}'
    video_clip = VideoFileClip(video_path)
    height = video_clip.h  # Height of the video
    video_clip.close()
    return height


def getWidth():

    video_path = f'input/{inputName}'
    video_clip = VideoFileClip(video_path)
    width = video_clip.w  # Height of the video
    video_clip.close()
    return width


generateBlackFrames(getHeight(), getWidth(), findDuration() * frameRate)
time.sleep(2)
rename("blackFrames", "nframes", 11, 2, "o")
generateVidFrames("input_video.mp4")
time.sleep(2)
rename("vidFrames", "nframes", 6, 2, "e")
time.sleep(1)
moveAllFiles()
time.sleep(1)
compileVideo()
resetFolders()
findFrameRate()
