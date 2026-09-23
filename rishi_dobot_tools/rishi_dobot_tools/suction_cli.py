#!/usr/bin/env python3
"""Control the Dobot suction cup service, with explicit execution."""

import argparse

import rclpy
from rclpy.node import Node
from dobot_msgs.srv import SuctionCupControl


class SuctionClient(Node):
    def __init__(self):
        super().__init__("rishi_suction_client")
        self.client = self.create_client(
            SuctionCupControl, "/dobot_suction_cup_service"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state", choices=["on", "off"])
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    enable = args.state == "on"

    if not args.execute:
        print(f"DRY RUN: would set suction to {enable}.")
        print("Add --execute to command the real end effector.")
        return

    rclpy.init()
    node = SuctionClient()
    try:
        if not node.client.wait_for_service(timeout_sec=5.0):
            raise RuntimeError("Suction service is unavailable")

        req = SuctionCupControl.Request()
        req.enable_suction = enable

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
