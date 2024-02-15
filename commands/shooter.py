import commands2
from subsystem.swerveShooter import SwerveShooter
from subsystem.swerveShooterPivot import ShooterPivot
import typing

class Shooter(commands2.CommandBase):
    def __init__(self, shooter : SwerveShooter, intaking : typing.Callable[[], bool], outaking : typing.Callable[[], bool], shooterSpeed : typing.Callable[[], float], pivot : ShooterPivot, pivotSpeed : typing.Callable[[], float]):
        super().__init__()

        self.shooter = shooter
        self.intaking = intaking
        self.outaking = outaking
        self.shooterSpeed = shooterSpeed

        self.pivot = pivot
        self.pivotSpeed = pivotSpeed

        self.addRequirements(self.shooter, self.pivot)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.2)
        elif(self.outaking()):
            self.shooter.runIntake(-0.2)
        else:
            self.shooter.runIntake(0)

        self.shooter.runShooters(self.shooterSpeed())

        self.pivot.runPivot(self.pivotSpeed())
