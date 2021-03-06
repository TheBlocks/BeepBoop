import math

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState

from .base_step import BaseStep
from beepboop import BeepBoop
from bot_math.Vector3 import Vector3
from utils.physics_object import PhysicsObject
from utils.steering import gosling_steering


class EscapeGoalStep(BaseStep):
    def __init__(self, agent: BeepBoop):
        super().__init__(agent)

    """Drives towards the ball's first ground bounce and tries to arrive there at the same time as the bounce."""
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)
        goal_location = Vector3(self.agent.get_field_info().goals[self.agent.team].location)
        goal_location.y = abs(goal_location.y) * math.copysign(1, bot.location.y)

        controller: SimpleControllerState = SimpleControllerState()
        controller.steer = gosling_steering(bot.location, bot.rotation.z, goal_location)
        controller.throttle = 1

        return controller
