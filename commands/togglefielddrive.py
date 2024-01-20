import commands2
from subsystem.swerveDriveTrain import Drivetrain

class ToggleFieldDrive(commands2.InstantCommand):
    def __init__(self, driveTrain: Drivetrain) -> None:
        super().__init__()
        self.driveTrain = driveTrain
        self.addRequirements(driveTrain)

    def execute(self) -> None:
        print(f"Toggling field relative from {self.driveTrain.getFieldDriveRelative()} to {not self.driveTrain.getFieldDriveRelative()}")
        self.driveTrain.setFieldDriveRelative(not self.driveTrain.getFieldDriveRelative())

