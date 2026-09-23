# RISHI G — Dobot Magician ROS 2 Work

## Overview

This repository is based on the MIT-licensed `magician_ros2` ROS 2 control stack for the Dobot Magician.

This document separates the upstream control stack from the additional tools and experiments developed in this workspace.

## Work covered

- USB/serial connection testing with the Dobot Magician.
- Verification of the robot device and ROS 2 communication.
- Reading the robot TCP pose and joint-state feedback.
- Testing point-to-point (PTP) motion through the ROS 2 action interface.
- Working with Cartesian XYZ targets and robot orientation.
- Working with robot coordinate calculations and kinematics concepts.
- Recording robot pose data for experiments.
- Building camera-to-robot coordinate mapping utilities.
- Calibration from camera/image coordinates to robot coordinates.
- Designing a corrected-coordinate pick-and-place workflow.
- Adding gripper and suction-cup command helpers.
- Adding a dry-run-first pick-and-place demonstration.
- Organizing repeatable commands and experiment notes for the Dobot Magician.

## Safety

The tools in `rishi_dobot_tools` default to non-motion/dry-run behavior where practical.
Real robot motion must be explicitly requested with `--execute`.

Before executing motion:

1. Confirm the robot is clear of people and obstacles.
2. Confirm the target coordinates are inside the robot's safe workspace.
3. Use low velocity and acceleration ratios during testing.
4. Be ready to stop the robot immediately.
5. Never run two independent programs that command the robot at the same time.

## Attribution

The underlying `magician_ros2` control stack remains under its original MIT license and attribution.

The files under `rishi_dobot_tools/` and the documentation in this section are additional work for this repository.
