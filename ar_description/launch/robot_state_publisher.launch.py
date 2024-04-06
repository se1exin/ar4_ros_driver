import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    robot_description_raw = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("ar_description"), "urdf", "ar.urdf.xacro"]
            ),
            " ",
            "name:=ar"
        ]
    )

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}] # add other parameters here if required
    )


    # Run the node
    return LaunchDescription([
        node_robot_state_publisher
    ])