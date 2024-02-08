import commands2
import typing
import rev
from subsystem.swerveIntake import SwerveIntake
from subsystem.swerveIntakePivot import SwerveIntakePivot
from subsystem.swerveIntakePivotController import pivotController

class Intake(commands2.CommandBase):
    def __init__(self, intake: SwerveIntake, pivot : pivotController, intakePercent: typing.Callable[[], float], spitOut: typing.Callable[[], bool], pivotGround : typing.Callable[[], bool], pivotHandOff : typing.Callable[[], bool]) -> None:
        super().__init__()
        self.intake = intake
        self.pivot = pivot
        self.intakePercent = intakePercent
        self.spitOut = spitOut

        self.pivotGround = pivotGround
        self.pivotHandOff = pivotHandOff

        self.addRequirements(self.intake, self.pivot)

    def execute(self):
        if(self.spitOut()):
            self.intake.runIntake(-0.5)
        else:
            self.intake.runIntake(self.intakePercent())

        if(self.pivotGround()):
            self.pivot.setGroundPickup()
        elif(self.pivotHandOff()):
            self.pivot.setHandOffPickup()
        