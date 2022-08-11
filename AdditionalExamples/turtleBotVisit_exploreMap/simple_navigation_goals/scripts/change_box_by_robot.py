#!/usr/bin/env python
# license removed for brevity
# from https://answers.ros.org/question/337065/what-is-the-correct-way-to-spawn-a-model-to-gazebo-using-a-python-script/
# see https://www.programcreek.com/python/example/116064/gazebo_msgs.srv.SpawnModel

#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_tf') 
import math
import tf
import geometry_msgs.msg 
from gazebo_msgs.srv import SpawnModel, DeleteModel, DeleteModelRequest
import rospy
from geometry_msgs.msg import Pose
 


def change_box_by_robot():
    print('started')
    listener = tf.TransformListener()
    (trans,rot) = listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
    print('trans:')
    print(trans)
    return
    while True:
	    rospy.init_node('spawn_model',log_level=rospy.INFO)
	    
	    srv = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
	    req = DeleteModelRequest()
	    req.model_name = 'my_model'
	    resp = srv(req)


	    pose = Pose()
	    pose.position.x = 3
	    pose.position.y = 2
	    pose.position.z = 1
	    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
	    spawn_model_client(model_name='my_model', model_xml=open('/home/or/catkin_ws/src/simple_navigation_goals/sources/box.sdf', 'r').read(), robot_namespace='/foo', initial_pose=pose, reference_frame='world')
	
    
if __name__ == '__main__':
    try:
        change_box_by_robot()
    except rospy.ROSInterruptException:
        rospy.loginfo("change_box_by_robot test finished.")
