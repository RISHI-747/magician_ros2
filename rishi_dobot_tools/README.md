# rishi_dobot_tools

Additional Dobot Magician ROS 2 tools.

## Build

From the root of the ROS 2 workspace:

```bash
colcon build --packages-select rishi_dobot_tools
source install/setup.bash
```

## Non-motion checks

```bash
ros2 run rishi_dobot_tools connection_check
ros2 run rishi_dobot_tools pose_monitor
```

## Record TCP pose

```bash
ros2 run rishi_dobot_tools record_pose --output dobot_pose.csv
```

## PTP

Dry run:

```bash
ros2 run rishi_dobot_tools ptp_cli --target 200 0 100 0
```

Real motion:

```bash
ros2 run rishi_dobot_tools ptp_cli --target 200 0 100 0 --velocity 0.15 --acceleration 0.15 --execute
```

Validate the robot workspace and target before using `--execute`.

## Gripper

Dry run:

```bash
ros2 run rishi_dobot_tools gripper_cli open
ros2 run rishi_dobot_tools gripper_cli close
```

Real command:

```bash
ros2 run rishi_dobot_tools gripper_cli open --execute
```

## Suction

```bash
ros2 run rishi_dobot_tools suction_cli on
ros2 run rishi_dobot_tools suction_cli off
```

Use `--execute` for the real robot.

## Camera-to-robot calibration

This utility fits a 2-D affine mapping from image pixels to robot XY.

```bash
python3 rishi_dobot_tools/rishi_dobot_tools/camera_robot_calibration.py   --camera "100,200" "300,200" "100,400"   --robot  "200,50"  "240,50"  "200,90"   --query "220,300"
```

Use measured calibration points from your actual setup. Do not use the example numbers for a real robot.

## Pick and place

The sequence is dry-run by default:

```bash
ros2 run rishi_dobot_tools pick_place_demo   --pick 200 0 40   --place 220 40 40   --safe-z 120
```

Real execution requires `--execute`:

```bash
ros2 run rishi_dobot_tools pick_place_demo   --pick 200 0 40   --place 220 40 40   --safe-z 120   --velocity 0.15   --acceleration 0.15   --execute
```

These are examples only. Measure and validate the actual safe coordinates for the robot and end effector.
