import wpilib
import commands2
import commands2.cmd
import commands2.button
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import math
from input import Input
from selector import Selector

from .configBasedRobot import ConfigBaseCommandRobot
from subsystems.actuators.dumboArm import Arm


class Dumbo(ConfigBaseCommandRobot):
    robot_arm: Arm

    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        # Attempt assignments from subsystems and if something is empty, throw an exception
        try:
            self.robot_arm = self.subsystems["arm"]
            self.driveTrain = self.subsystems["drivetrain"]
        except:
            raise Exception(
                "ERROR! Wrong Config! Check ~/robotConfig to ensure you're using the correct robot config or correct robot. If it doubt, read the README.md"
            )
        self.driver_controller = commands2.button.CommandXboxController(0)
        self.mech_controller = commands2.button.CommandXboxController(1)
        self.configureButtonBindings()
        self.selector = Selector()
        self.tankDrive = TankDrive(
            Input.getStick(wpilib.XboxController.Axis.kLeftY, 0, True),
            Input.getStick(wpilib.XboxController.Axis.kRightY, 0, True),
            self.driveTrain,
        )
        self.arcadeDrive = ArcadeDrive(
            Input.getStick(wpilib.XboxController.Axis.kLeftY, 0, True),
            Input.getStick(wpilib.XboxController.Axis.kRightX, 0, False),
            self.driveTrain,
        )

        wpilib.SmartDashboard.putNumber(
            "set angle", self.robot_arm.getPostion() * math.pi / 180.0
        )

    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)

    def teleopPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber(
            "curr ang", self.robot_arm.getPostion() * math.pi / 180.0
        )
        if Input().getButton("BButton", self.mech_controller):
            self.selector.GetSelection(self.mech_controller)
        wpilib.SmartDashboard.putNumber("curr rad", self.robot_arm.getPostion())

        return super().teleopPeriodic()

    def testInit(self) -> None:
        wpilib.SmartDashboard.putNumber("ang", 180)

    def testPeriodic(self) -> None:
        # test code to trigger. Remove after arm mounted and tested
        self.robot_arm._getMeasurement()
        super().testPeriodic()

    def teleopExit(self) -> None:
        self.disablePIDSubsystems()
        return super().teleopExit()

    def moveArm(self, radians: float) -> None:
        self.robot_arm.setSetpoint(radians)
        self.robot_arm.enable()

    def moveArmDegrees(self, degrees: float) -> None:
        self.moveArm(math.radians(degrees))

    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""
        self.robot_arm.disable()

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        # Move the arm to 2 radians above horizontal when the 'A' button is pressed.
        self.mech_controller.A().whileTrue(
            commands2.cmd.runOnce(lambda: self.trackAngle(), [self.robot_arm])
        )

        self.mech_controller.X().onTrue(
            commands2.cmd.runOnce(lambda: self.moveArmDegrees(0), [self.robot_arm])
        )

        # Move the arm to neutral position when the 'B' button is pressed
        self.mech_controller.start().onTrue(
            commands2.cmd.runOnce(lambda: self.moveArmDegrees(180), [self.robot_arm])
        )
        self.mech_controller.Y().onTrue(
            commands2.cmd.runOnce(lambda: self.moveArmDegrees(90), [self.robot_arm])
        )

        # Disable the arm controller when Y is pressed
        self.mech_controller.back().onTrue(
            commands2.cmd.runOnce(lambda: self.disablePIDSubsystems(), [self.robot_arm])
        )

    def trackAngle(self):
        self.moveArmDegrees(
            wpilib.SmartDashboard.getNumber("set angle", self.robot_arm.getPostion())
        )

    def disableArm(self):
        print("disabling")
        self.robot_arm.disable()
