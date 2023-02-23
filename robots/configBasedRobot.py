import wpilib
import commands2

import wpimath.filter
import wpimath
from Input import input
import navx
from auto import Autonomous

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

        self.navx = navx._navx.AHRS.create_spi()

    def getAutonomousCommand(self):
        return(Autonomous(self.driveTrain, self.navx))


    def teleopInit(self) -> None:
        super().teleopInit()

    #TODO move to a better way, demo purposes
    def getStick(self, axis: wpilib.XboxController.Axis, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))
