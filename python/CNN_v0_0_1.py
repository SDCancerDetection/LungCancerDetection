# Convolutional Neural Network version 0.0.1
# Author: Joshua Stauffer
# Created: 12/03/2018
# Modified: 1/28/2019
# Summary: a Machine Learning model for finding nodules of lung cancer in CT scans
# -----------------------------------------------------------------------------------BoF
# Initializing
import tensorflow as tf
import numpy as np
import os
import cv2
import random

MODELDIR = "D:\Josh Stauffer\Documents\Senior Design\Cancer Detection Code\models"
DATADIR = "D:\Josh Stauffer\Documents\Senior Design\Cancer Detection Code\testdata_0"
CATEGORIES = ["Negative", "Positive"]
IMG_SIZE = 64
training_data = [] 	#Temp for creating data
train_data = []		#Actual data for training
train_labels = []	#Actual labesl for training

tf.logging.set_verbosity(tf.logging.INFO)
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

# Create CNN model
def cnn_model_fn(features, labels, mode):
	"""Model function for CNN."""
	# Input Layer
	input_layer = tf.reshape(features["x"], [-1,64,64,1])
	# Convolutional Layer #1, outputs [-1,64,64,8] tensor
	conv1 = tf.layers.conv2d(
		inputs = input_layer,
		filters = 8,
		kernel_size = 5,
		padding = "same",
		activation = tf.nn.leaky_relu)
	# Pooling Layer #1, outputs [-1,32,32,8] tensor
	pool1 = tf.layers.max_pooling2d(
		inputs = conv1,
		pool_size = 2,
		strides = 2)
	# Convolutional Layer #2, outputs [-1,32,32,16] tensor
	conv2 = tf.layers.conv2d(
		inputs = pool1,
		filters = 16,
		kernel_size = 5,
		padding = "same",
		activation = tf.nn.leaky_relu)
	# Pooling Layer #2, outputs [-1,16,16,16] tensor
	pool2 = tf.layers.max_pooling2d(
		inputs = conv1,
		pool_size = 2,
		strides = 2)
	#-----------------------------------------------Can add more layers here
	#Flatten tensor into a batch of vectors
	pool_flat = tf.reshape(pool2, [-1,1*1*16])
	#Dense Layer
	dense = tf.layers.dense(
		inputs = pool_flat,
		units = 16,
		activation = tf.nn.leaky_relu)
	#Dropout Layer during training only
	dropout = tf.layers.dropout(
		inputs = dense,
		rate = 0.33,					# Knob
		training = mode == tf.estimator.ModeKeys.TRAIN)
	#Logits Layer, current units: cancer - true or false
	logits = tf.layers.dense(
		inputs = dropout,
		units = 2)
		
	# Generate Predictions
	predictions = {
		"classes": tf.argmax(input = logits, axis = 1)
		"probabilities": tf.nn.softmax(logits, name = "softmax_tensor")
	}
	if mode == tf.estimator.ModeKeys.PREDICT:
		return tf.estimator.EstimatorSpec(mode = mode, predictions = predictions)
		
	# Calculate Loss
	loss = tf.losses.sparse_softmax_cross_entropy(labels = labels, logits = logits)
	
	# Config Training
	if mode == tf.estimator.ModeKeys.TRAIN:
		optimizer = tf.train.AdamOptimizer(learning_rate=0.001)	# Knob
		train_op = optimizer.minimize(
			loss=loss,
			global_step=tf.train.get_global_step())
		return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
		
	# Evaluation metrics
	eval_metric_ops = {
		"accuracy": tf.metrics.accuracy(
			labels = labels, predictions - predictions["classes"])}
	return tf.estimator.EstimatorSpec(
		mode = mode, loss = loss, eval_metric_ops = eval_metric_ops)
#-----------------------------------------------------------------------------------
def create_training_data():
	for category in CATEGORIES:
		path = os.path.join(DATADIR, category)    # path to Negative or Positive
		for img in os.listdir(path):
			img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
			reimg_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
			training_data.append([reimg_array, class_num])	
	random.shuffle(training_data)
	for features, labels in training_data
		train_data.append(features)
		train_labels.append(label)
		
	train_data = np.array(train_data).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
	
	#Save data for later
	np.save(train_data, train_data, allow_pickle=True,fix_imports=True)
	np.save(train_labels, train_labels, allow_pickle=True,fix_imports=True)			
#-----------------------------------------------------------------------------------		
def main(unused_argv):		
	# Create Training Data
	create_training_data()
	# Load in training data
	
	train_data = np.load(train_data, mmap_mode=None, allow_pickle=True, fix_imports=True)
	train_labels = np.load(train_labels, mmap_mode=None, allow_pickle=True, fix_imports=True)
	
	# Data to be used for evaluation?
	#eval_data = 
	#eval_labels = 
	
	# Create the estimator
	ct_classifier = tf.estimator.Estimator(
		model_fn = cnn_model_fn, model_dir = MODELDIR)
		
	# Logging hook
	tensors_to_log = {"probabilities": "softmax_tensor"}
	logging_hook = tf.train.LoggingTensorHook(
		tensors = tensors_to_log, every_n_iter = 64)					# Knob
		
	# Train model
	train_input_fn = tf.estimator.inputs.numpy_input_fn(
		x = {"x": train_data},
		y = train_labels,
		batch_size = 64,												# Knob
		num_epochs = None,
		shuffle = True)
	ct_classifier.train(
		input_fn = train_input_fn,
		steps = 20000,													# Knob
		hooks = [logging_hook])
		
	# Evaluate model
	eval_input_fn = tf.estimator.inputs.numpy_input_fn(
		x = {"x": eval_data},
		y = eval_labels,
		num_epochs = None,
		shuffle = False)
	eval_results = ct_classifier.evaluate(input_fn = eval_input_fn)
	print(eval_results)
	# Save model to file
	# TODO

# -----------------------------------------------------------------------------------EoF