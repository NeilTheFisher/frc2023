from commands2 import SubsystemBase

from constants.ArmConstants import ArmConstants
from controllers.operator import OperatorController
from subsystems.Arm.ArmSubsystem import ArmSubsystem


class ArmAssemblySubsystem(SubsystemBase):
    def __init__(self, operatorController: OperatorController) -> None:
        super().__init__()

        self.operatorController = operatorController

        self.arm = ArmSubsystem(ArmConstants.Arm)
        self.claw = ArmSubsystem(ArmConstants.Claw)

        self._holdArmPositionFlag = False
        self._holdClawPositionFlag = False

    # def isManuallyControlled(self):
    #     # instead of imperatively checking if the operator controller is connected, there could be a method/property
    #     # on the default command get a callback to check if it is being manually controlled.
    #     return self.operatorController.isConnected() and (
    #         self.operatorController.getArmRotation() != 0
    #         or self.operatorController.getClawRotation() != 0
    #     )

    lastArmPos = 0
    lastClawPos = 0

    def periodic(self) -> None:
        # if there is manual control, cancel the current command to run the default command
        # if self.isManuallyControlled():
        #     # let manual control override the current command
        #     currentCommand = self.getCurrentCommand()
        #     if self.getDefaultCommand() != currentCommand:
        #         currentCommand.cancel()

        armPos = self.arm.getAngle()
        clawPos = self.claw.getAngle()
        if armPos != self.lastArmPos:
            print("Arm angle:", armPos)
        if clawPos != self.lastClawPos:
            print("Claw angle:", clawPos)

        self.lastArmPos = armPos
        self.lastClawPos = clawPos

    # def getClawAngle(self):
    #     """Returns the angle of the claw"""
    #     return self.claw.getAngle()

    # def getWorldClawAngle(self):
    #     """Returns the angle of the claw added to the angle of the arm to get the total angle of the claw"""
    #     return (self.getClawAngle() + self.getArmAngle()) % 360

    # def setClawAngle(self, angle: float):
    #     """Sets the angle of the claw to the given angle relative to the arm"""
    #     self.claw.setAngle(angle)

    # def getArmAngle(self):
    #     """Returns the angle of the arm"""
    #     return self.arm.getAngle()

    # def setArmAngle(self, angle: float):
    #     """Sets the angle of the arm to the given angle"""
    #     self.arm.setAngle(angle)

    def setArmAndClawAngle(self, armAngle: float, clawAngle: float):
        """
        Sets the angle of the arm and claw to the given angles in space
        Up=180
        Front=90
        Down=0
        Back=270
        """
        self.arm.setAngle(armAngle)
        # these are subtracted to get the actual ending angle for the claw to be set to.
        # self.claw.setAngle(worldClawAngle - worldArmAngle)
        self.claw.setAngle(clawAngle)

    def atSetpoint(self):
        """Returns true if the arm and claw are at their setpoints"""
        return self.arm.atSetpoint() and self.claw.atSetpoint()

    def resetArmAndClaw(self):
        self.arm.setPosition(self.arm.initialPosition)
        self.claw.setPosition(self.claw.initialPosition)
