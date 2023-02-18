import wpilib
import commands2
import commands2.cmd
import commands2.button
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
import wpimath.filter
import wpimath

import utils.configMapper
from .configBasedRobot import ConfigBaseCommandRobot

class Dumbo(ConfigBaseCommandRobot):
    def __init__(self, period: float = 0.02) -> None:
        super().__init__(period)

        controller = commands2.button.CommandXboxController(0)
        controller.A().onTrue(
            commands2..run(lambda: self.moveArm(2), [self.robot_arm])
        )




    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)


    def testInit(self) -> None:
        return super().testInit()