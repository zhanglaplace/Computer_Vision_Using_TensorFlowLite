"""
    Script passes raw image to an already trained model to get prediction

            @date: 20th December, 2017
            @Language: Python

usage = $python classify_img_arg.py [saved_model_directory] [path_to_image]

#IMPORTS, VARIABLE DECLARATION, AND LOGGING TYPE SETTING
----------------------------------------------------------------------------------------------------------------------------------------------------------------"""


from __future__ import absolute_import
from __future__ import print_function

import sys
import os
import math
import time
import numpy as np
import tensorflow as tf #import tensorflow
import matplotlib.pyplot as plt
from PIL import Image

flags = tf.app.flags
flags.DEFINE_integer("image_width", "227", "Alexnet input layer width")
flags.DEFINE_integer("image_height", "227", "Alexnet input layer height")
flags.DEFINE_integer("image_channels", "3", "Alexnet input layer channels")
flags.DEFINE_integer("num_of_classes", "43", "Number of training clases")
FLAGS = flags.FLAGS

tf.logging.set_verbosity(tf.logging.WARN) #setting up logging (can be DEBUG, ERROR, FATAL, INFO or WARN)
"""----------------------------------------------------------------------------------------------------------------------------------------------------------------"""


#TRAINING AND EVALUATING THE ALEXNET CNN CLASSIFIER
"""----------------------------------------------------------------------------------------------------------------------------------------------------------------"""
#Specify checkpoint & image directory
checkpoint_directory= sys.argv[1] # "/home/olu/Dev/data_base/sign_base/backup/Checkpoints_N_Model2-After_Epoch_20_copy/trained_alexnet_model"
filename= sys.argv[2]             # "/home/olu/Dev/data_base/sign_base/training_227x227/road_closed/00002_00005.jpeg"

#Declare categories/classes as string
categories = ["speed_20", "speed_30","speed_50","speed_60","speed_70",
    "speed_80","speed_less_80","speed_100","speed_120",
    "no_car_overtaking","no_truck_overtaking","priority_road",
    "priority_road_2","yield_right_of_way","stop","road_closed",
    "maximum_weight_allowed","entry_prohibited","danger","curve_left",
    "curve_right","double_curve_right","rough_road","slippery_road",
    "road_narrows_right","work_in_progress","traffic_light_ahead",
    "pedestrian_crosswalk","children_area","bicycle_crossing",
    "beware_of_ice","wild_animal_crossing","end_of_restriction",
    "must_turn_right","must_turn_left","must_go_straight",
    "must_go_straight_or_right","must_go_straight_or_left",
    "mandatroy_direction_bypass_obstacle",
    "mandatroy_direction_bypass_obstacle2", 
    "traffic_circle","end_of_no_car_overtaking",
    "end_of_no_truck_overtaking"];

print("resizing image.....")
#Process image to be sent to Neural Net
img = Image.open(filename)
img_resized = img.resize((FLAGS.image_width, FLAGS.image_height), Image.ANTIALIAS)
img_batch_np = np.array(img_resized)
plt.imshow(img_batch_np)
img_batch = img_batch_np.reshape(1, FLAGS.image_width, FLAGS.image_height,FLAGS.image_channels)

print("loading network graph.....")
#Recreate network graph.  
sess = tf.Session()
latest_checkpoint_name = tf.train.latest_checkpoint(checkpoint_dir=checkpoint_directory)
saver = tf.train.import_meta_graph(latest_checkpoint_name+'.meta') #At this step only graph is created.
    
#Accessing the default graph which we have restored
graph = tf.get_default_graph()

print("loading network weights.....")
#Get model's graph
checkpoint_file=tf.train.latest_checkpoint(checkpoint_directory)
saver.restore(sess, checkpoint_file) #Load the weights saved using the restore method.

print("classification process started.....")
start = time.time()
probabilities = graph.get_tensor_by_name("softmax_tensor:0")
classes = graph.get_tensor_by_name("ArgMax:0") #'ArgMax:0' is the name of the argmax tensor in the train_alexnet.py file.
feed_dict = {"Reshape:0": img_batch} #'Reshape:0' is the name of the 'input_layer' tensor in the train_alexnet.py. Given to it as default.
predicted_class = sess.run(classes, feed_dict)
predicted_probabilities = sess.run(probabilities, feed_dict)
assurance = predicted_probabilities[0,int(predicted_class)]*100;
end = time.time()
difference = end-start
difference_milli = difference*1000

print("Predicted Sign: '", categories[int(predicted_class)], "' With ", assurance," Percent Assurance")
print("Time Taken For Classification: %f millisecond(s)" % difference_milli)
plt.show()
"""----------------------------------------------------------------------------------------------------------------------------------------------------------------"""
