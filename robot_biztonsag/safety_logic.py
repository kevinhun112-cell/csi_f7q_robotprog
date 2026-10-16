"""ROS-independent logic for limiting forward speed near an obstacle."""

import math
from typing import Tuple


def calculate_safe_speed(
    desired_speed: float,
    obstacle_distance: float,
    stop_distance: float = 0.65,
    full_speed_distance: float = 1.50,
) -> Tuple[float, str]:
    """Return a safe forward speed and mode: STOP, SLOW, or CLEAR.

    Forward motion is stopped at or below stop_distance. Between the stop and
    full-speed distances, speed is scaled linearly. Reverse motion is unchanged
    because the simulated range sensor points forward. Invalid distance
    readings fail safe by stopping forward motion.
    """
    if not math.isfinite(desired_speed):
        desired_speed = 0.0
    if not math.isfinite(obstacle_distance) or obstacle_distance < 0.0:
        return (0.0 if desired_speed > 0.0 else desired_speed), 'STOP'
    if not (0.0 < stop_distance < full_speed_distance):
        raise ValueError('A hatarertekekre 0 < stop_distance < full_speed_distance kell.')

    if desired_speed <= 0.0:
        return desired_speed, 'CLEAR'
    if obstacle_distance <= stop_distance:
        return 0.0, 'STOP'
    if obstacle_distance < full_speed_distance:
        ratio = (obstacle_distance - stop_distance) / (
            full_speed_distance - stop_distance
        )
        return desired_speed * ratio, 'SLOW'
    return desired_speed, 'CLEAR'
