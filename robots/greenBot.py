import wpilib
import commands2
import ctre
import navx
from subsystems.drivetrains.westcoast import Westcoast as Drivetrain
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
from MotorHelper import createMotor
import wpimath

import enum

class GreenBot(commands2.TimedCommandRobot):
    config_name = "GreenBot"

    class DrivetrainMode(enum.Enum):
        ARCADE = enum.auto()
        TANK = enum.auto()

    class motorDescription():
        """
        Here is where all the basic info for a motor is set up.
        """
        def __init__(self, type, channel, usesPID, P, I, D, haslimits, CurrentLimit, triggerCurrent, triggerTime, invert, masterChannel):
            self.motorType = type
            self.motorChannel = channel
            self.motorUsesPID = usesPID
            self.motorP = P
            self.motorI = I
            self.motorD = D
            self.motorHasLimits = haslimits
            self.triggerThresholdCurrent = triggerCurrent
            self.triggerThresholdTime = triggerTime
            self.currentLimit = CurrentLimit
            self.motorInvert = invert
            self.motorMasterChannel = masterChannel

    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        #create the greenbot motors
        type = "CANTalonFX"
        motors = {}
        rightMotor = self.motorDescription("CANTalonFX", 30, False, 0, 0, 0, True, 40, 60, 50, False, 0)
        rightMotorFront = self.motorDescription("CANTalonFX", 31, False, 0, 0, 0, True, 40, 60, 50, False, 0)
        leftMotor = self.motorDescription("CANTalonFX", 20, False, 0, 0, 0, True, 40, 60, 50, False, 0)
        leftMotorFront = self.motorDescription("CANTalonFX", 21, False, 0, 0, 0, True, 40, 60, 50, False, 0)

        rightMotor = createMotor(rightMotor, motors)
        rightMotorFront = createMotor(rightMotorFront, motors)
        leftMotor = createMotor(leftMotor, motors)
        leftMotorFront = createMotor(leftMotorFront, motors)

        rightM = wpilib.MotorControllerGroup(rightMotor, rightMotorFront)
        leftM = wpilib.MotorControllerGroup(leftMotor, leftMotorFront)

        self.driveTrain = Drivetrain(rightM, leftM, leftMotor, rightMotor, navx.AHRS.create_i2c())
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

