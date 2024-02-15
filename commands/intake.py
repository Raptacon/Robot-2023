import commands2
import typing
from subsystem.swerveIntake import SwerveIntake
from subsystem.swerveIntakePivot import SwerveIntakePivot
from subsystem.swerveIntakePivotController import pivotController

class Intake(commands2.CommandBase):
    def __init__(self, intake: SwerveIntake, pivot : pivotController, intakePercent: typing.Callable[[], float], spitOut: typing.Callable[[], bool], changePivot : typing.Callable[[], bool]) -> None:
        super().__init__()
        self.intake = intake
        self.pivot = pivot
        self.intakePercent = intakePercent
        self.spitOut = spitOut

        self.rotatePivot = False
        self.changePivot = changePivot

        self.addRequirements(self.intake, self.pivot)

    def execute(self):
        if(self.spitOut()):
            self.intake.runIntake(-0.2)
        else:
            self.intake.runIntake(self.intakePercent())

        if(self.changePivot()):
            self.rotatePivot = not self.rotatePivot
            
        if(self.rotatePivot):
            self.pivot.setGroundPickup()
        else:
            self.pivot.setHandOffPickup()
        