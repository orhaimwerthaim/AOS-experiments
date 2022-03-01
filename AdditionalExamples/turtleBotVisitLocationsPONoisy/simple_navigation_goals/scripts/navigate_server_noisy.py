#!/usr/bin/env python
# license removed for brevity
# from https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/
import rospy
import actionlib
import random
from geometry_msgs.msg import Point
from simple_navigation_goals.srv import navigate,navigateResponse#
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

SUCCEEDED = 3
# def movebase_client():
#     print("2")
#     client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
#     client.wait_for_server()
#
#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"
#     goal.target_pose.header.stamp = rospy.Time.now()
#     goal.target_pose.pose.position.x = -0.790801882744
#     goal.target_pose.pose.position.y = -1.71117520332
#     goal.target_pose.pose.position.z = 0.00247192382812
#     goal.target_pose.pose.orientation.w = 1.0
#
#     print("goal sent:")
#     print(goal)
#     client.send_goal(goal)
#     wait = client.wait_for_result()
#     if not wait:
#         rospy.logerr("Action server not available!")
#         rospy.signal_shutdown("Action server not available!")
#     else:
#         return client.get_result()

def callback_active():
    rospy.loginfo("Action server is processing the goal")

def callback_done(state, result):
    rospy.loginfo("Action server is done. State: %s, result: %s" % (str(state), str(result)))

def callback_feedback(feedback):
    rospy.loginfo("Feedback:%s" % str(feedback))

def handle_navigate(req):
    print("handle_navigate(req):req.goal")
    print(req.goal)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = req.goal.x
    goal.target_pose.pose.position.y = req.goal.y
    goal.target_pose.pose.position.z = req.goal.z
    goal.target_pose.pose.orientation.w = 1.0

    print("goal sent:")
    #print(goal)
    client.send_goal(goal)#, active_cb=callback_active, feedback_cb=callback_feedback, done_cb=callback_done)
    wait = client.wait_for_result()
    res = navigateResponse(success = False);

    if not wait:
        print("----------------not_wait----------------------")
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
        return res
    else:
        print("----------------res----------------------")
        print("real result:")
        print(client.get_state() == SUCCEEDED)
        res.success = client.get_state() == SUCCEEDED
        print("result after adding noise:")
        if client.get_state() == SUCCEEDED and random.random() < 0.1:
            res.success = client.get_state() != SUCCEEDED
        print(res)
        return res



def navigate_server():
    rospy.init_node('navigate_server')
    s = rospy.Service('/navigate_to_point', navigate, handle_navigate)
    print "Ready to navigate."
    rospy.spin()

if __name__ == '__main__':
    try:
        navigate_server()
        if False:
            rospy.init_node('movebase_client_py')
            #result = movebase_client()
            if result:
                rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
