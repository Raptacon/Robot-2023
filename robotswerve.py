import wpilib

from wpilib.interfaces import GenericHID

import commands2
#import commands2.button

from subsystem.swerveDriveTrain import Drivetrain

kDriveControllerIdx = 0


class RobotSwerve:
    """
    Container to hold the main robot code
    """

    def __init__(self) -> None:
        self.driveController = wpilib.XboxController(kDriveControllerIdx)
        self.driveTrain = Drivetrain()


