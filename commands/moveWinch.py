import commands2 
import logging
from typing import Callable
log = logging.getLogger(__name__)

class moveWinch(commands2.CommandBase):
    def __init__(self,winchMotor: Callable[[], float], winch):
        super().__init__()
        self.winchMotor = winchMotor
        self.winch = winch
        self.addRequirements(self.winch)
    
    def execute(self) -> None:
        winchMotor = self.winchMotor()
        self.winch.setspeed(winchMotor)
    
    def end(self, interrupted: bool) -> None:
        self.winch.setspeed(0)
        
    def isFinished(self) -> bool:
        return False
        