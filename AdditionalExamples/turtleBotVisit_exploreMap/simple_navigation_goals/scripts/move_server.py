#!/usr/bin/python
import datetime
import rospy  
import pymongo
import operator
import traceback
import numpy as np
from robotican_demos_upgrade.srv import *
from geometry_msgs.msg import Point,Point,Pose,Quaternion 
from rosgraph_msgs.msg import Log
from std_srvs.srv import *
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Twist
from simple_navigation_goals.srv import move,moveResponse# 

#map_published=False
sub_once = None
counter=0
def cb__map(data):
	global counter
 #       global map_published
        print(counter)
        counter=1+counter
	map_published = True
  #      print('counter:',counter)

def handle_move(req):
    global map_published
    global sub_once
    global counter
    counter=0
    map_published = False
    print("handle_move(req):req")
    print(req)
    if abs(req.angular) > 0:
	move_robot(0.0, req.angular)
        rospy.sleep(0.15)
    if abs(req.linear) > 0:
	move_robot(req.linear, 0.0) 
    
    sub_once = rospy.Subscriber("/map", OccupancyGrid, cb__map, queue_size=1000)
    while not counter>1:
        rospy.sleep(0.05)
#	print('counter:',counter)
    
    sub_once.unregister()

    return moveResponse()


def move_robot(lin,ang):
        try:
	    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    	     
	     
	    # Create a Twist message and add linear x and angular z values
	    move_cmd = Twist()
	    a=0
	    while a<100:
	        a=a+1
		rospy.sleep(0.01)
		print(a)
		move_cmd.linear.x = lin
	    	move_cmd.angular.z = ang
	        print(pub.publish(move_cmd))
	    print(move_cmd)
 	    print(pub.publish(Twist()))
        except Exception as e:
            print('Error:',str(e), traceback.format_exc(e))




if __name__ == '__main__':
    try:
	rospy.init_node('move_server', anonymous=True)
	s = rospy.Service('/move', move, handle_move)
        print("Ready to move.")
        rospy.spin()
	#move(0.0,1.5)rotate 90 deg left
	#move(0.5, 0.0)
    except Exception as e:
        print('main error:',str(e))
    
