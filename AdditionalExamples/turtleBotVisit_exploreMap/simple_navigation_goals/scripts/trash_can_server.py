#!/usr/bin/env python
# license removed for brevity
# from https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/
import rospy
import actionlib 
from simple_navigation_goals.srv import trash_can_update,trash_can_updateResponse#

trash_cans = {1:1,2:5}#{canId:spaceLeft,canId:spaceLeft}
 
def handle_trash_can_update(req):
    print("handle_trash_can_update(req):req")
    print(req)

    print("trash cans current state:")
    print(trash_cans)
    
    if req.can_id != 1 and req.can_id != 2: 
	print("invalid 'can_id', valid values are '1' or '2'!")
	return trash_can_updateResponse(-1000)
    
    if req.add_cup:
        trash_cans[req.can_id] = trash_cans[req.can_id] -1
  
    if req.add_cup:
        print("trash cans after update:")
        print(trash_cans)
    
    return trash_can_updateResponse(trash_cans[req.can_id])



def trash_can_server():
    rospy.init_node('trash_can_server')
    s = rospy.Service('/trash_can_update', trash_can_update, handle_trash_can_update)
    print("Ready to update or query trash cans.")
    rospy.spin()

if __name__ == '__main__':
    try:
        trash_can_server()
    except rospy.ROSInterruptException:
        rospy.loginfo("trash_can_server test finished.")
