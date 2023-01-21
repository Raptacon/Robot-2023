import wpilib
import commands2

from typing import Callable

class ArcadeDrive(commands2.CommandBase):
    '''
    Command for converting joystick input to drive train output
    '''
    def __init__(self, speed: Callable[[], float], mix: Callable[[], float], driveTrain):
        '''
        Takes a left, right callerable to get tank drive controls
        Takes driveTrain on which to operate. Requires drive train with left, right drive call.
        Update to support other types in future? X, Y?
        '''
        super().__init__()
        self.speed = speed
        self.mix = mix
        self.driveTrain = driveTrain

        #setup subsystem
        self.addRequirements(self.driveTrain)

    def execute(self) -> None:
        '''
        Called repeatably when this command is scheduled to run.
        '''
        speed = self.speed()
        mix = self.mix()
        left = speed * mix
        right = speed * -mix
        print(f"l {left}, r {right}")
        self.driveTrain.drive(left, right)

    def end(self, interrupted: bool) -> None:
        '''
        Safe drive train when ending
        '''

        self.driveTrain.drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False