import wpilib

#from wpilib.interfaces import Gene1ricHID
import wpimath.filter
import wpimath
import commands2.button

from subsystem.swerveDriveTrain import Drivetrain

from commands.defaultdrive import DefaultDrive
from commands.togglefielddrive import ToggleFieldDrive

kDriveControllerIdx = 0


class RobotSwerve:
    """
    Container to hold the main robot code
    """

    def __init__(self) -> None:
        self.driveController = wpilib.XboxController(kDriveControllerIdx)
        self.driveTrain = Drivetrain()

        self.driveController = wpilib.XboxController(0)

        self.xLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

        commands2.button.JoystickButton(self.driveController, 1).whenPressed(ToggleFieldDrive(self.driveTrain))
        '''
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: -self.xLimiter.calculate(wpimath.applyDeadband(self.driveController.getLeftY(), 0.02)),
            lambda: self.yLimiter.calculate(wpimath.applyDeadband(self.driveController.getLeftX(), 0.02)),
            lambda: -self.xLimiter.calculate(wpimath.applyDeadband(self.driveController.getRightX(), 0.02)),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))
        '''
        self.driveTrain.setDefaultCommand(DefaultDrive(
            self.driveTrain,
            lambda: -self.driveController.getLeftY(),
            lambda: self.driveController.getLeftX(),
            lambda: -self.driveController.getRightX(),
            lambda: self.driveTrain.getFieldDriveRelative()
        ))


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
        pass

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""

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
        match self.testChooser.getSelected():
            case "Drive Disable":
                print("Drive Disable")
                self.calEn = False
                self.calDis = False                
                self.driveTrain.disable()
            case "Wheels Select":
                self.driveTrain.setSteer(wheelAngle)
            case "Wheels Drive":
                self.driveTrain.setDrive(wheelSpeed)
            case "Enable Cal":
                if not self.calEn:
                    self.driveTrain.calWheels(True)
                    self.calEn = False
            case "Disable Cal":
                self.driveTrain.calWheels(False)
            case _:
                print(f"Unknown {self.testChooser.getSelected()}")

