from commands.Auto.PPAutoSelector import PPAutonomousSelector
from commands.Claw.ArmCommand import ArmCommand
from commands2 import InstantCommand
from constants.ArmConstants import ArmConstants
from photonvision import PhotonCamera

from commands.Auto.PPAutonomousCommand import PPAutonomousCommand
from commands.Claw.ManualMoveClawCommand import ManualMoveClawCommand
from commands.Pickup.PickupCommand import PickupCommand
from commands.SwerveCommand import SwerveCommand
from constants.GameConstants import GamePieceType
from controllers.operator import OperatorController
from controllers.pilot import PilotController
from subsystems.Arm.ArmAssemblySubsystem import ArmAssemblySubsystem
from subsystems.Pickup.PickupSubsystem import PickupSubsystem
from subsystems.Swerve.SwerveSubsystem import SwerveSubsystem


class RobotContainer:
    field_oriented = True

    photon_camera = PhotonCamera("photonvision")

    selectedGamePiece = GamePieceType.kEmpty

    def __init__(self) -> None:
        self.pilotController = PilotController()
        self.operatorController = OperatorController()

        self.swerveSubsystem = SwerveSubsystem()
        self.armAssemblySubsystem = ArmAssemblySubsystem(self.operatorController)
        self.pickup = PickupSubsystem(self.operatorController)

        self.autoSelector = PPAutonomousSelector(
            self.swerveSubsystem, self.armAssemblySubsystem
        )

        self.configureButtonBindings()

        # self.light_strip = LightStrip(Constants.light_strip_pwm_port)
        # self.light_strip.setRainbowSlow()

    def robotPeriodic(self):
        # self.light_strip.update()
        pass

    @staticmethod
    def getSelectedGamePiece():
        return RobotContainer.selectedGamePiece

    @staticmethod
    def setSelectedGamePiece(gamePiece: GamePieceType):
        print("Selected game piece: " + gamePiece.name)
        RobotContainer.selectedGamePiece = gamePiece

    def get_angle(self):
        return self.swerveSubsystem.getAngle()

    def getAutonomousCommand(self):
        return self.autoSelector.getSelectedAutonomousCommand()

    def vision_track(self):
        if self.photon_camera.hasTargets():
            target = self.photon_camera.getLatestResult().getBestTarget()
            transform_to_target = target.getBestCameraToTarget()
            # TODO

    def configureButtonBindings(self) -> None:
        c1Connected = self.pilotController.isConnected()
        c2Connected = self.operatorController.isConnected()
        if c1Connected:
            self.setupSwerve()
        else:
            self.pilotController.onceConnected(self.setupSwerve)
        if c2Connected:
            self.setupArm()
            self.setupPickup()
            self.configureGeneralOperatorButtonBindings()
        else:

            def onConnected():
                self.setupArm()
                self.setupPickup()
                self.configureGeneralOperatorButtonBindings()

            self.operatorController.onceConnected(onConnected)

    def configureGeneralOperatorButtonBindings(self) -> None:
        self.operatorController.getConeSelected().onTrue(
            InstantCommand(lambda: self.setSelectedGamePiece(GamePieceType.kCone))
        )
        self.operatorController.getCubeSelected().onTrue(
            InstantCommand(lambda: self.setSelectedGamePiece(GamePieceType.kCube))
        )
        self.operatorController.getEmptySelected().onTrue(
            InstantCommand(lambda: self.setSelectedGamePiece(GamePieceType.kEmpty))
        )

    def setupSwerve(self) -> None:
        self.swerveSubsystem.setDefaultCommand(
            SwerveCommand(
                self.swerveSubsystem,
                self.pilotController,
                self.getFieldOriented,
            )
        )

        self.configureSwerveButtonBindings()

    def getFieldOriented(self) -> bool:
        return self.field_oriented

    def toggleFieldOriented(self) -> None:
        self.field_oriented = not self.field_oriented
        print("Field oriented: ", self.field_oriented)

    def configureSwerveButtonBindings(self) -> None:
        self.pilotController.fieldOrientedBtn().onTrue(
            InstantCommand(self.toggleFieldOriented)
        )
        self.pilotController.resetGyroBtn().onTrue(
            InstantCommand(self.swerveSubsystem.resetGyro)
        )

    def setupArm(self):
        self.armAssemblySubsystem.setDefaultCommand(
            ManualMoveClawCommand(self.armAssemblySubsystem, self.operatorController)
        )

        self.configureArmButtonBindings()

    def configureArmButtonBindings(self) -> None:
        self.operatorController.getResetArmAndClawPosition().onTrue(
            InstantCommand(self.armAssemblySubsystem.resetArmAndClaw)
        )
        self.operatorController.getFloorPickup().whileTrue(
            ArmCommand(
                self.armAssemblySubsystem,
                self.getSelectedGamePiece,
                ArmConstants.AngleType.kFloor,
            )
        )
        self.operatorController.getUpperFeedStation().whileTrue(
            ArmCommand(
                self.armAssemblySubsystem,
                self.getSelectedGamePiece,
                ArmConstants.AngleType.kUpperFeedStation,
            )
        )
        self.operatorController.getL1Grid().whileTrue(
            ArmCommand(
                self.armAssemblySubsystem,
                self.getSelectedGamePiece,
                ArmConstants.AngleType.kGridL1,
            )
        )
        self.operatorController.getL2Grid().whileTrue(
            ArmCommand(
                self.armAssemblySubsystem,
                self.getSelectedGamePiece,
                ArmConstants.AngleType.kGridL2,
            )
        )
        self.operatorController.getL3Grid().whileTrue(
            ArmCommand(
                self.armAssemblySubsystem,
                self.getSelectedGamePiece,
                ArmConstants.AngleType.kGridL3,
            )
        )

    def setupPickup(self):
        self.pickup.setDefaultCommand(
            PickupCommand(
                self.pickup, self.operatorController, self.getSelectedGamePiece
            )
        )

    """ def getAutonomousCommand(self):
        trajectory_config = TrajectoryConfig(
            SwerveConstants.kDriveMaxMetersPerSecond,
            SwerveConstants.kDriveMaxAccelerationMetersPerSecond,
        )
        trajectory_config.setKinematics(SwerveConstants.kDriveKinematics)

        trajectory = TrajectoryGenerator.generateTrajectory(
            Pose2d(0, 0, Rotation2d(0)),
            [Translation2d(1, 1), Translation2d(2, -1)],
            Pose2d(3, 0, Rotation2d(0)),
            trajectory_config,
        )

        # TODO make these constants in constants.py
        x_pid = PIDController(0.5, 0, 0, period=Constants.period)
        y_pid = PIDController(0.5, 0, 0, period=Constants.period)
        theta_pid = ProfiledPIDControllerRadians(
            0.5,
            0,
            0,
            TrapezoidProfileRadians.Constraints(3, 3),
            period=Constants.period,
        )
        theta_pid.enableContinuousInput(-180, 180)

        swerve_command = Swerve4ControllerCommand(
            trajectory,
            self.swerveSubsystem.getPose,
            SwerveConstants.kDriveKinematics,
            x_pid,
            y_pid,
            theta_pid,
            self.swerveSubsystem.setModuleStates,
            [self.swerveSubsystem],
        )

        return SequentialCommandGroup(
            InstantCommand(self.swerveSubsystem.resetOdometer, trajectory.initialPose),
            swerve_command,
            InstantCommand(self.swerveSubsystem.stop),
        ) """
