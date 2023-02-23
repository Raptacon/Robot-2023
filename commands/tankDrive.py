import commands2
import logging
from typing import Callable
from subsystems.drivetrains.westcoast import Westcoast

log = logging.getLogger(__name__)
class TankDrive(commands2.CommandBase):
    '''
    Command for converting joystick input to drive train output
    '''
    def __init__(self, left: Callable[[], float], right: Callable[[], float], driveTrain: Westcoast):
        '''
        Takes a left, right callerable to get tank drive controls
        Takes driveTrain on which to operate. Requires drive train with left, right drive call.
        Update to support other types in future? X, Y?
        '''
        super().__init__()

        self.controller = {'left': left, 'right': right, 'dt': driveTrain}
        #setup subsystem
        self.addRequirements(self.controller['dt'])

    def execute(self) -> None:
        '''
        Called repeatably when this command is scheduled to run.
        '''
        log.debug(f"l {self.controller['left']}, r {self.controller['right']}")
        self.controller['dt'].drive(self.controller['left'], self.controller['right'])

    def end(self, interrupted: bool) -> None:
        '''
        Safe drive train when ending
        '''
        self.controller['dt'].drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False
