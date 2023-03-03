import commands2
import commands2.cmd
import wpimath.controller
import time
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

#TODO change name to something that represents time as this no longer works with distance
class GoToDist(commands2.CommandBase):
    def __init__(self, maxTime: float, drive: DriveTrain, speed : float) -> None:
        """Creates a new DriveDistance. This command will drive your your robot for a desired distance at
        a desired speed.
        inches: The number of inches the robot will drive
        drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()
        self.drive = drive
        self.startingTime = time.time()
        self.maxTime = maxTime
        self.speed = speed
        self.addRequirements(drive)

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.currentTime = time.time() - self.startingTime
        print(self.currentTime)
        if(self.currentTime < self.maxTime):
            self.drive.drive(self.speed, self.speed)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return self.currentTime > self.maxTime
