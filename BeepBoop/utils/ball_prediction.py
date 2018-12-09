from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from BeepBoop.bot_math.Vector3 import Vector3
from typing import List, Tuple


def get_ground_bounces(path: BallPrediction) -> List[Tuple[Vector3, float]]:
    bounces: List[Tuple[Vector3, float]] = []

    for i in range(1, path.num_slices):
        prev_ang_vel: Vector3 = Vector3(path.slices[i - 1].physics.angular_velocity)

        # Make sure it's never (0, 0, 0) to avoid ZeroDivisionError
        if prev_ang_vel == Vector3(0, 0, 0):
            prev_ang_vel_normalised: Vector3 = Vector3(1, 1, 1)
        else:
            prev_ang_vel_normalised: Vector3 = prev_ang_vel.normalised()

        current_slice = path.slices[i]
        current_ang_vel: Vector3 = Vector3(current_slice.physics.angular_velocity)

        # Make sure it's never (0, 0, 0) to avoid ZeroDivisionError
        if current_ang_vel == Vector3(0, 0, 0):
            current_ang_vel_normalised: Vector3 = Vector3(1, 1, 1)
        else:
            current_ang_vel_normalised: Vector3 = current_ang_vel.normalised()

        # Ball's angular velocity does not change in air; it only changes when bouncing.
        # Therefore, if the ball changes angular velocity between frames and the height is low, a bounce occurred.
        if prev_ang_vel_normalised != current_ang_vel_normalised and current_slice.physics.location.z < 125:
            bounces.append((Vector3(current_slice.physics.location), current_slice.game_seconds))

    return bounces
