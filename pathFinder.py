#import commands2
import wpimath.geometry
#from typing import Callable
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain
import aprilTags

'''
The pathfinder class uses the information obtained by the april tag class to navigate to a new position
'''
class PathFinder():
    '''
    Params:
        a drive train object from the drive train class
        a wpimath.geometry.pose2d that indicates where the robot should end up
        an april tag object from the april tag class
    '''
    def __init__(self, driveTrain:DriveTrain, finalPos:wpimath.geometry.Pose2d, apriltags:aprilTags.AprilTags):
        '''Makes variables class variable'''
        self.driveTrain = driveTrain
        self.finalPos = finalPos
        self.apriltags = apriltags
        '''gets the current robot pose'''
        self.initPos = self.apriltags.updatePose()

        '''each variable keeps track of whether or not a certain action has been preformed, true means the action needs to be performed'''
        self.drive = True
        self.turn = True

        '''gets the degree that it needs to turn to'''
        self.initPosAng = self.initPos.toPose2d().rotation().degrees()
        self.finalPosAng = self.finalPos.rotation().degrees()
        

        '''temp variables that make the printing further along more usefull'''
        self.i = 0
        self.j = 0
        

    def driveToFinal(self):
        '''
        params: none
        return: none
        effect: makes the driveTrain drive forward

        makes the drive train dirve forward at different speeds depending on how close it is to the destination
        '''

        '''gets the current position'''
        self.initPos = self.apriltags.updatePose()

        '''gets the distance to the wanted pose'''
        self.Xdist = abs(self.finalPos.X()- self.initPos.X())

        '''prints, but not every time execute is called'''
        self.i += 1
        if self.i % 3 == 0:
            print("Distance")
            print("---------")
            print(f"{self.Xdist} | {self.initPos.translation().X()} | {self.initPos.translation().Y()}")
            print(f"{self.finalPos.translation().X()} | {self.finalPos.translation().Y()}")

        '''checks the distance to the wanted pos, drives at a different speed so we don't overshoot'''
        # could add a backwards movement if we overshoot or get hit too far
        if(self.Xdist > 0.5 and self.drive):
            self.driveTrain.drive(0.5, 0.5)
        elif(self.Xdist > 0.15 and self.drive):
            self.driveTrain.drive(0.3, 0.3)
        else:
            self.driveTrain.drive(0,0)
            self.drive = False

    def turnToFinal(self):
        '''turns to the angle given in the wanted pos'''

        '''get's the robots psoe'''
        self.initPos = self.apriltags.updatePose()
        self.initPosAng = self.initPos.toPose2d().rotation().degrees()

        '''gets the distance between the angles so we can see how close we are'''
        angDist = abs(self.finalPosAng - self.initPosAng)

        '''prints, but not everytime the method is called'''
        if self.j % 3 == 0:
            print(self.initPosAng)
            print(angDist)

        '''code that should make it turn in the right direction'''
        #I beleive this doesnt work right
        self.direction = "right"
        if(self.finalPosAng > self.initPosAng):
            self.direction = "left"

        '''WIP turning, will turn at different speeds to we don't over shoot'''
        # Greenbot motors break when trying to go backwards, which is why there are 0s in the drives, should be the negative of the other value
        if(self.direction == "right" and self.turn and angDist > 1.5):
            self.driveTrain.drive(0, 0.3)
        elif(self.direction == "left" and self.turn and angDist > 1.5):
            self.driveTrain.drive(0.3, 0) 
        else:
            self.driveTrain.drive(0,0)
            self.turn = False
    
    def turnToPos(self):
        '''turns to look at the wanted pos so we can drive there'''
        '''code that should make it turn in the right direction'''
        #I beleive this doesnt work right
        self.direction = "right"
        if(self.finalPosAng > self.initPosAng):
            self.direction = "left"
        pass

    def execute(self):
        '''runs the path finder code'''
        self.initPos = self.apriltags.updatePose()

        ''''''
        self.Xdist = abs(self.finalPos.X()- self.initPos.X())
        self.i += 1
        if self.i % 3 == 0:
            print("Distance")
            print("---------")
            print(f"{self.Xdist} | {self.initPos.translation().X()} | {self.initPos.translation().Y()}")
            print(f"{self.finalPos.translation().X()} | {self.finalPos.translation().Y()}")
        
        
        
        # if(self.turn):
        #     self.turnToFinal()
        # elif(self.drive):
        #     self.driveToFinal()