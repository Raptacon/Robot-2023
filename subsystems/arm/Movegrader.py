
import commands2 
import logging
from typing import Callable
log = logging.getLogger(__name__)

class MoveGrader(commands2.CommandBase):
    def __init__(self,graderMotorTriger: Callable[[], float],graderMotorTriger: Callable[[], bollean], grader):
        super().__init__()
        self.graderMotor = winchMotor
        self.grader = grader
        self.addRequirements(self.winch)

    def execute(self) -> None:
        graderMotor = self.graderMotor()
        self.grader.setspeed(graderMotor)

    def end(self, interrupted: bool) -> None:
        self.grader.setspeed(0)

    def isFinished(self) -> bool:
        return False

