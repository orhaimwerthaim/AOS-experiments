#!/usr/bin/env python
# license removed for brevity
# from https://answers.ros.org/question/337065/what-is-the-correct-way-to-spawn-a-model-to-gazebo-using-a-python-script/
# see https://www.programcreek.com/python/example/116064/gazebo_msgs.srv.SpawnModel


from gazebo_msgs.srv import SpawnModel, DeleteModel, DeleteModelRequest
import rospy
from geometry_msgs.msg import Pose
 


def spawn_model():
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
        spawn_model()
    except rospy.ROSInterruptException:
        rospy.loginfo("spawn_model test finished.")
