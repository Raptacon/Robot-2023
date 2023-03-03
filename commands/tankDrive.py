import commands2
import logging
from typing import Callable
import wpilib
log = logging.getLogger(__name__)
class TankDrive(commands2.CommandBase):
    '''
    Command for converting joystick input to drive train output
    '''
    def __init__(self, left: Callable[[], float], right: Callable[[], float], creeperMode: Callable[[], bool], driveTrain):
    #TODO replace crepper with command instead of bypassing commands
        '''
        Takes a left, right callerable to get tank drive controls
        Takes driveTrain on which to operate. Requires drive train with left, right drive call.
        Update to support other types in future? X, Y?
        '''
        super().__init__()
        self.left = left
        self.right = right
        self.driveTrain = driveTrain
        self.creeperMode = creeperMode
        #setup subsystem
        self.addRequirements(self.driveTrain)

    def execute(self) -> None:
        '''
        Called repeatably when this command is scheduled to run.
        '''
        left = self.left() * self.getCreeperMultiplier()
        right = self.right() * self.getCreeperMultiplier()
        log.debug(f"l {left}, r {right}")
        self.driveTrain.drive(left, right)

    def getCreeperMultiplier(self) -> float:
        creeperMode = self.creeperMode()
        print(creeperMode)
        if creeperMode:
            return float(wpilib.SmartDashboard.getNumber("CreeperMode Multiplier", .5))
        else:
            return 1

    def end(self, interrupted: bool) -> None:
        '''
        Safe drive train when ending
        '''
        self.driveTrain.drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False
