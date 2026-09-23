#!/usr/bin/env python3
"""Simple Dobot pick-and-place sequence using PTP Cartesian goals.

The sequence is dry-run by default. Real motion requires --execute.
The coordinates are examples and MUST be adapted and checked for the
actual robot, tool, workspace and object.
"""

import argparse
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from dobot_msgs.action import PointToPoint


class PickPlace(Node):
    def __init__(self):
        super().__init__("rishi_pick_place")
        self.client = ActionClient(self, PointToPoint, "/PTP_action")

    def move(self, xyzr, velocity, acceleration):
        goal = PointToPoint.Goal()
        goal.motion_type = 1
        goal.target_pose = list(xyzr)
        goal.velocity_ratio = velocity
        goal.acceleration_ratio = acceleration

        future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        handle = future.result()
        if not handle or not handle.accepted:
            raise RuntimeError(f"PTP rejected: {xyzr}")

        result_future = handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return result_future.result().result

    def run(self, pick, place, safe_z, velocity, acceleration):
        if not self.client.wait_for_server(timeout_sec=5.0):
            raise RuntimeError("/PTP_action is unavailable")

        px, py, pz, pr = pick
        qx, qy, qz, qr = place

        sequence = [
            ("approach_pick", [px, py, safe_z, pr]),
            ("pick_height", [px, py, pz, pr]),
            ("lift", [px, py, safe_z, pr]),
            ("approach_place", [qx, qy, safe_z, qr]),
            ("place_height", [qx, qy, qz, qr]),
            ("lift_after_place", [qx, qy, safe_z, qr]),
        ]

        for name, target in sequence:
            self.get_logger().info(f"{name}: {target}")
            self.move(target, velocity, acceleration)
            time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pick", nargs=3, type=float, required=True,
                        metavar=("X", "Y", "Z"))
    parser.add_argument("--place", nargs=3, type=float, required=True,
                        metavar=("X", "Y", "Z"))
    parser.add_argument("--safe-z", type=float, default=120.0)
    parser.add_argument("--rotation", type=float, default=0.0)
    parser.add_argument("--velocity", type=float, default=0.15)
    parser.add_argument("--acceleration", type=float, default=0.15)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    pick = [*args.pick, args.rotation]
    place = [*args.place, args.rotation]

    print("Pick-and-place plan:")
    print(f"  pick : {pick}")
    print(f"  place: {place}")
    print(f"  safe z: {args.safe_z}")

    if not args.execute:
        print("\nDRY RUN: no robot motion will occur.")
        print("Add --execute only after validating every coordinate.")
        return

    rclpy.init()
    node = PickPlace()
    try:
        node.run(
            pick, place, args.safe_z,
            args.velocity, args.acceleration
        )
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
