#import commands2
import wpimath.geometry
from typing import Callable
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain


class PathFinder():
    def __init__(self, driveTrain:DriveTrain, getInitPos:Callable, finalPos:wpimath.geometry.Pose2d):
        '''starting with moving a few ft forward, this will change'''
        self.driveTrain = driveTrain
        self.getInitPos = getInitPos
        self.finalPos = finalPos
        self.initPos = self.getInitPos()

    def execute(self):
        self.initPos = self.getInitPos()
        self.dist = self.initPos.translation().toTranslation2d().distance(self.finalPos.translation())
        print(self.dist)
        if(self.dist > 0.1 or True):
            print("i should be driving")
            self.driveTrain.drive(0.5, 0.5)
