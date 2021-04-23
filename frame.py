import cv2
import os, shutil

rootdir = 'walk'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        vidcap = cv2.VideoCapture(os.path.join(subdir, file))
        success,image = vidcap.read()
        count = 0
        directory = "images\\" + subdir[12:] + "\\" + str(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        while success:
            cv2.imwrite(directory + "\\%d.jpg" % count, image)     # save frame as JPEG file      
            success,image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1