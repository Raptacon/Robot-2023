#!/usr/bin/env python3

import os

import typing
import wpilib
import commands2

# from robots.configBasedRobot import ConfigBaseCommandRobot
# from robots.greenBot import GreenBot
# from robots.dumboBot import Dumbo
from utils import botFactory


class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run
    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.

        # get a robot (with defined motors, subsystems, etc based on the robot name or config file
        # TODO rename container to robot or something more obvious?
        self.container = botFactory.get_bot(self.setRobotNameFromEnv())

        # if False:
        #     self.container = GreenBot()
        # if True:
        #     self.container = ConfigBaseCommandRobot()
        #  if True:
        # self.container = Dumbo()

    def setRobotNameFromEnv(self) -> str:
        """Attempts to get the robot name from the environment variable ROBOT_NAME

        Returns:
            str: name of the robot like green, dumbo, teapot, lab, etc
        """
        return os.getenv("ROBOT_NAME")

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        self.container.disabledInit()

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        self.container.disabledPeriodic()

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.container.autonomousInit()
        self.autonomousCommand = None

        try:
            self.autonomousCommand = self.container.getAutonomousCommand()
        except Exception as err:
            wpilib.reportError(f"Autonoms command not found. {err}", True)

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        self.container.autonomousPeriodic()

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
        self.container.teleopInit()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        self.container.teleopPeriodic()

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        self.container.testInit()

    def testPeriodic(self) -> None:
        self.container.testPeriodic()


if __name__ == "__main__":
    wpilib.run(MyRobot)
