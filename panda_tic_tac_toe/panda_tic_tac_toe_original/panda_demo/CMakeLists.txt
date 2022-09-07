cmake_minimum_required(VERSION 3.0.2)
project(panda_demo)
 
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  genmsg 
)

add_service_files(
   FILES
  detect_new_state.srv
  mark_cell.srv
)
 
 generate_messages(
   DEPENDENCIES
   std_msgs 
 )

 
catkin_package(
CATKIN_DEPENDS message_runtime
)

include_directories( 
# include
  ${catkin_INCLUDE_DIRS}
)
 
