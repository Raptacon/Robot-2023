import commands2

from subsystems.drivetrains import westcoast


class goToDist(commands2.CommandBase):
    def __init__(self, speed: float, inches: float, drive: westcoast) -> None:
        """Creates a new goToDist. This command will drive your your robot for a desired distance at
        a desired speed.
        :param speed:  The speed at which the robot will drive
        :param inches: The number of inches the robot will drive
        :param drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()

        self.distance = inches
        self.speed = speed
        self.drive = drive
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        self.drive.drive(0, 0)
        self.drive.reset()

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.drive.drive(self.speed, 0)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return abs(self.drive.getDistance()) >= self.distance