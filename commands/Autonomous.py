import commands2
import time
from threading import Timer

# from typing import Callable

class Autonomous(commands2.CommandBase):
    
    def __init__(self, driveTrain):
        '''
        Takes a left, right callerable to get tank drive controls
        Takes driveTrain on which to operate. Requires drive train with left, right drive call.
        Update to support other types in future? X, Y?
        '''

        super().__init__()
        self.driveTrain = driveTrain

        #setup subsystem
        self.addRequirements(self.driveTrain)

        self.startedTime = 0

    def execute(self):
        if self.startedTime == 0:
            return
        elapsedTime = time.time() - self.startedTime 
        if elapsedTime <= 2: 
            self.driveForward()
        elif elapsedTime <= 4:
            self.turnLeft()
        elif elapsedTime <= 6:
            self.turnRight()
        elif elapsedTime <= 8:
            self.driveBackwards()
        elif elapsedTime > 10:
            self.stop
            self.startedTime = 0

    def schedule(self):
        self.startedTime = time.time()
        
    def setDirection(self, direction):
        self.driveDirection = direction


    def driveForward(self) -> None:
        self.driveTrain.drive(.5, -.5)

    def driveBackwards(self) -> None:
        self.driveTrain.drive(-.5, -.5)

    def turnLeft(self) -> None:
        self.driveTrain.drive(0,-.5)

    def turnRight(self) -> None:
        self.driveTrain.drive(.5,0)

    def stop(self) -> None:
        self.driveTrain.drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False
