# Dobot Magician Work Log

## 1. Connection

The Dobot Magician was connected to Ubuntu through USB. The Linux device was observed as `/dev/ttyACM0` in the development setup.

The upstream stack uses a configurable serial port. Check the active configuration before changing it.

Useful checks:

```bash
ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
groups
```

## 2. ROS 2 communication

The project uses ROS 2 topics, services and actions. Important interfaces include:

- `/joint_states`
- `/dobot_TCP`
- `/dobot_pose_raw`
- `/PTP_action`
- `/dobot_gripper_service`
- `/dobot_suction_cup_service`

## 3. Motion experiments

PTP goals use the `dobot_msgs/action/PointToPoint` interface.

Motion types:

- `1`: joint-interpolated motion with Cartesian target
- `2`: linear motion with Cartesian target
- `4`: joint-interpolated motion with joint target
- `5`: linear motion with joint target

The command-line tool in this repository defaults to dry-run mode and requires `--execute` for real motion.

## 4. Pose logging

`record_pose` subscribes to `/dobot_TCP` and writes timestamped Cartesian pose data to CSV.

This is useful for:

- repeatability tests
- trajectory inspection
- calibration experiments
- motion debugging

## 5. Camera-to-robot mapping

The repository includes a 2D affine mapping utility. Given corresponding camera pixels `(u, v)` and robot coordinates `(x, y)`, it estimates:

    [x]   [a b c] [u]
    [y] = [d e f] [v]
    [1]   [0 0 1] [1]

At least three non-collinear calibration points are required.

This is a planar calibration utility, not a substitute for a full hand-eye calibration.

## 6. Pick-and-place workflow

The example workflow is:

1. Move to a safe approach position.
2. Move above the detected object.
3. Move down to the pick height.
4. Activate the selected end effector.
5. Lift vertically.
6. Move to the place position.
7. Move down.
8. Release the object.
9. Return to a safe height.

The provided implementation is deliberately conservative and requires explicit `--execute`.
