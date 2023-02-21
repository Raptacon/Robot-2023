import wpilib
import commands2
from commands.tankDrive import TankDrive
from commands.arcadeDrive import ArcadeDrive
from Input import input
import navx
from auto import Autonomous
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
        self.balance = Balance(input().getButton("XButton", self.XboxController), self.driveTrain)

        self.tankDrive = TankDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightY, True),
                                   self.driveTrain)
        self.arcadeDrive = ArcadeDrive(input.getStick(wpilib.XboxController.Axis.kLeftY, True),
                                   input.getStick(wpilib.XboxController.Axis.kRightX, False),
                                   self.driveTrain)
        self.balanceDrive = TankDrive(self.balance.dobalance,self.balance.dobalance, self.driveTrain)

        self.navx = navx._navx.AHRS.create_spi()
        #self.driveModeSelect = commands2.SelectCommand(
        #    self.DrivetrainMode.TANK
        #)

    def getAutonomousCommand(self):
        return(Autonomous(self.driveTrain, self.navx))

    def teleopInit(self) -> None:
        self.XboxController = wpilib.XboxController(0)
        self.driveTrain.setDefaultCommand(self.tankDrive)

    def teleopPeriodic(self) -> None:
        """ Runs every frame """
        if input().getButton("XButton", self.XboxController):
            if(not self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.balanceDrive)
            self.balanceing = True
        else:
            if(self.balanceing):
                commands2.CommandScheduler.getInstance().cancelAll()
            self.driveTrain.setDefaultCommand(self.tankDrive)
            self.balanceing = False

