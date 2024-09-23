#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler


def movebase_client():
    # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()
    # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    x_goal= float(input("Please enter value of x-coordinate")) # Value of X should be within -2 to 2
    y_goal= float(input("Please enter value of y-coordinate")) # Value of Y should be within -2 to 2
    #According to the boxes inside gazebo (Each box is 1) and origin inside gazebo is in the center
    while (x_goal>2 or y_goal >2 or x_goal<-2 or y_goal<-2): 
            print("Please enter coordinates of x and y in the range of -2 to 2")
            x_goal= float(input("Please enter value of x-coordinate"))
            y_goal= float(input("Please enter value of y-coordinate"))
    # Set the goal position
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x_goal #Move to coordinate x_goal
    goal.target_pose.pose.position.y = y_goal  # Move to coordinate y_goal
    goal.target_pose.pose.position.z = 0  # No lateral movement

    # Set the goal orientation to face forward
    quaternion = quaternion_from_euler(0, 0, 0)  # Roll, Pitch, Yaw
    goal.target_pose.pose.orientation = Quaternion(*quaternion)
    # Sends the goal to the action server.
    client.send_goal(goal)
    
    # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
    # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        # Result of executing the action
        return client.get_result()
    
if __name__ == '__main__':
    try:
        # Initialize a ROS node
        rospy.init_node('send_goal_py')
        result = movebase_client()

        if result:
            rospy.loginfo("Goal execution done!")
         #If robot rotated in its place, this means that coordinates entered will make robot collide
            rospy.loginfo("If robot is rotating around itself in its place, this is due to that it'll collide at the coordinates you've entered")

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
