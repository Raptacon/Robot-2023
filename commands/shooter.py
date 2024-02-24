import commands2
from subsystem.sparkyShooter import SparkyShooter
from subsystem.sparkyShooterPivot import SparkyShooterPivot
import typing

class Shooter(commands2.CommandBase):
    def __init__(self,
                 shooter : SparkyShooter,
                 pivot: SparkyShooterPivot,
                 intaking : typing.Callable[[], bool],
                 outaking : typing.Callable[[], bool],
                 shooterSpeed : typing.Callable[[], float],
                 pivotToggle: typing.Callable[[], bool]):
        super().__init__()

        self.shooter = shooter
        self.intaking = intaking
        self.outaking = outaking
        self.shooterSpeed = shooterSpeed
        self.pivotToggle = pivotToggle

        self.pivot = pivot
        self.pivotLoad = True
        self.pivot.enable()

        self.addRequirements(self.shooter, self.pivot)

    def execute(self):
        if(self.intaking()):
            self.shooter.runIntake(0.2)
        elif(self.outaking()):
            self.shooter.runIntake(-0.2)
        else:
            self.shooter.runIntake(0)

        self.shooter.runShooters(self.shooterSpeed())

        if(self.pivotToggle()):
            if self.pivotLoad:
                self.pivotLoad = False
                self.pivot.setAmp()
            else:
                self.pivotLoad = True
                self.pivot.setLoading()
