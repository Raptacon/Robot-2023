
import commands2 
import logging
from typing import Callable
log = logging.getLogger(__name__)

class MoveGrader(commands2.CommandBase):
    def __init__(self,graderMotorTriger: Callable[[], float],graderMotorBumper: Callable[[], float], grader):
        super().__init__()
        self.intake = graderMotorTriger
        self.outtake = graderMotorBumper
        self.grader = grader
        self.addRequirements(self.winch)

    def execute(self) -> None:
        graderMotor = self.graderMotor()
        if self.outtake == True:
            self.grader.setspeed(1)
        elif self.intake == True:
            self.grader.setspeec(-1)

    def end(self, interrupted: bool) -> None:
        self.grader.setspeed(0)

    def isFinished(self) -> bool:
        return False

