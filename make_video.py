import cv2
import os
from natsort import natsorted

image_folder = '/Users/playment/Parth /Codes/data'
video_name = '/Users/playment/Parth /Codes/AI_VideoEditing/video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
images = natsorted(images)
video = cv2.VideoWriter(video_name, 0, 60, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
