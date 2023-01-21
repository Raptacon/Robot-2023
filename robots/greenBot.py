import wpilib
import commands2
import ctre
import navx
from subsystems.drivetrains.westcoast import Westcoast as Drivetrain
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath

import enum

class GreenBot(commands2.TimedCommandRobot):
    config_name = "GreenBot"

    class DrivetrainMode(enum.Enum):
        ARCADE = enum.auto()
        TANK = enum.auto()


    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        #create the greenbot motors
        motors = {}
        motors['right'] = ctre.WPI_TalonFX(30)
        motors['rightF'] = ctre.WPI_TalonFX(31)
        motors['left'] = ctre.WPI_TalonFX(20)
        motors['leftF'] = ctre.WPI_TalonFX(21)

        rightM = wpilib.MotorControllerGroup(motors['right'], motors['rightF'])
        leftM = wpilib.MotorControllerGroup(motors['left'], motors['leftF'])

        self.driveTrain = Drivetrain(rightM, leftM, motors['left'], motors['right'], None)
        self.tankDrive = TankDrive(getStick(wpilib.XboxController.Axis.kRightY, True),
                                   getStick(wpilib.XboxController.Axis.kLeftY, False),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)

        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)





#TODO move to a better way, demo purposes
def getStick(axis: wpilib.XboxController.Axis, invert: bool = False):
    sign = -1.0 if invert else 1.0
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))

