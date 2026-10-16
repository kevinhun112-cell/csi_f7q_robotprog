"""Launch the motion simulator and the obstacle safety controller."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='robot_biztonsag',
            executable='motion_simulator',
            name='motion_simulator',
            output='screen',
            emulate_tty=True,
            parameters=[{'publish_rate_hz': 2.0}],
        ),
        Node(
            package='robot_biztonsag',
            executable='safety_controller',
            name='safety_controller',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'stop_distance_m': 0.65, 'full_speed_distance_m': 1.50}
            ],
        ),
    ])
