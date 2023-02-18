import commands2
import commands2.cmd
import wpimath.controller
import navx
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

class TurnToAngle(commands2.CommandBase):
    initialHeading = 0
    nextHeading = 0
    turnAngle = 0
    tolerance = .8
    change = 0
    def __init__(self, speed: float, degrees: float, drive: DriveTrain, navx : navx.AHRS) -> None:
        """Creates a new TurnDegrees. This command will turn your robot for a desired rotation (in
        degrees) and rotational speed.
        :param speed:   The speed which the robot will drive. Negative is in reverse.
        :param degrees: Degrees to turn. Leverages encoders to compare distance.
        :param drive:   The drive subsystem on which this command will run
        """
        super().__init__()
        self.turnAngle = degrees
        self.speed = speed
        self.drive = drive
        self.navx = navx
        self.pid = wpimath.controller.PIDController(0.001, 0.001, 0.001, 0.01)
        self.pid.setTolerance(.8)
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        # Set motors to stop, read encoder values for starting point
        self.drive.drive(0, 0)
        self.drive.reset()
        self.initialHeading = self.navx.getFusedHeading()

    def calcHeading(self):
        """Calculates how far away from the desired angle the bot is"""
        self.nextHeading = self.initialHeading + self.turnAngle

        if self.nextHeading > 360:
            self.nextHeading -= 360
        elif self.nextHeading < 0:
            self.nextHeading += 360

        self.change = self.nextHeading - self.navx.getFusedHeading()
        if self.change > 180:
            self.change -= 360
        elif self.change < -180:
            self.change += 360

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.speed = self.pid.calculate(self.change)
        print(self.pid.calculate(self.change, self.tolerance))
        self.drive.arcadeDrive(0, self.speed)
        print("change" + str(self.change))
        self.calcHeading()
        #self.speed = self.speedSections.getSpeed(self.speed, self.change, "TurnToAngle")

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        self.drive.drive(0, 0)
        self.drive.reset()
        self.pid.reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        return abs(self.change) < self.tolerance
