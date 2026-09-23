#!/usr/bin/env python3
"""Non-motion health check for the Dobot Magician ROS 2 stack."""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from dobot_msgs.action import PointToPoint
from dobot_msgs.srv import GripperControl, SuctionCupControl


class ConnectionCheck(Node):
    def __init__(self):
        super().__init__("rishi_connection_check")
        self.joint_seen = False
        self.tcp_seen = False

        self.create_subscription(JointState, "/joint_states", self.joint_cb, 10)
        self.create_subscription(PoseStamped, "/dobot_TCP", self.tcp_cb, 10)

        self.ptp = ActionClient(self, PointToPoint, "/PTP_action")
        self.gripper = self.create_client(GripperControl, "/dobot_gripper_service")
        self.suction = self.create_client(SuctionCupControl, "/dobot_suction_cup_service")

    def joint_cb(self, _msg):
        self.joint_seen = True

    def tcp_cb(self, _msg):
        self.tcp_seen = True


def main():
    rclpy.init()
    node = ConnectionCheck()
    node.get_logger().info("Checking Dobot ROS 2 interfaces. No robot motion will be commanded.")

    for _ in range(20):
        rclpy.spin_once(node, timeout_sec=0.1)

    print("\nDobot ROS 2 connection check")
    print("--------------------------------")
    print(f"/joint_states received:       {node.joint_seen}")
    print(f"/dobot_TCP received:           {node.tcp_seen}")
    print(f"/PTP_action available:         {node.ptp.wait_for_server(timeout_sec=0.2)}")
    print(f"/dobot_gripper_service ready:  {node.gripper.wait_for_service(timeout_sec=0.2)}")
    print(f"/dobot_suction_cup_service:    {node.suction.wait_for_service(timeout_sec=0.2)}")
    print("\nNo motion was requested.")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
