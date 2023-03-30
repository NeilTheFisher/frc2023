import wpilib as wp
from commands2 import CommandScheduler
from ntcore import NetworkTableInstance

from ArmAnglesConfigurator import configureArmAnglePreferences
from constants.RobotConstants import RobotConstants
from RobotContainer import RobotContainer
from utils.utils import printAsync


class Robot(wp.TimedRobot):
    def __init__(self, period=RobotConstants.period) -> None:
        super().__init__(period)

    def robotInit(self) -> None:
        RobotConstants.isSimulation = self.isSimulation()

        # self.smartDashboard = NetworkTables.getTable("SmartDashboard")
        ntInstance = NetworkTableInstance.getDefault()
        self.smartDashboard = ntInstance.getTable("SmartDashboard")
        self.gyro_topic = self.smartDashboard.getDoubleTopic("Gyro Angle").publish()
        self.turner_topic = self.smartDashboard.getDoubleTopic("Turn Encoder").publish()
        # # create ps4 controller
        # self.controller = wp.PS4Controller(0)

        # # self.module_1 = SwerveModule()
        # self.turner = rev.CANSparkMax(3, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        # self.turner_encoder = self.turner.getAbsoluteEncoder(
        #     rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle
        # )

        self.robotContainer = RobotContainer()

        self.swerveAutoCommand = self.robotContainer.getAutonomousCommand()

    lastArmPos = 0.0

    def robotPeriodic(self) -> None:
        # arm angle calibration
        # armPos = self.robotContainer.armAssemblySubsystem.arm.armEncoder.getPosition()
        # if armPos != self.lastArmPos:
        #     print(
        #         "current arm pos:",
        #         armPos,
        #     )
        #     # self.robot_container.robotPeriodic()
        # self.lastArmPos = armPos

        self.gyro_topic.set(self.robotContainer.get_angle())

        self.turner_topic.set(
            # self.robot_container.swerve_subsystem.front_left.turn_encoder.getPosition()
            # % math.pi
            # * 2
            self.robotContainer.swerveSubsystem.front_left.getPosition().angle.degrees()
        )

        try:
            CommandScheduler.getInstance().run()
        except Exception as e:
            printAsync("Caught exception:", e)

    def autonomousInit(self) -> None:
        # auto_command = self.robot_container.getAutonomousCommand()
        # if auto_command is not None:
        #     auto_command.schedule()
        #     print("Auto command scheduled")
        # self.robot_container.autonomousInit()
        self.swerveAutoCommand = self.robotContainer.getAutonomousCommand()
        self.swerveAutoCommand.schedule()

    def autonomousExit(self) -> None:
        self.swerveAutoCommand.cancel()

    # def autonomousPeriodic(self) -> None:
    #     self.robot_container.autonomousPeriodic()

    # def teleopInit(self) -> None:
    #     self.robotContainer.teleopInit()

    # def teleopPeriodic(self) -> None:
    #     self.robot_container.teleopPeriodic()

    #     # TODO maybe stop the auto command here if executing the swerve drive command doesn't stop it.
    #     # There may not need to be any teleop code here if everything uses commands.
    #     # The commands are run using the command scheduler which is run in robotPeriodic.
    #     # The CommandScheduler automatically runs the appropriate code depending on the state of the competition (disabled, autonomous, teleoperated).
    #     pass


if __name__ == "__main__":
    wp.run(Robot)
