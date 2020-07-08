# Python program using OpenCV and CNN for video trimming using signs
# CNN model trained to exactly predict 2 classes - Up or Down

# Import necessary libraries
import numpy as np
import cv2
import time
import tensorflow.keras
from keras.preprocessing import image

# Access WebCam
cap = cv2.VideoCapture(0)
state = True

# Load the TensorFlow CNN model weights
model = tensorflow.keras.models.load_model('keras_model.h5')

# Set the width and height of the frame for video to be saved
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a writer object to save the frames
writer = cv2.VideoWriter(r'C:\Users\Sharan Babu\Desktop\trimm_video.mp4', cv2.VideoWriter_fourcc(*'XVID'),25, (width, height))
save = []

while True:
	success, image = cap.read()

	if success==True:
		save.append(image)
		img = image.copy()
		# Draw a rectangle to indicate the region of interest
		cv2.rectangle(img,pt1=(450,100),pt2=(620,300),color=(0,255,0),thickness=3)
		cv2.imshow("Video",img)
		roi = img[102:298,448:618]
		
		# Image pre-processing for making predictions of the image
		data = cv2.resize(roi,(224,224))
		data = np.array(data,dtype=np.float32)
		data = np.expand_dims(data,axis=0)
		data = data/255

		# Predict output class for the image
		prediction = model.predict(data) # Start,End
		start,end = prediction[0][0],prediction[0][1]
		
        # Save frames to the output video file according to sign
		if end>0.7:  
		    prediction='end' 
		    save = []
		    print('end')
		if end<0.0005:
		    prediction='start'
		    for i in save:
		    	writer.write(i)
		    save = []	
		    print('start')

    # Break the program
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break	   

# Close webcam and other connections
writer.release()
cap.release()
cv2.destroyAllWindows()