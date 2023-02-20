import wpilib
import commands2
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath
from commands.balance import Balance

import utils.configMapper

class  ConfigBaseCommandRobot(commands2.TimedCommandRobot):
    balanceing = False
    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        #load config
        config, configPath = utils.configMapper.findConfig("greenBot.yml")

        assert config, "Please configure default robotConfig. \n\
                        run 'echo (robotCfg.yml) > robotConfig' on roborio\n\
                        where (robotCfg.yml) is the name of the file"

        self.configMapper = utils.configMapper.ConfigMapper(config, configPath)

        self.subsystems = {}
        for ssName in self.configMapper.getSubsystems():
            print(ssName)
            subsystem = self.configMapper.getSubsystem(ssName)
            self.subsystems[ssName] = subsystem

        self.XboxController = wpilib.XboxController(0)

        self.driveTrain = self.subsystems["drivetrain"]
        self.balance = Balance(getButton(wpilib.XboxController.getXButton(self.XboxController)), self.driveTrain)
        self.tankDrive = TankDrive(getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   getStick(wpilib.XboxController.Axis.kRightY, True),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)
        self.balanceDrive = TankDrive(self.balance.dobalance,self.balance.dobalance, self.driveTrain)

        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def teleopInit(self) -> None:
        self.XboxController = wpilib.XboxController(0)
        self.driveTrain.setDefaultCommand(self.tankDrive)

    def teleopPeriodic(self) -> None:
        """ Runs every frame """
        if self.XboxController.getXButton():
            if(not self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.balanceDrive)
            self.balanceing = True
        else:
            if(self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.tankDrive)
            self.balanceing = False


#TODO move to a better way, demo purposes
def getStick(axis: wpilib.XboxController.Axis, invert: bool = False):
    sign = -1.0 if invert else 1.0
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))

def getButton(button: wpilib.XboxController.Button.kX):
    return lambda: wpilib.XboxController(0).getRawButton(button)
