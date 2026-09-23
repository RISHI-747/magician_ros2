from setuptools import find_packages, setup

package_name = "rishi_dobot_tools"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/rishi_dobot_tools.launch.py"]),
    ],
    install_requires=["setuptools", "numpy"],
    zip_safe=True,
    description="Additional Dobot Magician ROS 2 tools and experiments.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "connection_check = rishi_dobot_tools.connection_check:main",
            "pose_monitor = rishi_dobot_tools.pose_monitor:main",
            "record_pose = rishi_dobot_tools.record_pose:main",
            "ptp_cli = rishi_dobot_tools.ptp_cli:main",
            "gripper_cli = rishi_dobot_tools.gripper_cli:main",
            "suction_cli = rishi_dobot_tools.suction_cli:main",
            "pick_place_demo = rishi_dobot_tools.pick_place_demo:main",
        ],
    },
)
