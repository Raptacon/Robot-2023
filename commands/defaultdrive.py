import typing
import commands2
from subsystem.swerveDriveTrain import Drivetrain


class DefaultDrive(commands2.CommandBase):
    def __init__ (
        self,
        driveTrain: Drivetrain,
        forward: typing.Callable[[], float],
        translation: typing.Callable[[], float],
        rotation: typing.Callable[[], float],
        field: typing.Callable[[], bool]
    ) -> None:
        super().__init__()

        self.driveTrain = driveTrain
        self.forward = forward
        self.translation = translation
        self.rotation = rotation
        self.field = field
        self.addRequirements(self.driveTrain)

    def execute(self) -> None:
        #print(f"self.forward() {self.forward():1.2f} , self.translation() {self.translation():1.2f} , self.rotation() {self.rotation():1.2f}")
        self.driveTrain.drive(self.forward(), self.translation(), self.rotation(), self.field())
