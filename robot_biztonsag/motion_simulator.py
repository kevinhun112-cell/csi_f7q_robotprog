"""Publish simulated forward velocity commands and front obstacle range."""

import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Range


class MotionSimulator(Node):
    """Generate a changing obstacle distance and a desired forward velocity."""

    def __init__(self) -> None:
        super().__init__('motion_simulator')
        self.declare_parameter('publish_rate_hz', 2.0)
        rate_hz = max(0.1, float(self.get_parameter('publish_rate_hz').value))
        self.range_publisher = self.create_publisher(Range, '/robot/front_range', 10)
        self.command_publisher = self.create_publisher(
            Twist, '/robot/desired_cmd_vel', 10
        )
        self.step = 0
        self.timer = self.create_timer(1.0 / rate_hz, self.publish_sample)
        self.get_logger().info(
            f'Szimulalt mozgas elindult ({rate_hz:.1f} Hz); '
            'topicok: /robot/front_range, /robot/desired_cmd_vel'
        )

    def publish_sample(self) -> None:
        """Publish one range measurement and one desired velocity command."""
        t = float(self.step)
        distance_m = 1.80 + 1.35 * math.sin(t * 0.13)
        desired_speed = 0.65 + 0.15 * math.sin(t * 0.07)
        stamp = self.get_clock().now().to_msg()

        range_msg = Range()
        range_msg.header.stamp = stamp
        range_msg.header.frame_id = 'front_range_sensor'
        range_msg.radiation_type = Range.ULTRASOUND
        range_msg.field_of_view = 0.26
        range_msg.min_range = 0.10
        range_msg.max_range = 4.00
        range_msg.range = distance_m
        self.range_publisher.publish(range_msg)

        command = Twist()
        command.linear.x = desired_speed
        command.angular.z = 0.12 * math.sin(t * 0.05)
        self.command_publisher.publish(command)

        self.get_logger().info(
            f'Szimulalt adat: akadaly={distance_m:.2f} m, '
            f'kert eloresebesseg={desired_speed:.2f} m/s'
        )
        self.step += 1


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MotionSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
