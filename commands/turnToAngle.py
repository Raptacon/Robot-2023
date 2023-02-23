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

    def __init__(self, degrees: float, drive: DriveTrain, navx : navx.AHRS) -> None:
        """Creates a new TurnDegrees. This command turns the robot to a desired angle in degrees
        :param degrees: Degrees to turn. Uses encoders to compare distance.
        :param drive:   The drive subsystem where this command will run
        """
        super().__init__()

        # tA: TurnAngle

        # self.turnAngle = degrees
        # self.drive = drive
        # self.navx = navx
        # self.pid = wpimath.controller.PIDController(0.001, 0.001, 0.001, 0.01).setTolerance(.8)
        # self.pid.setTolerance(.8)

        self.angle = { 'tA': degrees, 'drive': drive, 'navX': navx, 'pid': wpimath.controller.PIDController(0.001, 0.001, 0.001, 0.01).setTolerance(.8) }
        self.addRequirements(drive)

    def initialize(self) -> None:
        """Called when the command is initially scheduled."""
        # Set motors to stop, read encoder values for starting point
        self.angle['drive'].drive(0, 0)
        self.angle['drive'].reset()
        self.initialHeading = self.angle['navX'].getFusedHeading()

    def calcHeading(self):
        """Calculates how far away from the desired angle the bot is"""
        self.nextHeading = self.initialHeading + self.turnAngle

        if self.nextHeading > 360:
            self.nextHeading -= 360
        elif self.nextHeading < 0:
            self.nextHeading += 360

        self.change = self.nextHeading - self.angle['navX'].getFusedHeading()
        if self.change > 180:
            self.change -= 360
        elif self.change < -180:
            self.change += 360

    def execute(self) -> None:
        """Called every time the scheduler runs while the command is scheduled."""
        self.speed = self.angle['pid'].calculate(self.change)
        self.angle['drive'].arcadeDrive(0, self.speed)
        self.calcHeading()

    def end(self, interrupted: bool) -> None:
        """Called once the command ends or is interrupted."""
        #Stops the movement of the robot and resets the encoders and the PID controller
        self.angle['drive'].drive(0, 0)
        self.angle['drive'].reset()
        self.angle['pid'].reset()

    def isFinished(self) -> bool:
        """Returns true when the command should end."""
        return abs(self.change) < self.tolerance
