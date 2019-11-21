# VideoEditor
AI assisted video editor based on motion difference between the frames of given videos 


All the differnet modules of the main code are also uploaded from which I build the main code.



 -- Download the universal file onto to you computer and install the neccessary libraries as mentioned in the code itself. 



What the code basically does, flow of data 
Pointers: 
- takes video input 
- splits into frames
- does frame level computation and give pixel diff 
- chooses which frames to be selected based on user input for `threshold`
- joins the selected frames to make a video 
- no sound, add external sound source later
