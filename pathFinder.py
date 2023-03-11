import commands2
import wpimath.geometry
from typing import Callable
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain


class PathFinder():
    def __init__(self, driveTrain:DriveTrain, getInitPos:Callable, finalPos:wpimath.geometry.Pose2d):
        '''starting with moving 3ft forward, this will change'''
        self.driveTrain = driveTrain
        self.getInitPos = getInitPos
        self.finalPos = finalPos
        self.initPos = self.getInitPos()

    def execute(self):
        self.initPos = self.getInitPos()
        self.dist = self.initPos.translation().distance(self.finalPos.translation())
        if(self.dist > 0):
            self.driveTrain.drive(0.5, 0.5)