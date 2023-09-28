import commands2
from subsystem.swerveDriveTrain import Drivetrain

class ResetFieldDrive(commands2.InstantCommand):
    def __init__(self, driveTrain: Drivetrain) -> None:
        super().__init__()
        self.driveTrain = driveTrain
        self.addRequirements(driveTrain)

    def execute(self) -> None:
        print("reset heading")
        self.driveTrain.resetHeading()
