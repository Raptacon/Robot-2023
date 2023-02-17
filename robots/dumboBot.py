import wpilib
import commands2
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath

import utils.configMapper
from .configBasedRobot import ConfigBaseCommandRobot

class Dumbo(ConfigBaseCommandRobot):
    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        wpilib.XboxController(0).A().whenPressed(commands2.Command.runOnce(lambda: print("A pressed")))



    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)


    def testInit(self) -> None:
        return super().testInit()