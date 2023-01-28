# from components.Actuators.HighLevel.driveTrainHandler import DriveTrainHandler
# from components.Actuators.LowLevel.driveTrain import ControlMode
# from components.SoftwareControl.speedSections import SpeedSections
from commands2 import tunable, feedback, StateMachine, state
import random

# ControlMode input
from enum import Enum, auto
from robot import MyRobot

import navx

import math
import commands2

from subsystems.drivetrains import westcoast


class turnToAngle(commands2.CommandBase):
    def __init__(self, speed: float, degrees: float, drive: westcoast) -> None:
        """Creates a new turnToAngle. This command will turn your robot for a desired rotation (in
        degrees) and rotational speed.
        :param speed:   The speed which the robot will drive. Negative is in reverse.
        :param degrees: Degrees to turn. Leverages encoders to compare distance.
        :param drive:   The drive subsystem on which this command will run
        """
        super().__init__()

        self.degrees = degrees
        self.speed = speed
        self.drive = drive
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        # Set motors to stop, read encoder values for starting point
        self.drive.drive(0, 0)
        self.drive.reset()

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.drive.drive(0, self.speed)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""

        # Need to convert distance travelled to degrees. The Standard
        # Romi Chassis found here, https://www.pololu.com/category/203/romi-chassis-kits,
        # has a wheel placement diameter (149 mm) - width of the wheel (8 mm) = 141 mm
        # or 5.551 inches. We then take into consideration the width of the tires.
        inchPerDegree = math.pi * 5.551 / 360.0

        # Compare distance travelled from start to distance based on degree turn
        return self._getAverageTurningDistance() >= inchPerDegree * self.degrees

    def _getAverageTurningDistance(self) -> float:
        distance = abs(self.drive.getDistance())
        return distance