#!/usr/bin/env python3
"""Record /dobot_TCP to CSV without commanding the robot."""

import argparse
import csv
from datetime import datetime, timezone

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped


class PoseRecorder(Node):
    def __init__(self, output):
        super().__init__("rishi_pose_recorder")
        self.file = open(output, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow(
            ["timestamp_utc", "x_m", "y_m", "z_m", "qx", "qy", "qz", "qw"]
        )
        self.create_subscription(PoseStamped, "/dobot_TCP", self.cb, 20)

    def cb(self, msg):
        p = msg.pose.position
        q = msg.pose.orientation
        self.writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            p.x, p.y, p.z, q.x, q.y, q.z, q.w
        ])
        self.file.flush()

    def close(self):
        self.file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dobot_pose.csv")
    args = parser.parse_args()

    rclpy.init()
    node = PoseRecorder(args.output)
    node.get_logger().info(f"Recording /dobot_TCP to {args.output}")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
