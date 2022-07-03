#!/usr/bin/python
import datetime
import rospy  
import pymongo
import operator
import traceback
import numpy as np
from robotican_demos_upgrade.srv import *
from geometry_msgs.msg import Point,Point,Pose,Quaternion
from simple_navigation_goals.srv import navigate,navigateResponse
from rosgraph_msgs.msg import Log
from std_srvs.srv import *
from nav_msgs.msg import OccupancyGrid


my_map=None
count=0
def cd__map(data):
        try:
	    global count
            count=count+1
	    print('/map message')
            my_map=data.data
	    print('Count=',count)
            arr = np.array(my_map)
	    un = np.count_nonzero(arr == -1)
	    print(un,', unknown grid cells')
    	    #print(my_map)
        except Exception as e:
            print('Error:',str(e), traceback.format_exc(e))




if __name__ == '__main__':
    try:
	print('1')
        rospy.init_node('aos_ros_middleware_auto222', anonymous=True)
	print('2')	
	rospy.Subscriber("/map", OccupancyGrid, cd__map, queue_size=1000)
        print('3')
	rospy.spin()
    except Exception as e:
        print('main error:',str(e))
    
