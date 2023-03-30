import typing

from commands2 import Command, Subsystem

from constants.GameConstants import GamePieceType
from controllers.operator import OperatorController
from subsystems.Pickup.PickupSubsystem import PickupSubsystem


class PickupCommand(Command):
    def __init__(
        self,
        pickup: PickupSubsystem,
        controller: OperatorController,
        getGamePieceSelected: typing.Callable[[], GamePieceType],
    ) -> None:
        super().__init__()

        self.controller = controller
        self.pickup = pickup
        self.getGamePieceSelected = getGamePieceSelected

        self.stopPickupOnLimitSwitchWhileTriggerHeld = False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self.pickup}

    def execute(self) -> None:
        if not self.controller.isConnected():
            return

        # read axes and set speed depending on the game piece selected.
        # if the limit switch is hit while the cube is selected, stop motion
        releaseSpeed = self.controller.getPickupReleaseSpeed()
        intakeSpeed = self.controller.getPickupIntakeSpeed()
        speed = releaseSpeed + intakeSpeed

        # if the speed is 0, don't let the intake move.
        # Superior to brake mode, this is to prevent the intake from dropping a cone
        if speed == 0:
            self.pickup.holdPosition()
            return

        # if self.stopPickupOnLimitSwitchWhileTriggerHeld:
        #     if speed == 0:
        #         self.stopPickupOnLimitSwitchWhileTriggerHeld = False
        #     self.pickup.set(0)
        #     return

        match self.getGamePieceSelected():
            case GamePieceType.kEmpty:
                # speed = 0
                pass
            case GamePieceType.kCube:
                pass
                # if (
                #     self.pickup.isCubeLimitSwitchHit()
                #     and not self.pickup.getLimitSwitchHitChecked()
                # ):
                #     speed = 0
                #     self.stopPickupOnLimitSwitchWhileTriggerHeld = True
                #     self.pickup.setLimitSwitchHitChecked(True)
                # else:
                #     self.pickup.setLimitSwitchHitChecked(False)
            case GamePieceType.kCone:
                speed = -speed

        self.pickup.set(speed)

    def isFinished(self) -> bool:
        return False
