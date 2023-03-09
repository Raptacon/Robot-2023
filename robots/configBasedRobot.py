import wpilib
import commands2
import json
from pathlib import Path
import wpimath.filter
import wpimath
import navx
from auto import Autonomous
import os

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

        # self.robotVersion = self.getRobotVersion()

    def getRobotVersion(self) -> str:
        jason_object = None
        home = str(Path.home()) + os.path.sep
        releaseFile = home + "release.json"
        print("release file:" + str(releaseFile))
        try:
            with open('releaseFile', 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                print(json_object)
                print(type(json_object))
        except OSError as E:
                dictionary = '{"deploy-host": "DESKTOP-80HA89O", "deploy-user": "ehsra", "deploy-date": "2023-03-02T17:54:14", "code-path": "blah", "git-hash": "3f4e89f138d9d78093bd4869e0cac9b61becd2b9", "git-desc": "3f4e89f-dirty", "git-branch": "fix-recal-nbeasley"}'
                json_object = json.dumps(dictionary, indent=4)
                for i in json_object:
                    print(f"i={i['deploy-host']}")
        print(f">>>>>>>>>>>>>>>>{json_object}")
        return json_object

    def teleopPeriodic(self) -> None:
        #  wpilib.SmartDashboard.putString("robotVersion", self.robotVersion)
         wpilib.SmartDashboard.putString("robotVersion", "1.26.12")

    def getAutonomousCommand(self):
        return(Autonomous(self.driveTrain, self.navx))


    def teleopInit(self) -> None:
        super().teleopInit()

    #TODO move to a better way, demo purposes
    def getStick(self, axis: wpilib.XboxController.Axis, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))
