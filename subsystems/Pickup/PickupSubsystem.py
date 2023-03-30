from constants.PickupConstants import PickupConstants
import rev

from commands2 import Subsystem
import wpilib

from controllers.operator import OperatorController


class PickupSubsystem(Subsystem):
    def __init__(self, operatorController: OperatorController) -> None:
        super().__init__()

        self.controller = operatorController

        self.pickupMotor = rev.CANSparkMax(
            PickupConstants.kCANId, rev.CANSparkMax.MotorType.kBrushless
        )
        self.pickupMotor.restoreFactoryDefaults()
        self.pickupMotor.setSmartCurrentLimit(PickupConstants.currentLimit)
        self.pickupMotor.setSecondaryCurrentLimit(PickupConstants.secondaryCurrentLimit)
        self.pickupPID = self.pickupMotor.getPIDController()
        self.pickupPID.setP(PickupConstants.kP)
        self.pickupPID.setI(PickupConstants.kI)
        self.pickupPID.setD(PickupConstants.kD)
        self.pickupMotor.burnFlash()

        self.cubeLimitSwitch = wpilib.DigitalInput(0)

        self.limitSwitchHitChecked = False

    def holdPosition(self):
        self.pickupPID.setReference(0, rev.CANSparkMax.ControlType.kVelocity)

    def isCubeLimitSwitchHit(self):
        return self.cubeLimitSwitch.get()

    def getLimitSwitchHitChecked(self):
        return self.limitSwitchHitChecked

    def setLimitSwitchHitChecked(self, checked=True):
        self.limitSwitchHitChecked = checked

    def set(self, speed: float):
        self.pickupMotor.set(speed)
