#!/usr/bin/env python3
"""Print live Dobot TCP pose and joint-state feedback."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped


class PoseMonitor(Node):
    def __init__(self):
        super().__init__("rishi_pose_monitor")
        self.create_subscription(PoseStamped, "/dobot_TCP", self.tcp_cb, 10)
        self.create_subscription(JointState, "/joint_states", self.joint_cb, 10)

    def tcp_cb(self, msg):
        p = msg.pose.position
        q = msg.pose.orientation
        self.get_logger().info(
            f"TCP xyz = ({p.x:.3f}, {p.y:.3f}, {p.z:.3f}) m | "
            f"quat = ({q.x:.3f}, {q.y:.3f}, {q.z:.3f}, {q.w:.3f})"
        )

    def joint_cb(self, msg):
        if msg.position:
            degrees = [round(v * 180.0 / 3.141592653589793, 2) for v in msg.position]
            self.get_logger().debug(f"Joint positions [deg]: {degrees}")


def main():
    rclpy.init()
    node = PoseMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
