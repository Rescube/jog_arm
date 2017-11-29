#!/usr/bin/env python

# Take joystick cmds. Republish them as twist for
# e.g. jogging.

# RB: +x, LB: -x
# L on L dpad: +x
# Up on L dpad: +z

# R on R stick: +Rx
# Up on R stick: +Ry
# B: +Rz, A: -Rz

import rospy
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Joy

class joy_to_twist:

    def __init__(self):
        self.pub = rospy.Publisher('jog_arm_server/delta_jog_cmds', TwistStamped, queue_size=1)

    # Convert to TwistStamped and republish
    def callback(self, joy):
        #rospy.loginfo("Incoming joy: %s", joy)
        #rospy.loginfo("")

        ts = TwistStamped()

        ts.header.stamp = rospy.Time.now()

        ts.header.frame_id = rospy.get_param("joy_to_twist/cmd_frame")

        # These buttons are binary
        ts.twist.linear.x = -joy.buttons[4] + joy.buttons[5]
        # Double buttons
        ts.twist.linear.y = joy.axes[0]
        ts.twist.linear.z = joy.axes[1]

        ts.twist.angular.x = -joy.axes[3]
        ts.twist.angular.y = joy.axes[4]
        # These buttons are binary
        ts.twist.angular.z = -joy.buttons[0] + joy.buttons[1]

        #rospy.loginfo("Outgoing ts: %s", ts)
        #rospy.loginfo("")

        self.pub.publish(ts)
        
    def republish(self):
        rospy.Subscriber("joy", Joy, self.callback)

        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('joy_to_twist', anonymous=True)
    republisher = joy_to_twist()
    republisher.republish()