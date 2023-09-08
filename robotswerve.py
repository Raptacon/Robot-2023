import wpilib

#from wpilib.interfaces import GenericHID
import wpimath.filter
import wpimath
import commands2.button

from subsystem.swerveDriveTrain import Drivetrain

from commands.defaultdrive import DefaultDrive
from commands.togglefielddrive import ToggleFieldDrive

import math
kDriveControllerIdx = 0
lastDeg =0

class RobotSwerve:
    """
    Container to hold the main robot code
    """

    def __init__(self) -> None:
        self.driveController = wpilib.XboxController(kDriveControllerIdx)
        self.driveTrain = Drivetrain()

        #self.driveController = wpilib.XboxController(0)

        self.xLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

        commands2.button.JoystickButton(self.driveController, 1).whenPressed(ToggleFieldDrive(self.driveTrain))
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: wpimath.applyDeadband(self.driveController.getLeftX(), 0.02),
            lambda: wpimath.applyDeadband(self.driveController.getLeftY(), 0.02),
            lambda: wpimath.applyDeadband(self.driveController.getRightY(), 0.1),
            lambda: self.driveTrain.getFieldDriveRelative()
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
        #if self.autonomousCommand:
        #    self.autonomousCommand.cancel()
        #self.MaxMps = 1
        #self.RotationRate = 1
        pass

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        # LeftX = self.driveController.getRawAxis(wpilib.XboxController.Axis.kLeftX)
        # LeftY = self.driveController.getRawAxis(wpilib.XboxController.Axis.kLeftY)
        # RightX = self.driveController.getRawAxis(wpilib.XboxController.Axis.kRightX)

        # if abs(LeftX) < .05:
        #     LeftX = 0
        # if abs(LeftY) < .05:
        #     LeftY = 0
        # if abs(RightX) < .05:
        #     RightX = 0

        LeftX = wpimath.applyDeadband(self.driveController.getLeftX(), 0.02)
        LeftY = wpimath.applyDeadband(self.driveController.getLeftY(), 0.02)
        RightY = wpimath.applyDeadband(self.driveController.getRightY(), 0.1)

        #self.driveTrain.drive(-1 * LeftY * self.MaxMps, LeftX * self.MaxMps, RightX * self.RotationRate, False)
        #ang = (math.degrees(math.atan2(LeftY, LeftX)) +90.0) %360.0
        #if(abs(LeftX) < 0.8 and abs(LeftY) < 0.8):
            #pass
            #print("pass")
        #else:
            #print(f"Set {ang}")
            #self.driveTrain.setSteer(ang)


    testModes = ["Drive Disable", "Wheels Select", "Wheels Drive", "Enable Cal", "Disable Cal"]
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


    def testPeriodic(self) -> None:
        wheelAngle = wpilib.SmartDashboard.getNumber("Wheel Angle", 0)
        wheelSpeed = wpilib.SmartDashboard.getNumber("Wheel Speed", 0)
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
            case _:
                print(f"Unknown {self.testChooser.getSelected()}")

        for m in self.driveTrain.swerveModules:
            break
            print(f"{m.name} {m.driveMotor.getAppliedOutput()} {m.driveMotor.get()}")
