import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    carpeta_tb3 = get_package_share_directory('turtlebot3_gazebo')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(carpeta_tb3, 'launch', 'empty_world.launch.py')
        )
    )

    mi_nodo = Node(
        package='g13_prii3_move_turtlebot',
        executable='draw_number',
        output='screen',
    )

    return LaunchDescription([gazebo, mi_nodo])