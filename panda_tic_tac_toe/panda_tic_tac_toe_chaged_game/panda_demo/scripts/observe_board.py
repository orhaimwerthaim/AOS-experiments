#!/usr/bin/env python

from __future__ import print_function

import sys
from sys import exit
from panda_demo.srv import detect_new_state, detect_new_stateResponse
import time
from datetime import datetime
import signal
import string

import os, time, signal, threading
import subprocess
from subprocess import Popen, PIPE, call


import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from subprocess import Popen, PIPE

global current_img_msg 

#crop image variables
left=390
right=1050
top=100
bottom=580
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2


def observe_cb(req):
    global current_img_msg
    bridge = CvBridge()
    if current_img_msg is None:
        print('NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONE')
    cv_image=None
    try:
      cv_image =bridge.imgmsg_to_cv2(current_img_msg, desired_encoding='passthrough')
      #cv_image = bridge.imgmsg_to_cv(current_img_msg, "bgr8")
    except CvBridgeError as e:
    #except Exception as e:
      print(e)

    
        
    start_point=(left,top)
    end_point=(right,bottom)
    image = cv2.rectangle(cv_image, start_point, end_point, color, thickness)   
    cv2.imwrite('/home/or/catkin_ws/src/panda_demo/scripts/original_camera_image.jpg', cv_image)
    print('cv_image.shape:',cv_image.shape)
    cropped_image = cv_image[top+thickness:bottom-thickness,left+thickness:right-thickness]
    cv2.imwrite('/home/or/catkin_ws/src/panda_demo/scripts/cropped_camera_image.jpg', cropped_image)

    

    process = Popen(["bash", "/home/or/catkin_ws/src/panda_demo/scripts/run_image_detection.bash"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    
 
    message = output.replace('\'','').replace(',','').replace('[','').replace(']','').replace(' ','').replace('~','cannot proccess image').replace('\n','')
    try:      
        return detect_new_state(message)
        
    except:
        return detect_new_stateResponse(message)
        

def callback(data):
    global current_img_msg
    current_img_msg=data
    

 
if __name__ == "__main__":
    camera_topic = "/camera/color/image_raw"
    #camera_topic = "/intel_d435/color/image_raw"#for debug
    #cv2.NamedWindow("Image window", 1)
    
    image_sub = rospy.Subscriber(camera_topic,Image,callback)
    current_img_msg = None
    rospy.init_node('observe_tic_tac_toe_board_node')
    s = rospy.Service('observe_tic_tac_toe_board', detect_new_state, observe_cb)
    print("Ready to observe tic-tac-toe board!")
    rospy.spin()
 
    rospy.init_node('image_converter', anonymous=True)
    try:
      rospy.spin()
    except KeyboardInterrupt:
      print("Shutting down")
    cv2.DestroyAllWindows()
 
