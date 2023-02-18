import wpilib
import commands2
import commands2.cmd
import commands2.button
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath
import math

import utils.configMapper
from .configBasedRobot import ConfigBaseCommandRobot
from subsystems.actuators.dumboArm import Arm

class Dumbo(ConfigBaseCommandRobot):
    robot_arm: Arm
    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)
        self.robot_arm = self.subsystems["arm"]
        self.driver_controller = commands2.button.CommandXboxController(0)
        #controller = commands2.button.CommandXboxController(0)
        #controller.A().onTrue(
        #    commands2.cmd.run(lambda: self.moveArm(2), [self.robot_arm])
        #)

        self.configureButtonBindings()



    def teleopInit(self) -> None:
        #ang = wpilib.SmartDashboard.getNumber("ang", 180) * math.pi / 180.0
        #commands2.cmd.run(self.moveArm(ang), [self.robot_arm])
        #curr_pos = self.robot_arm.getPostion()
        #print(f"Arm at {curr_pos} / {curr_pos * 180.0 / math.pi}")
        #self.moveArmDegrees(ang)
        #self.driveTrain.setDefaultCommand(self.tankDrive)
        pass

    def testInit(self) -> None:
        wpilib.SmartDashboard.putNumber("ang", 180)
    
    def testPeriodic(self) -> None:
        ang = wpilib.SmartDashboard.getNumber("ang", 180) * math.pi / 180.0
        #commands2.cmd.run(self.moveArm(ang), [self.robot_arm])
        #curr_pos = self.robot_arm.getPostion()
        #print(f"Arm at {curr_pos} / {curr_pos * 180.0 / math.pi}")
        self.moveArmDegrees(ang)
        super().testPeriodic()

    def teleopExit(self) -> None:
        self.disablePIDSubsystems()
        return super().teleopExit()

    def moveArm(self, radians: float) -> None:
        self.robot_arm.setGoal(radians)
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
        self.driver_controller.A().onTrue(
            commands2.cmd.run(lambda: self.moveArmDegrees(0), [self.robot_arm])
        )

        self.driver_controller.X().onTrue(
            commands2.cmd.run(lambda: self.moveArmDegrees(90), [self.robot_arm])
        )

        # Move the arm to neutral position when the 'B' button is pressed
        self.driver_controller.B().onTrue(
            commands2.cmd.run(
                lambda: self.moveArmDegrees(180), [self.robot_arm]
            )
        )

        # Disable the arm controller when Y is pressed
        self.driver_controller.Y().onTrue(
            commands2.cmd.runOnce(lambda: self.disableArm())
        )

    def disableArm(self):
        print("disabling")
        self.robot_arm.disable()