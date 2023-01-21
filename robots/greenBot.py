import wpilib
import commands2
import ctre
import navx
from subsystems.drivetrains.westcoast import Westcoast as Drivetrain
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath
import typing

import enum
from enum import Enum, auto

class GreenBot(commands2.TimedCommandRobot):
    config_name = "GreenBot"


    InputCommand: typing.Optional[commands2.Command] = None
    class DrivetrainMode(enum.Enum):
        ARCADE = enum.auto()
        TANK = enum.auto()

    controlMode = DrivetrainMode.TANK
    controlModes = {"Tank": DrivetrainMode.TANK, "Arcade": DrivetrainMode.ARCADE}

    def selectInput(self) -> DrivetrainMode:
        self.controlMode = self.chooser.getSelected()
        print("Mode =" + str(self.controlMode))
        return self.controlMode

    def __init__(self, period: float = 0.02) -> None:
        """
        Creates the greenbot motors and gets the input from an xbox controller
        """
        super().__init__(period)

        motors = {}
        motors['right'] = ctre.WPI_TalonFX(30)
        motors['rightF'] = ctre.WPI_TalonFX(31)
        motors['left'] = ctre.WPI_TalonFX(20)
        motors['leftF'] = ctre.WPI_TalonFX(21)

        rightM = wpilib.MotorControllerGroup(motors['right'], motors['rightF'])
        leftM = wpilib.MotorControllerGroup(motors['left'], motors['leftF'])

        rightM.setInverted(True)

        self.driveTrain = Drivetrain(rightM, leftM, motors['left'], motors['right'], navx.AHRS.create_i2c())
        self.tankDrive = TankDrive(getStick(wpilib.XboxController.Axis.kRightY, False),
                                   getStick(wpilib.XboxController.Axis.kLeftY, False),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)

        self.chooser = wpilib.SendableChooser()

        for key, item in self.controlModes.items():
            if key == self.controlMode:
                self.chooser.setDefaultOption(key, self.controlMode)
            self.chooser.addOption(key, item)

        wpilib.SmartDashboard.putData("Control Mode", self.chooser)

    def teleopInit(self) -> None:
        #TODO create a way to switch between drivetrain types
        self.controlMode = self.chooser.getSelected()
        print(str(self.controlMode))

        self.InputCommand = commands2.SelectCommand( self.selectInput,
            # Maps selector values to commands
            [
                (
                    self.DrivetrainMode.TANK,
                    commands2.PrintCommand("Command Tank was selected!"),
                ),
                (
                    self.DrivetrainMode.ARCADE,
                    commands2.PrintCommand("Command Arcade was selected!"),
                ),
            ],
        )
        if self.controlMode == self.DrivetrainMode.TANK:
            self.driveTrain.setDefaultCommand(self.tankDrive)
        elif self.controlMode == self.DrivetrainMode.ARCADE:
            self.driveTrain.setDefaultCommand(self.arcadeDrive)

    class tank(commands2.CommandBase):
        def __init__(self) -> None:
            super().__init__()
            commands2.PrintCommand("Command Tank was selected")

#TODO move to a better way, demo purposes
def getStick(axis: wpilib.XboxController.Axis, invert: bool = False):
    sign = -1.0 if invert else 1.0
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))
