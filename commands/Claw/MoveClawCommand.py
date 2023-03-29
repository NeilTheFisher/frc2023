import typing

from commands2 import Command, Subsystem
from wpimath.filter import SlewRateLimiter

from constants.ArmConstants import ArmConstants
from controllers.operator import OperatorController
from utils.utils import sgn

if typing.TYPE_CHECKING:
    from subsystems.Arm.ArmAssemblySubsystem import ArmAssemblySubsystem


class MoveClawCommand(Command):
    """Allows operator to move the arm and claw manually using controller axes."""

    def __init__(
        self, armSubsystem: "ArmAssemblySubsystem", controller: OperatorController
    ):
        super().__init__()

        self.armSubsystem = armSubsystem
        self.controller = controller

        self.armLimiter = SlewRateLimiter(ArmConstants.Arm.Manual.maxAnglePerSecond)
        self.clawLimiter = SlewRateLimiter(ArmConstants.Claw.Manual.maxAnglePerSecond)

        self.lastArmAxis = 0
        self.lastClawAxis = 0

    def initialize(self) -> None:
        pass

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self.armSubsystem}

    def execute(self) -> None:
        if self.controller.isConnected():
            armSpeed = self.controller.getArmRotation() * ArmConstants.Arm.speedScale
            if armSpeed > 0:
                self.armSubsystem.stopHoldArmPosition()
                self.armSubsystem.arm.armMotor.set(armSpeed)
            clawSpeed = self.controller.getClawRotation() * ArmConstants.Claw.speedScale
            if clawSpeed > 0:
                self.armSubsystem.stopHoldClawPosition()
                self.armSubsystem.claw.armMotor.set(clawSpeed)

            # armAxis = self.controller.getArmRotation()
            # if armAxis == 0 or sgn(self.lastArmAxis) != sgn(armAxis):
            #     self.armLimiter.reset(0)
            # armOmega = self.armLimiter.calculate(
            #     armAxis * ArmConstants.Arm.Manual.omegaScale
            # )
            # self.lastArmAxis = armAxis

            # clawAxis = self.controller.getClawRotation()
            # if clawAxis == 0 or sgn(self.lastClawAxis) != sgn(clawAxis):
            #     self.clawLimiter.reset(0)
            # clawOmega = self.clawLimiter.calculate(
            #     clawAxis * ArmConstants.Claw.Manual.omegaScale
            # )
            # self.lastClawAxis = clawAxis

            # # print("armOmega:", armOmega, "clawOmega:", clawOmega)

            # self.armSubsystem.arm.addAngle(armOmega)
            # self.armSubsystem.claw.addAngle(clawOmega)

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False
