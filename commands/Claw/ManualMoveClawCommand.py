import typing

from commands2 import Command, Subsystem

from constants.ArmConstants import ArmConstants
from controllers.operator import OperatorController
from utils.utils import calcAxisSpeedWithCurvatureAndDeadzone

if typing.TYPE_CHECKING:
    from subsystems.Arm.ArmAssemblySubsystem import ArmAssemblySubsystem


class ManualMoveClawCommand(Command):
    """Allows operator to move the arm and claw manually using controller axes."""

    def __init__(
        self, armAssembly: "ArmAssemblySubsystem", controller: OperatorController
    ):
        super().__init__()

        self.armAssembly = armAssembly
        self.controller = controller

        self.lastArmAngle: float | None = None
        self.lastClawAngle: float | None = None

    def initialize(self) -> None:
        self.lastArmAngle = None
        self.lastClawAngle = None

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self.armAssembly}

    def execute(self) -> None:
        if not self.controller.isConnected():
            return

        armSpeed = self.controller.getArmRotation()
        armSpeed = calcAxisSpeedWithCurvatureAndDeadzone(armSpeed, 2, 0, 0)
        armSpeed *= ArmConstants.Arm.speedScale
        if abs(armSpeed) > 0:
            self.armAssembly.arm.stopHoldingPosition()
            self.armAssembly.arm.armMotor.set(armSpeed)
            self.armAssembly.arm.updateLastSetAngle()
        else:
            self.armAssembly.arm.startHoldingPosition()

        clawSpeed = self.controller.getClawRotation()
        clawSpeed = calcAxisSpeedWithCurvatureAndDeadzone(clawSpeed, 2, 0, 0)
        clawSpeed *= ArmConstants.Claw.speedScale
        if abs(clawSpeed) > 0:
            self.armAssembly.claw.stopHoldingPosition()
            self.armAssembly.claw.armMotor.set(clawSpeed)
            self.armAssembly.claw.updateLastSetAngle()
        else:
            self.armAssembly.claw.startHoldingPosition()

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False
