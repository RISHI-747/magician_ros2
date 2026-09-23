#!/usr/bin/env python3
"""Control the Dobot gripper service, with explicit execution."""

import argparse

import rclpy
from rclpy.node import Node
from dobot_msgs.srv import GripperControl


class GripperClient(Node):
    def __init__(self):
        super().__init__("rishi_gripper_client")
        self.client = self.create_client(
            GripperControl, "/dobot_gripper_service"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state", choices=["open", "close"])
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--keep-compressor-running", action="store_true")
    args = parser.parse_args()

    if not args.execute:
        print(f"DRY RUN: would set gripper to {args.state}.")
        print("Add --execute to command the real end effector.")
        return

    rclpy.init()
    node = GripperClient()
    try:
        if not node.client.wait_for_service(timeout_sec=5.0):
            raise RuntimeError("Gripper service is unavailable")

        req = GripperControl.Request()
        req.gripper_state = args.state
        req.keep_compressor_running = args.keep_compressor_running

        future = node.client.call_async(req)
        rclpy.spin_until_future_complete(node, future)
        response = future.result()
        print(f"success={response.success}")
        print(response.message)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
