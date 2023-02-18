import wpilib
import commands2
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath

import utils.configMapper

class  ConfigBaseCommandRobot(commands2.TimedCommandRobot):
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
        """
        """
        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def teleopInit(self) -> None:
        super().teleopInit()




    #TODO move to a better way, demo purposes
    def getStick(self, axis: wpilib.XboxController.Axis, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))

