# Convolutional Neural Network version 0.0.2_keras
# Author: Joshua Stauffer
# Created: 2/6/2019
# Modified: 2/11/2019
# Summary: Upgrade version with keras implementation
# -----------------------------------------------------------------------------------BoF
# Initializing
import tensorflow as tf
import numpy as np
import os
import cv2	#pip install opencv-python
import random
import pickle

# ------------------------------------------------------------------Data set creation
DATADIR = "D:\\Josh Stauffer\\Documents\\Senior Design\\Cancer Detection Code\\Patches"
CATEGORIES = ["Negative", "Positive"]
training_data = [] #Training pairs
IMG_SIZE = 64
X = []	#Features
y = []	#Labels

def create_training_data():
	
	for category in CATEGORIES:
		numOfCases = 37200					# how much data to use from each category
		print("Reading Categories " + category)
		path = os.path.join(DATADIR, category)
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			print("On img " + img)
			img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
			new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
			training_data.append([new_array, class_num])
			if numOfCases == 1:
				break
			numOfCases -= 1
			
		
create_training_data()
print("Length of training_data created is " + repr(len(training_data)))
random.shuffle(training_data)

for features, label in training_data:
	X.append(features)
	y.append(label)
	
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
print("Saving")

#Save features
pickle_out = open("X.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

#Save Labels
pickle_out = open("y.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()

print("Saving Complete")
input('Press ENTER to exit')
#To open later: X = pickle.load(open("X.pickle","rb")) \n
# -----------------------------------------------------------------------------------EoF