#!/usr/bin/env python3
"""Send a Dobot PTP goal. Defaults to dry-run for safety."""

import argparse

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from dobot_msgs.action import PointToPoint


class PTPClient(Node):
    def __init__(self):
        super().__init__("rishi_ptp_client")
        self.client = ActionClient(self, PointToPoint, "/PTP_action")

    def send(self, motion_type, target, velocity, acceleration):
        if not self.client.wait_for_server(timeout_sec=5.0):
            raise RuntimeError("/PTP_action is not available")

        goal = PointToPoint.Goal()
        goal.motion_type = motion_type
        goal.target_pose = target
        goal.velocity_ratio = velocity
        goal.acceleration_ratio = acceleration

        self.get_logger().info(
            f"Sending PTP: type={motion_type}, target={target}, "
            f"v={velocity}, a={acceleration}"
        )

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_cb,
        )
        rclpy.spin_until_future_complete(self, future)
        handle = future.result()

        if handle is None or not handle.accepted:
            raise RuntimeError("PTP goal was rejected")

        result_future = handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return result_future.result().result

    def feedback_cb(self, feedback_msg):
        pose = feedback_msg.feedback.current_pose
        self.get_logger().info(f"Current pose: {list(pose)}")


def main():
    parser = argparse.ArgumentParser(description="Dobot PTP command")
    parser.add_argument("--motion-type", type=int, default=1,
                        choices=[1, 2, 4, 5])
    parser.add_argument("--target", nargs=4, type=float, required=True,
                        metavar=("X", "Y", "Z", "R"))
    parser.add_argument("--velocity", type=float, default=0.2)
    parser.add_argument("--acceleration", type=float, default=0.2)
    parser.add_argument("--execute", action="store_true",
                        help="Actually command the robot. Without this flag the command is dry-run.")
    args = parser.parse_args()

    print("Dobot PTP command")
    print(f"motion_type={args.motion_type}")
    print(f"target={args.target}")
    print(f"velocity={args.velocity}")
    print(f"acceleration={args.acceleration}")

    if not args.execute:
        print("\nDRY RUN: robot will NOT move.")
        print("Add --execute only after checking the target and workspace.")
        return

    rclpy.init()
    node = PTPClient()
    try:
        result = node.send(
            args.motion_type,
            args.target,
            args.velocity,
            args.acceleration,
        )
        print(f"Achieved pose: {list(result.achieved_pose)}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
