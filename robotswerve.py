import wpilib

#from wpilib.interfaces import GenericHID
import wpimath.filter
import wpimath
import commands2.button

from subsystem.swerveDriveTrain import Drivetrain
from subsystem.swerveIntake import SwerveIntake
from subsystem.swerveIntakePivot import SwerveIntakePivot
from subsystem.swerveIntakePivotController import pivotController

from commands.intake import Intake
from commands.defaultdrive import DefaultDrive
from commands.togglefielddrive import ToggleFieldDrive
from commands.resetfielddrive import ResetFieldDrive

import math
kDriveControllerIdx = 0
kMechControllerIdx = 1
lastDeg =0

class RobotSwerve:
    """
    Container to hold the main robot code
    """

    def __init__(self) -> None:
        self.driveController = wpilib.XboxController(kDriveControllerIdx)
        self.mechController = wpilib.XboxController(kMechControllerIdx)

        self.driveTrain = Drivetrain()

        self.intake = SwerveIntake()
        self.pivot = SwerveIntakePivot()
        self.intakePivotController = pivotController()
        self.intakePivotController.setIntakeRotationSubsystem(self.pivot)
        #self.driveController = wpilib.XboxController(0)

        self.xLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

        commands2.button.JoystickButton(self.driveController, 1).onTrue(ToggleFieldDrive(self.driveTrain))
        commands2.button.JoystickButton(self.driveController, 2).onTrue(ResetFieldDrive(self.driveTrain))
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: wpimath.applyDeadband(self.driveController.getLeftX(), 0.06),
            lambda: wpimath.applyDeadband(self.driveController.getLeftY(), 0.06),
            lambda: wpimath.applyDeadband(self.driveController.getRightX(), 0.1),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))
        self.intake.setDefaultCommand(Intake(
            self.intake,
            self.intakePivotController,
            lambda: wpimath.applyDeadband(self.mechController.getLeftTriggerAxis(), 0.05),
            lambda: self.mechController.getLeftBumper(),
            lambda: self.mechController.getAButton(),
            lambda: self.mechController.getBButton()
        ))
        '''
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: -self.driveController.getLeftY(),
            lambda: self.driveController.getLeftX(),
            lambda: -self.driveController.getRightX(),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))'''


    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        #self.autonomousCommand = self.container.getAutonomousCommand()

        #if self.autonomousCommand:
        #    self.autonomousCommand.schedule()
        pass

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        pass

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        pass

    testModes = ["Drive Disable", "Wheels Select", "Wheels Drive", "Enable Cal", "Disable Cal", "Wheel Pos", "Pivot Rot"]
    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        #commands2.CommandScheduler.getInstance().cancelAll()
        self.calEn = False
        self.calDis = False
        self.testChooser = wpilib.SendableChooser()
        for i in self.testModes:
            self.testChooser.addOption(i, i)
        self.testChooser.setDefaultOption("Drive Disable","Drive Disable")
        wpilib.SmartDashboard.putData("Test Mode", self.testChooser)
        wpilib.SmartDashboard.putNumber("Wheel Angle", 0)
        wpilib.SmartDashboard.putNumber("Wheel Speed", 0)
        wpilib.SmartDashboard.putNumber("Pivot Angle:", 40)


    def testPeriodic(self) -> None:
        wheelAngle = wpilib.SmartDashboard.getNumber("Wheel Angle", 0)
        wheelSpeed = wpilib.SmartDashboard.getNumber("Wheel Speed", 0)
        pivotAngle = wpilib.SmartDashboard.getNumber("Pivot Angle:", 40)
        wheelAngle #"use" value
        wheelSpeed #"use" value
        self.driveTrain.getCurrentAngles()
        LeftX = wpimath.applyDeadband(self.driveController.getLeftX(), 0.02)
        LeftY = wpimath.applyDeadband(self.driveController.getLeftY(), 0.02)
        RightY = wpimath.applyDeadband(self.driveController.getRightY(), 0.1)
        global lastDeg

        #self.driveTrain.drive(-1 * LeftY * self.MaxMps, LeftX * self.MaxMps, RightX * self.RotationRate, False)
        match self.testChooser.getSelected():
            case "Drive Disable":
                print("Drive Disable")
                self.calEn = False
                self.calDis = False
                self.driveTrain.disable()
            case "Wheels Select":
                #self.driveTrain.setSteer(wheelAngle)
                ang = (math.degrees(math.atan2(LeftY, LeftX)) +90.0) %360.0
                if(abs(LeftX) < 0.8 and abs(LeftY) < 0.8):
                    pass
                    print("pass")
                    self.driveTrain.setSteer(ang)
                    self.driveTrain.setDrive(RightY)
                else:
                    print(f"Set {ang}")
                    lastDeg = ang
                    self.driveTrain.setSteer(ang)
                    self.driveTrain.setDrive(RightY)
            case "Wheels Drive":
                self.driveTrain.setDrive(RightY)
            case "Enable Cal":
                if not self.calEn:
                    self.driveTrain.calWheels(True)
                    self.calEn = False
            case "Disable Cal":
                self.driveTrain.calWheels(False)
            case "Wheel Pos":
                self.driveTrain.setSteer(wheelAngle)
            case "Pivot Rot":
                self.intakePivotController.setManipulator(pivotAngle)
            case _:
                print(f"Unknown {self.testChooser.getSelected()}")

        for m in self.driveTrain.swerveModules:
            break
            print(f"{m.name} {m.driveMotor.getAppliedOutput()} {m.driveMotor.get()}")
