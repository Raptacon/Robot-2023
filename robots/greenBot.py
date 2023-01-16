import wpilib
import commands2
import ctre
import navx
from subsystems.drivetrains.westcoast import Westcoast as Drivetrain
from commands.tankDrive import TankDrive
import wpimath.filter
import wpimath

class GreenBot(commands2.TimedCommandRobot):
    config_name = "GreenBot"


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

        self.driveTrain = Drivetrain(rightM, leftM, motors['left'], motors['right'], navx.AHRS.create_i2c())
        self.tankDrive = TankDrive(getStick(wpilib.XboxController.Axis.kLeftY),
                                   getStick(wpilib.XboxController.Axis.kRightY),
                                   self.driveTrain)

    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)





#TODO move to a better way, demo purposes
def getStick(axis: wpilib.XboxController.Axis):
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(wpimath.applyDeadband(-wpilib.XboxController(0).getRawAxis(axis), 0.1))

