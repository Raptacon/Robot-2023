import commands2
import logging
from typing import Callable
log = logging.getLogger(__name__)
class TankDrive(commands2.CommandBase):
    '''
    Command for converting joystick input to drive train output
    '''
    limit : float

    def __init__(self, left: Callable[[], float], right: Callable[[], float], driveTrain):
        '''
        Takes a left, right callerable to get tank drive controls
        Takes driveTrain on which to operate. Requires drive train with left, right drive call.
        Update to support other types in future? X, Y?
        '''
        super().__init__()
        self.left = left
        self.right = right
        self.driveTrain = driveTrain

        #setup subsystem
        self.addRequirements(self.driveTrain)

    def execute(self) -> None:
        '''
        Called repeatably when this command is scheduled to run.
        '''
        left = self.left()
        right = self.right()
        if left > self.limit:
            left = self.limit
        if right > self.limit:
            right = self.limit
        log.debug(f"l {left}, r {right}")
        self.driveTrain.drive(left, right)

    def end(self, interrupted: bool) -> None:
        '''
        Safe drive train when ending
        '''
        self.driveTrain.drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False
