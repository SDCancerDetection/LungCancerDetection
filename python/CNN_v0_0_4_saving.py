# Convolutional Neural Network version 0.0.4_saving
# Author: Joshua Stauffer
# Created: 2/11/2019
# Modified: 2/26/2019
# Summary: Added TensorBoard monitoring and early_stopping
# -----------------------------------------------------------------------------------BoF
# Initializing
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping
import pickle
import time

#Recorded log name
NAME = "CT-Patches-cnn-64x2-{}".format(int(time.time()))
#SavedModel Dir
MODELDIR = 'D:\\Josh Stauffer\\Documents\\Senior Design\\Cancer Detection Code\\models\\savedModels\\' + NAME

#Log callbacks
tensorboard = TensorBoard(log_dir = 'logs/{}'.format(NAME))
early_stopping = EarlyStopping(monitor = 'val_loss', patience = 2)

# ------------------------------------------------------------------Data loading
X = pickle.load(open("X.pickle","rb"))
y = pickle.load(open("y.pickle","rb"))

#Normalizing
X = X/255.0

#Model infrastructure
model = Sequential()
with tf.device('/device:GPU:0'):
	model.add(    Conv2D(64, (4,4), input_shape = X.shape[1:])    )
	model.add(Activation("relu"))
	model.add(    MaxPooling2D(pool_size = (2,2))    )

	model.add(    Conv2D(64, (4,4))    )
	model.add(Activation("relu"))
	model.add(    MaxPooling2D(pool_size = (2,2))    )

	model.add(Flatten())
	
	model.add(Dense(64))
	model.add(Activation("relu"))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(loss = "binary_crossentropy",
				optimizer = "adam",
				metrics = ['accuracy'])
			
	model.fit(X, y, batch_size = 64, epochs = 10, validation_split = 0.2,
	callbacks = [tensorboard, early_stopping], shuffle = True)
	
#Saving Model
model.save(MODELDIR)
#To load model, keras.models.load_model(filepath)
print("Saving Complete")
input('Press ENTER to exit')
# -----------------------------------------------------------------------------------EoF