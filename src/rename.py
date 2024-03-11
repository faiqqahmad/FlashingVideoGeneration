import os

sourceDirectory = "vidFrames/"
increment = 1
filenames = sorted(os.listdir(sourceDirectory))


def convert(string, length):
    originalVal = int(string)
    newVal = originalVal * 2
    nvString = str(newVal)
    while len(nvString) < length:
        nvString = "0" + nvString
    return nvString


for filename in filenames:
    try:
        updatedFileName = "nframe_" + convert(filename[6:12], 6) + ".png"
        os.rename("vidFrames/" + filename, "vidFrames/" + updatedFileName)
    except:
        print("invalid file")
