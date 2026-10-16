"""Limit forward velocity when the obstacle range becomes unsafe."""

from typing import Optional

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import String

from robot_biztonsag.safety_logic import calculate_safe_speed


class SafetyController(Node):
    """Combine desired velocity and obstacle range into a safe command."""

    def __init__(self) -> None:
        super().__init__('safety_controller')
        self.declare_parameter('stop_distance_m', 0.65)
        self.declare_parameter('full_speed_distance_m', 1.50)
        self.stop_distance = float(self.get_parameter('stop_distance_m').value)
        self.full_speed_distance = float(
            self.get_parameter('full_speed_distance_m').value
        )
        if not (0.0 < self.stop_distance < self.full_speed_distance):
            raise ValueError('A parameterekre 0 < stop_distance_m < full_speed_distance_m kell.')

        self.latest_distance: Optional[float] = None
        self.latest_command: Optional[Twist] = None
        self.last_mode: Optional[str] = None

        self.create_subscription(
            Range, '/robot/front_range', self.range_callback, 10
        )
        self.create_subscription(
            Twist, '/robot/desired_cmd_vel', self.command_callback, 10
        )
        self.safe_command_publisher = self.create_publisher(
            Twist, '/robot/safe_cmd_vel', 10
        )
        self.status_publisher = self.create_publisher(
            String, '/robot/safety_status', 10
        )
        self.get_logger().info(
            'Biztonsagi vezerlo elindult; '
            f'leallasi tavolsag={self.stop_distance:.2f} m, '
            f'teljes sebesseg tavolsaga={self.full_speed_distance:.2f} m'
        )

    def range_callback(self, message: Range) -> None:
        self.latest_distance = float(message.range)
        self.apply_safety_rule()

    def command_callback(self, message: Twist) -> None:
        self.latest_command = message
        self.apply_safety_rule()

    def apply_safety_rule(self) -> None:
        """Publish safe motion after at least one message from each input."""
        if self.latest_distance is None or self.latest_command is None:
            return

        safe_speed, mode = calculate_safe_speed(
            desired_speed=self.latest_command.linear.x,
            obstacle_distance=self.latest_distance,
            stop_distance=self.stop_distance,
            full_speed_distance=self.full_speed_distance,
        )
        safe = Twist()
        safe.linear.x = safe_speed
        safe.linear.y = self.latest_command.linear.y
        safe.linear.z = self.latest_command.linear.z
        safe.angular.x = self.latest_command.angular.x
        safe.angular.y = self.latest_command.angular.y
        safe.angular.z = self.latest_command.angular.z
        if mode == 'STOP':
            safe.linear.x = 0.0
        self.safe_command_publisher.publish(safe)

        if mode != self.last_mode:
            distance_text = f'{self.latest_distance:.2f} m'
            status_text = (
                f'{mode}: akadaly {distance_text}; '
                f'kert sebesseg={self.latest_command.linear.x:.2f} m/s, '
                f'biztonsagos sebesseg={safe.linear.x:.2f} m/s'
            )
            message = String()
            message.data = status_text
            self.status_publisher.publish(message)
            if mode == 'STOP':
                self.get_logger().warning(status_text)
            else:
                self.get_logger().info(status_text)
            self.last_mode = mode


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SafetyController()
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
