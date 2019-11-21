import os
import cv2
import shutil
import imageio
import decimal
import pathlib
import numpy as np
from natsort import natsorted
import matplotlib.pyplot as plt

change = []
threshold = 0.1
videos = os.listdir('PATH TO VIDEOS DIRECTORY')
videos = natsorted(videos)
for video in videos:
    cap = cv2.VideoCapture('PATH TO VIDEOS DIRECTORY' + video)
    success = cap.read()
    currentFrame = 0
    os.makedirs('data_' + video)
    while success:
        # Capture frame-by-frame
        success, frame = cap.read()

        # Saves image of the current frame in jpg file
        name = './data_'+ video + '/' + video + '_' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        currentFrame += 1
    print("all frames created")
    os.remove('PATH TO data_ FOLDER' + video + '/' + video + '_' + str(currentFrame - 1) + '.jpg')


    #frame level computation
    rdiff = decimal.Decimal(0)
    gdiff = decimal.Decimal(0)
    bdiff = decimal.Decimal(0)
    n = 0

    frames = os.listdir('PATH TO data_ FOLDER' + video) #directory containing the frames of the video
    frames = natsorted(frames)  #sorting the files in order
    for frame in frames:
        file = pathlib.Path('PATH TO data_ FOLDER' + video + '/' + video + '_' + str(n + 1) + '.jpg')
        if file.exists():
            pic = imageio.imread('PATH TO data_ FOLDER' + video + '/' + video + '_' + str(n) + '.jpg')
            pic1 = imageio.imread('PATH TO data_ FOLDER' + video + '/' + video + '_' + str(n + 1) + '.jpg')
            height = int(format(pic.shape[0]))
            width = int(format(pic.shape[1]))
            tcount = height * width
            print('total number of pixels: ' + str(tcount))
            print('Computing Frames: ' + str(n) + ' and ' + str(n+1))

            #get diff of R, G and B channels:
            for i in range(pic.shape[0]):
                for j in range(pic.shape[1]):
                    #RGB values of fist frame:
                    R1 = int(format(pic[i,j,0]))
                    G1 = int(format(pic[i,j,1]))
                    B1 = int(format(pic[i,j,2]))


                    #RGB values of second frame:
                    R2 = int(format(pic1[i,j,0]))
                    G2 = int(format(pic1[i,j,1]))
                    B2 = int(format(pic1[i,j,2]))


                    rdiff += abs(R2 - R1) / decimal.Decimal('255')  #getting a decimal value between 0 and 1
                    gdiff += abs(G2 - G1) / decimal.Decimal('255')
                    bdiff += abs(B2 - B1) / decimal.Decimal('255')


            #average values of each channel:
            rdiff =  rdiff / decimal.Decimal(tcount)
            gdiff =  gdiff / decimal.Decimal(tcount)
            bdiff =  bdiff / decimal.Decimal(tcount)

            change.append(float(rdiff + gdiff + bdiff) / 3)
            n+= 1
            # print(change)
        else:
            print('reached the last frame')

    #grabbin frames which have more than the given threshold motion diff:
    #_MAIN_ALGORITHM_SPACE (UPDATE THIS):
    #you might have to create a folder named: "selected_frames"
    for i in range(len(change)):
        filename = 'PATH TO data_ FOLDER' + video + '/' + video + '_' + str(i) + '.jpg'
        if (change[i] >= threshold):
            shutil.move(filename , 'PATH TO selected_frames FOLDER')
        else:
            os.remove(filename)

    # shutil.rmtree('/Users/playment/Parth /Codes/data')



print('no more videos found')
print('\n')


#making the video from the selected frames:

image_folder = 'PATH TO selected_frames FOLDER'
video_name = 'OUTPUT FILE PATH'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
images = natsorted(images)
video = cv2.VideoWriter(video_name, 0, 25, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
