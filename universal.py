import os
import cv2
import shutil
import imageio
import decimal
import pathlib
import random
import numpy as np
from natsort import natsorted
import matplotlib.pyplot as plt
p=0
q=0

change = []
threshold = 0.1
videos = os.listdir('sample_videos')
videos = natsorted(videos)
for video in videos:
    cap = cv2.VideoCapture('sample_videos/' + video)
    success = cap.read()
    currentFrame = 0
    os.makedirs('data')
    while success:
        # Capture frame-by-frame
        success, frame = cap.read()

        # Saves image of the current frame in jpg file
        name = './data/'+ str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        currentFrame += 1
    print("all frames created")
    os.remove('data/'+ str(currentFrame - 1)+'.jpg')
    t_frames = (currentFrame - 2)


    #frame level computation
    rdiff = decimal.Decimal(0)
    gdiff = decimal.Decimal(0)
    bdiff = decimal.Decimal(0)
    n = 0

    frames = os.listdir('data') #directory containing the frames of the video
    frames = natsorted(frames)  #sorting the files in order
    for frame in frames:
        file = pathlib.Path('data/'+str(n + 1)+'.jpg')
        if file.exists():
            pic = imageio.imread('data/'+str(n)+'.jpg')
            pic1 = imageio.imread('data/'+str(n + 1)+'.jpg')
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
            #print(change)
        else:
            print('reached the last frame')
 
for i in range(len(change)):
    if (change[i] >= threshold):
        print(change[i])
        print('the change is observed between frame ' + str(i) + ' and frame ' + str(i+1))
        #actual algotithm:
        number = random.randrange(20,50)
        number1 = random.randrange(20,50)
        #taking frames which lie before the chosen frame
        for j in range(number):
            if os.path.exists('data/'+str(i-j+1)+'.jpg'):
                if os.path.exists('selected_frames/'+str(i-j+1)+'.jpg'):
                    continue
                else:
                    shutil.copy('data/'+str(i-j+1)+'.jpg','selected_frames/'+str(i-j+1)+'.jpg')
                    p+=1
            else:
                continue
        
        #taking frames which lie after the chosen frame        
        for j in range(number):
            if os.path.exists('data/'+str(i+j+1)+'.jpg'):
                if os.path.exists('selected_frames/'+str(i+j+1)+'.jpg'):
                    continue
                else:
                    shutil.copy('data/'+str(i+j+1)+'.jpg','selected_frames/'+str(i+j+1)+'.jpg')
                    q+=1
            else:
                continue        
shutil.rmtree('data')
#extra info to show 
t_frames_moved = (p + q)
frames_removed = ((t_frames - t_frames_moved)/t_frames)*100
print('clip removed: ' + str(frames_removed)+'%')   

#see the frames which are selected
s_frames = os.listdir('selected_frames')
s_frames = natsorted(s_frames)
for x in range(len(s_frames)):
    print(s_frames[x])

    
#making the video from the selected frames:
image_folder = 'selected_frames'
video_name = 'output/OUT.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
images = natsorted(images)
video = cv2.VideoWriter(video_name, 0, 25, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
