from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="rishi_dobot_tools",
            executable="pose_monitor",
            output="screen",
        ),
    ])
