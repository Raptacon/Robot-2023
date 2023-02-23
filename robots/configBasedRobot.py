import wpilib
import commands2
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
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

        self.driveTrain = self.subsystems["drivetrain"]
        self.tankDrive = TankDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightY, True),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)

        self.navx = navx._navx.AHRS.create_spi()
        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def getAutonomousCommand(self):
        return(Autonomous(self.driveTrain, self.navx))

    def teleopInit(self) -> None:
        self.driveTrain.setDefaultCommand(self.tankDrive)
