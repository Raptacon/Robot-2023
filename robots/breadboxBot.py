import wpilib
import commands2
import commands2.cmd
import commands2.button
from commands.tankDrive import TankDrive
import math
from input import Input
from commands.balance import Balance
from commands.breadbox import armCommands
from selector import Selector
from wpilib import cameraserver

from .configBasedRobot import ConfigBaseCommandRobot
from subsystems.actuators.breadboxArmRotation import ArmRotation
from subsystems.actuators.breadboxArmController import ArmController
from subsystems.arm.grader import Grabber

class Breadbox(ConfigBaseCommandRobot):
    balanceing = False
    robot_arm_rotation: ArmRotation
    robot_Grabber: Grabber
    robot_arm_controller: ArmController
    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        # Attempt assignments from subsystems and if something is empty, throw an exception
        try:
            self.robot_arm_rotation = self.subsystems["armRotation"]
            self.driveTrain = self.subsystems["drivetrain"]
            self.robot_Grabber = self.subsystems["grabber"]
            self.robot_arm_controller = self.subsystems["armController"]
            #TODO fix this way this setter works
            self.robot_arm_controller.setArmRotationSubsystem(self.robot_arm_rotation)
            #self.robot_arm_controller.setArmExtensionSubsystem(self.robot_arm_extension)

            cameraserver.CameraServer.launch()

        except:
            raise Exception(
                "ERROR! Wrong Config! Check ~/robotConfig to ensure you're using the correct robot config or correct robot. If it doubt, read the README.md"
            )

        wpilib.SmartDashboard.putNumber(
            "set angle", self.robot_arm_rotation.getPostion() * math.pi / 180.0
        )

        #create auto distance numbers if do not exist
        # if wpilib.SmartDashboard.getNumber("Auto Distance 1", -1) == -1:
        wpilib.SmartDashboard.putNumber("Auto Distance 1", 8)
        wpilib.SmartDashboard.putNumber("Auto Distance 2", 8)


    def teleopInit(self) -> None:
        self.driver_controller = commands2.button.CommandXboxController(0)
        self.mech_controller = commands2.button.CommandXboxController(1)
        self.mech_controller_hid = commands2.button.CommandGenericHID(1)
        self.configureButtonBindings()
        self.selector = Selector()

        self.tankDrive = TankDrive(
            Input.getStick(wpilib.XboxController.Axis.kLeftY, 0, True),
            Input.getStick(wpilib.XboxController.Axis.kRightY, 0, True),
            lambda: self.getCreeperMode(),
            self.driveTrain,
        )

        wpilib.SmartDashboard.putNumber(
            "set angle", self.robot_arm_rotation.getPostion() * math.pi / 180.0
        )
        wpilib.SmartDashboard.putNumber(
            "CreeperMode Multiplier", 0.5
        )

        self.driveTrain = self.subsystems["drivetrain"]
        # self.balance = Balance(Input.getButton("XButton", self.XboxController), self.driveTrain)
        self.balance = Balance(Input().getButton("XButton", self.driver_controller), self.driveTrain)
        self.balanceDrive = TankDrive(self.balance.dobalance,self.balance.dobalance, lambda: self.getCreeperMode(), self.driveTrain)


    def teleopPeriodic(self) -> None:
        # if Input.getButton("XButton", self.XboxController):
        if self.driver_controller.getAButton():
            if (not self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.balanceDrive)
            self.balanceing = True
            self.balance.execute()
        else:
            if(self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.tankDrive)
            self.balanceing = False

        wpilib.SmartDashboard.putNumber(
            "curr ang", self.robot_arm_rotation.getPostion() * math.pi / 180.0
        )
        if Input().getButton("RightTrigger", self.driver_controller) > 0.2:
            self.creeperMode = True
        else:
            self.creeperMode = False

        if self.mech_controller.getRightTriggerAxis() > 0.2:
            self.robot_Grabber.useOutputCones(self.mech_controller.getRightTriggerAxis())
        elif self.mech_controller.getRightBumper():
            self.robot_Grabber.useIntakehCones(self.mech_controller.getRightBumper())
        elif self.mech_controller.getLeftTriggerAxis() > 0.2:
            self.robot_Grabber.useOutputCubes(self.mech_controller.getLeftTriggerAxis())
        elif self.mech_controller.getLeftBumper():
            self.robot_Grabber.useIntakeCubes(self.mech_controller.getLeftBumper())
        if Input().getButton("RightTrigger", self.driver_controller):
            self.creeperMode = True
        else:
            self.creeperMode = False

        if Input().getButton("RightTrigger", self.mech_controller) != 0:
            self.robot_Grabber.useOutputCones(Input().getButton("RightTrigger", self.mech_controller))
        elif Input().getButton("RightBumper", self.mech_controller):
            self.robot_Grabber.useIntakehCones(Input().getButton("RightBumper", self.mech_controller))
        elif Input().getButton("LeftTrigger", self.mech_controller) != 0:
            self.robot_Grabber.useOutputCubes(Input().getButton("LeftTrigger", self.mech_controller))
        elif Input().getButton("LeftBumper", self.mech_controller):
            self.robot_Grabber.useIntakeCubes(Input().getButton("LeftBumper", self.mech_controller))
        else:
            self.robot_Grabber.stop()

        if Input().getButton("BButton", self.mech_controller):
            self.selector.GetSelection(self.mech_controller)
        wpilib.SmartDashboard.putNumber("curr rad", self.robot_arm_rotation.getPostion())

        self.robot_arm_rotation._getMeasurement()

        return super().teleopPeriodic()



    def testInit(self) -> None:
        wpilib.SmartDashboard.putNumber("ang", 180)

    def testPeriodic(self) -> None:
        # test code to trigger. Remove after arm mounted and tested
        self.robot_arm_rotation._getMeasurement()
        super().testPeriodic()

    def teleopExit(self) -> None:
        self.disablePIDSubsystems()
        return super().teleopExit()

    def moveArm(self, radians: float) -> None:
        self.robot_arm_rotation.setSetpoint(radians)
        self.robot_arm_rotation.enable()

    def moveArmDegrees(self, degrees: float) -> None:
        self.moveArm(math.radians(degrees))

    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""
        self.robot_arm_rotation.disable()

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """


        #track smart dashboad on left click
        self.mech_controller_hid.POVLeft().onTrue(
            commands2.cmd.runOnce(lambda: self.trackAngle(), [self.robot_arm_rotation])
        )

        # Disable the arm controller when Left Stick
        self.mech_controller.leftStick().onTrue(
            commands2.cmd.runOnce(lambda: self.disablePIDSubsystems(), [self.robot_arm_rotation])
        )

        armCommands.createArmPositionCommands(self.mech_controller_hid, self.mech_controller, self.robot_arm_controller, self.robot_arm_rotation)

    def trackAngle(self):
        self.moveArmDegrees(
            wpilib.SmartDashboard.getNumber("set angle", self.robot_arm_rotation.getPostion())
        )

    def disableArm(self):
        print("disabling")
        self.robot_arm_rotation.disable()

    def getCreeperMode(self):
        return self.creeperMode
