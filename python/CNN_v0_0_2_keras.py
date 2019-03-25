# Convolutional Neural Network version 0.0.2_keras
# Author: Joshua Stauffer
# Created: 2/11/2019
# Modified: 2/11/2019
# Summary: Upgrade version with keras implementation
# -----------------------------------------------------------------------------------BoF
# Initializing
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle

# ------------------------------------------------------------------Data loading
X = pickle.load(open("X.pickle","rb"))
y = pickle.load(open("y.pickle","rb"))

X = X/255.0

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
			
	model.fit(X, y, batch_size = 100, epochs = 5, validation_split = 0.2)
# -----------------------------------------------------------------------------------EoF