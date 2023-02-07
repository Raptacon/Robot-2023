import commands2
import time

from typing import Callable

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
            self.startedTime = time.time()
            print(f"setting start time: {self.startedTime}")

        elapsedTime = time.time() - self.startedTime
        if elapsedTime <= 5: 
            self.driveForward()
        elif elapsedTime <= 10:
            self.turnLeft()
        elif elapsedTime <= 15:
            self.turnRight()
        elif elapsedTime <= 20:
            self.driveBackwards()
        elif elapsedTime > 20:
            self.stop


    def driveForward(self) -> None:
        self.driveTrain.drive(1, 1)

    def driveBackwards(self) -> None:
        self.driveTrain.drive(-1, -1)

    def turnLeft(self) -> None:
        self.driveTrain.drive(0,1)

    def turnRight(self) -> None:
        self.driveTrain.drive(1,0)

    def stop(self) -> None:
        self.driveTrain.drive(0, 0)

    def isFinished(self) -> bool:
        '''Run until interrupted'''
        return False
