#!/usr/bin/env python3
"""2-D camera-pixel to robot-XY affine calibration.

Usage:
  python3 camera_robot_calibration.py \
      --camera "100,200" "300,200" "100,400" \
      --robot  "200,50"  "240,50"  "200,90"

Then provide a pixel coordinate to transform.
"""

import argparse
import numpy as np


def fit_affine(camera_points, robot_points):
    camera = np.asarray(camera_points, dtype=float)
    robot = np.asarray(robot_points, dtype=float)

    if camera.shape[0] < 3:
        raise ValueError("At least 3 calibration points are required.")
    if camera.shape != robot.shape or camera.shape[1] != 2:
        raise ValueError("Both point sets must have shape N x 2.")

    A = np.column_stack([camera, np.ones(len(camera))])
    params_x, *_ = np.linalg.lstsq(A, robot[:, 0], rcond=None)
    params_y, *_ = np.linalg.lstsq(A, robot[:, 1], rcond=None)

    return np.vstack([params_x, params_y])


def transform(M, uv):
    u, v = uv
    result = M @ np.array([u, v, 1.0])
    return result


def parse_point(text):
    return [float(v) for v in text.split(",")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", nargs="+", required=True,
                        help='Points like "u,v"')
    parser.add_argument("--robot", nargs="+", required=True,
                        help='Corresponding points like "x,y"')
    parser.add_argument("--query", help='Camera point "u,v" to transform')
    args = parser.parse_args()

    camera = [parse_point(p) for p in args.camera]
    robot = [parse_point(p) for p in args.robot]

    M = fit_affine(camera, robot)

    np.set_printoptions(precision=6, suppress=True)
    print("Affine transform:")
    print(M)

    if args.query:
        xy = transform(M, parse_point(args.query))
        print(f"Robot XY: x={xy[0]:.3f}, y={xy[1]:.3f}")


if __name__ == "__main__":
    main()
