"""Unit tests for the pure safety calculation (no ROS installation needed)."""

import math
import unittest

from robot_biztonsag.safety_logic import calculate_safe_speed


class SafetyLogicTests(unittest.TestCase):
    def test_clear_path_preserves_speed(self):
        self.assertEqual(calculate_safe_speed(0.7, 2.0), (0.7, 'CLEAR'))

    def test_inside_stop_distance_stops_forward_motion(self):
        self.assertEqual(calculate_safe_speed(0.7, 0.5), (0.0, 'STOP'))

    def test_boundary_stops_forward_motion(self):
        self.assertEqual(calculate_safe_speed(0.7, 0.65), (0.0, 'STOP'))

    def test_slow_zone_scales_speed_linearly(self):
        speed, mode = calculate_safe_speed(0.8, 1.075)
        self.assertAlmostEqual(speed, 0.4)
        self.assertEqual(mode, 'SLOW')

    def test_reverse_motion_is_not_blocked_by_front_sensor(self):
        self.assertEqual(calculate_safe_speed(-0.3, 0.2), (-0.3, 'CLEAR'))

    def test_invalid_distance_fails_safe_for_forward_motion(self):
        self.assertEqual(calculate_safe_speed(0.6, math.nan), (0.0, 'STOP'))

    def test_invalid_thresholds_raise(self):
        with self.assertRaises(ValueError):
            calculate_safe_speed(0.5, 2.0, 1.5, 0.6)


if __name__ == '__main__':
    unittest.main()
