#!/usr/bin/python
from __future__ import print_function
import datetime
import rospy  
import tf
import operator
import traceback
import numpy as np
from robotican_demos_upgrade.srv import *
from geometry_msgs.msg import Point,Point,Pose,Quaternion
from simple_navigation_goals.srv import navigate,navigateResponse
from rosgraph_msgs.msg import Log
from std_srvs.srv import *
from nav_msgs.msg import OccupancyGrid
import math 


map_data = None
map_resolution = None
map_width = None
map_height = None
map_position_x = None
map_position_y = None
def cd__map(data):
    global map_resolution
    global map_width
    global map_height
    global map_position_x
    global map_position_y
    global map_data
    map_data = data.data
    if map_resolution is None:
	map_resolution = data.info.resolution
        map_width = data.info.width
        map_height = data.info.height
        map_position_x = data.info.origin.position.x
        map_position_y = data.info.origin.position.y
	    
 
def get_map_cell(x,y):
    return map_data[int(x+y*map_width)]
    #val = map_data[int(x+y*map_width)]
    #if val > 50:
    #    return 100
    #return         

if __name__ == '__main__':
    global map_resolution
    global map_width
    global map_height
    pub_real = rospy.Publisher('robot_location/real', Pose, queue_size=10)
    pub_occ = rospy.Publisher('robot_location/occupancy_map', Pose, queue_size=10)
    # initialize node
    rospy.init_node('robot_location_publisher')
    rospy.Subscriber("/map", OccupancyGrid, cd__map, queue_size=1)#
    #rospy.Subscriber("/move_base/global_costmap/costmap", OccupancyGrid, cd__map, queue_size=1)
    # print in console that the node is running
    # create tf listener
    listener = tf.TransformListener()
    # set the node to run 1 time per second (1 hz)
    rate = rospy.Rate(10.0)
    # loop forever until roscore or this node is down
    while not rospy.is_shutdown():
        try:
            # listen to transform
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
            # print the transform
            print('---------')
	    print('x:' + str(trans[0]) + ', y:'+str(trans[1]))
            print('Translation: ' + str(trans))
            print('Rotation: ' + str(rot))
            euler = tf.transformations.euler_from_quaternion(rot)
            print('euler:' + str(euler) + '     deg:'+str(math.degrees(euler[2])))
		
	    #real pos
            #pose = Pose()
            #pose.position.x = trans[0]
            #pose.position.y = trans[1]
            #pose.orientation.w = math.degrees(euler[2])
	    #pub.publish(pose)
	    pose = Pose()
            pose.position.x = trans[0]
            pose.position.y = trans[1]
            pose.orientation.w = math.degrees(euler[2])
            pub_real.publish(pose)

	    #pose in occupancy map
            if(map_resolution is not None):
                robX=int((trans[0] - map_position_x) / map_resolution)
                robY=int((trans[1] - map_position_y) / map_resolution)
	        pose = Pose()
                pose.position.x = robX
                pose.position.y = robY

                pose.orientation.w = math.degrees(euler[2])
		print('location in Grid: (' + str(robX) + ',' + str(robY) + ')')
	        pub_occ.publish(pose)
		print('-----------------------------------------')
                print(map_width)
		print('-----------------------------------------')
                w=int(map_width)
                GREEN = '\033[32m'
                WHITE = '\033[37m'
                ONE='\033[1;32;40m'
                TWO=''
                a=""
                print('robX:'+str(robX) + ',robY:'+str(robY))
                if False:
		        for row in range(w,-1,-1):    
		            has=False
			    for col in range(w):
		                color = WHITE
		                #print('abs(col-robX):'+str(abs(col-robX)) + ', abs(row-robY):'+str(abs(row-robY)))
		                if abs(col-robX) < 50 and abs(row-robY) < 50:
		                    has=True
		                    color = GREEN 
				#a=a + str(get_map_cell(robY+ col -int(w/2),row)) + ','
		                    a= a +color + '' + str(get_map_cell(col,row)) + ','
		            if has:
		                a=a+'\n'
		        print(a)
                if a is not "":
                    quit()
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        # sleep to control the node frequency
        rate.sleep()
