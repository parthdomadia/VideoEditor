import cv2
import numpy as np
import os

# Playing video from file:
cap = cv2.VideoCapture('/Users/playment/Parth /Codes/AI_VideoEditing/Sample_videos/sample.mp4')
success = cap.read()
try:
    if not os.path.exists('data1'):
        os.makedirs('data1')
except OSError:
    print ('Error: Creating directory of data1')

currentFrame = 0
while success:
    # Capture frame-by-frame
    success, frame = cap.read()

    # Saves image of the current frame in jpg file
    name = './data1/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
