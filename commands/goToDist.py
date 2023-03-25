import commands2
import commands2.cmd
import wpimath.controller
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

class GoToDist(commands2.CommandBase):
    targetDist = 0
    tolerance = 5
    def __init__(self, feet: float, drive: DriveTrain) -> None:
        """Creates a new DriveDistance. This command will drive your your robot for a desired distance at
        a desired speed.
        inches: The number of inches the robot will drive
        drive:  The drivetrain subsystem on which this command will run
        """
        super().__init__()
        self.targetDist = feet * 10_000 #The encoders read in 10,000ths of a foot so we need to multiply it by 10000
        self.drive = drive
        self.pid = wpimath.controller.PIDController(0.1, 0.02, 0.0)
        self.pid.setTolerance(5, 10)
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        print("Init drive2distance")
        self.pid.reset()
        self.drive.drive(0, 0)
        self.drive.reset()
        self.startingDistance = abs(self.drive.getRightEncoder())

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.dist = abs(self.drive.getRightEncoder()) - self.startingDistance
        if(self.targetDist >= 0):
            self.totalOffset = self.targetDist - self.dist
        else:
            self.totalOffset = self.targetDist + self.dist
        self.speed = self.pid.calculate(self.dist / 10_000, self.targetDist / 10_000)
        self.drive.drive(self.speed, self.speed)
        print(self.totalOffset)

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)
        self.drive.reset()
        self.pid.reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        # Compare distance travelled from start to desired distance
        return abs(self.totalOffset) < self.tolerance
