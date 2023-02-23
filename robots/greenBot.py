import wpilib
import ctre
import navx
from subsystems.drivetrains.westcoast import Westcoast as Drivetrain
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
from .configBasedRobot import ConfigBaseCommandRobot
from Input import input

import enum

class GreenBot(ConfigBaseCommandRobot):
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

        self.driveTrain = Drivetrain(rightM, leftM, motors['left'], motors['right'], navx.AHRS.create_i2c())
        self.tankDrive = TankDrive(input.getStick(wpilib.XboxController.Axis.kRightY, True),
                                   input.getStick(wpilib.XboxController.Axis.kLeftY, False),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)
        self.driveTrain = self.subsystems["drivetrain"]
        self.tankDrive = TankDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightY, True),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)

        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)

