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
        self.addRequirements([self.driveTrain])

    def execute(self) -> None:
        self.driveTrain.drive(self.forward(), self.translation(), self.rotation(), self.field())