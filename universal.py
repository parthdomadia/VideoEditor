import os
from typing import Any, Union
import cv2
import shutil
import imageio
import decimal
import pathlib
import numpy as np
from natsort import natsorted

# declare global variables
key_frames = []
threshold = 0.1
video_path = 'sample_videos'
data_path = 'data'


def split(video):
    cap = cv2.VideoCapture(video_path + '/' + video)
    success, frame = cap.read()
    currentFrame = 0
    while success:
        # capture frames one by one
        success, frame = cap.read()

        if success is True:
            # save image of the current frame in jpg format

            name = 'data' + '/' + str(currentFrame) + '.jpg'
            print('Creating...' + name, success)
            cv2.imwrite(name, frame)
        currentFrame += 1

    print('All frames created')
    # os.remove('/Users/playment/PycharmProjects/data' + '/' + str(currentFrame - 1) + '.jpg')


def compute():
    # pixel level computation

    rdiff = decimal.Decimal(0)
    gdiff = decimal.Decimal(0)
    bdiff = decimal.Decimal(0)
    n = 0
    x = 1

    frames = os.listdir(data_path)  # directory containing the frames of the video
    frames = natsorted(frames)  # sorting the files in order
    for frame in frames:
        file = pathlib.Path('data' + '/' + str(x) + '.jpg')
        if file.exists():
            pic = imageio.imread('data' + '/' + str(n) + '.jpg')
            pic1 = imageio.imread('data' + '/' + str(x) + '.jpg')
            height = int(format(pic.shape[0]))
            width = int(format(pic.shape[1]))
            tcount = height * width
            print('total number of pixels: ' + str(tcount))
            print('Computing Frames: ' + str(n) + ' and ' + str(x))

            # get diff of R, G and B channels:
            # pixel level computation
            for i in range(pic.shape[0]):
                for j in range(pic.shape[1]):
                    # RGB values of fist frame:
                    R1 = int(format(pic[i, j, 0]))
                    G1 = int(format(pic[i, j, 1]))
                    B1 = int(format(pic[i, j, 2]))

                    # RGB values of second frame:
                    R2 = int(format(pic1[i, j, 0]))
                    G2 = int(format(pic1[i, j, 1]))
                    B2 = int(format(pic1[i, j, 2]))

                    rdiff += abs(R2 - R1) / decimal.Decimal('255')  # getting a decimal value between 0 and 1
                    gdiff += abs(G2 - G1) / decimal.Decimal('255')
                    bdiff += abs(B2 - B1) / decimal.Decimal('255')

            # average values of each channel:
            rdiff = rdiff / decimal.Decimal(tcount)
            gdiff = gdiff / decimal.Decimal(tcount)
            bdiff = bdiff / decimal.Decimal(tcount)

            difference = float(rdiff + gdiff + bdiff) / 3

            if (difference >= threshold):
                key_frames.append(str(x))
                n = x
            x += 1

    print('Computation completed , yaaaaaaaaaaaaaaaaaaaaaaaay')


def make_cut():
    # make cuts from selected frames
    # MAKE CHANGES ACCORDING TO THE NEW compute() FUNCTION

    global q, p
    for i in range(len(key_frames)):
        # print(change[i])
        print('Key frame observed is : ' + key_frames[i])
        # actual algorithm:
        number = random.randrange(20, 50)
        number1 = random.randrange(20, 50)

        # taking frames which lie before the chosen frame
        for j in range(number):
            if os.path.exists('data' + '/' + str(key_frames[i] - j + 1) + '.jpg'):
                if os.path.exists(
                        'selected_frames' + video + '/' + str(key_frames[i] - j + 1) + '.jpg'):
                    continue
                else:
                    shutil.copy('data' + '/' + str(key_frames[i] - j + 1) + '.jpg',
                                'selected_frames' + str(key_frames[i] - j + 1) + '.jpg')
                    p += 1
            else:
                continue

        # taking frames which lie after the chosen frame
        for j in range(number):
            if os.path.exists('data' + '/' + str(key_frames[i] + j + 1) + '.jpg'):
                if os.path.exists('selected_frames' + str(key_frames[i] + j + 1) + '.jpg'):
                    continue
                else:
                    shutil.copy('data' + '/' + str(key_frames[i] + j + 1) + '.jpg',
                                'selected_frames' + str(key_frames[i] + j + 1) + '.jpg')
                    q += 1
            else:
                continue
                
    # extra info to show
    t_frames_moved = (p + q)
    frames_removed = ((t_frames - t_frames_moved) / t_frames) * 100
    print('clip removed: ' + str(frames_removed) + '%')


def create():
    # join frames to make video

    image_folder = 'selected_frames'
    video_name = 'output/OUT.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    images = natsorted(images)
    video = cv2.VideoWriter(video_name, 0, 25, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    print('Video is created')


def initiate():
    # main function
    videos = os.listdir(video_path)
    videos = natsorted(videos)
 
    for video in videos:
        split(video)
        compute()
        make_cut()
    print('No more videos found')

    # calling function to create video
    create()


if __name__ == "__main__":
    print("STARTING ENGINES")
    initiate()
