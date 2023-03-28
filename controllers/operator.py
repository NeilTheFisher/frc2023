from commands2.button import CommandXboxController
from constants import Constants
from utils.utils import dz


class OperatorController:
    _controller = CommandXboxController(Constants.operator_controller_id)

    def isConnected(self):
        return self._controller.isConnected()

    def getTopGrid(self):
        return self._controller.Y()

    def getMiddleGrid(self):
        return self._controller.B()

    def getBottomGrid(self):
        return self._controller.A()

    def getFloorPickup(self):
        return self._controller.POVDown()

    def getStowClaw(self):
        return self._controller.POVLeft()

    def getUpperFeedStation(self):
        return self._controller.POVUp()

    def getConeSelected(self):
        return self._controller.leftBumper()

    def getCubeSelected(self):
        return self._controller.rightBumper()

    def getEmptySelected(self):
        # return self._controller.leftBumper().and_(self._controller.rightBumper()) # TODO try this
        return self._controller.POVRight()

    def getClawRotation(self):
        return dz(self._controller.getLeftY())

    def getArmRotation(self):
        return -dz(self._controller.getRightY())

    def getZeroEncoderPosition(self):
        return self._controller.X()

    def getPickupIntakeSpeed(self):
        return self._controller.getRightTriggerAxis()

    def getPickupReleaseSpeed(self):
        return -self._controller.getLeftTriggerAxis()
