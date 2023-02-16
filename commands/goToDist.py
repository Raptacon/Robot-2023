import commands2

from subsystems.drivetrains.westcoast import Westcoast as DriveTrain
from speedSections import SpeedSections

class GoToDist(commands2.CommandBase):
    targetDist = 0
    tolerance = .25
    def __init__(self, speed: float, feet: float, drive: DriveTrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot for a desired distance at
        a desired speed.
        :param speed:  The speed at which the robot will drive
        :param inches: The number of inches the robot will drive
        :param drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()
        self.targetDist = feet * 10_000
        self.speed = speed
        self.drive = drive
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        self.drive.drive(0, 0)
        self.drive.reset()
        self.startingDistance = abs(self.drive.getRightEncoder())

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.dist = abs(self.drive.getRightEncoder()) - self.startingDistance
        self.drive.drive(self.speed, self.speed)
        self.totalOffset = self.targetDist - self.dist
        #self.speed = self.speedSections.getSpeed(self.speed ,totalOffset, "GoToDist")

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)
        self.drive.reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.totalOffset < self.tolerance