from Inputs.InputXYR import XYRInput
from DriveTrain import DriveTrain
from utils.motorEnums import Tank, Swerve, TwoMotorTank
import logging as log
import math
from magicbot import AutonomousStateMachine, MagicRobot

class TankDrive:

    def MotorDrive(self, x,y,r):
        maximum = max(abs(y),abs(r))
        total = y+r
        dif = y-r
        if y >= 0:
            if r >= 0:  # I quadrant
                lmotor = maximum
                rmotor = dif
            else:            # II quadrant
                lmotor = total
                rmotor = maximum
        else:
            if r >= 0:  # IV quadrant
                lmotor = total
                rmotor = -1*maximum
            else:            # III quadrant
                lmotor = -1*maximum
                rmotor = dif

        lmotor *= DriveTrain.driveMotorsMultiplier
        rmotor *= DriveTrain.driveMotorsMultiplier

        return {Tank.FrontLeft.value : lmotor,
                Tank.BackLeft.value : lmotor,
                Tank.BackRight.value : rmotor,
                Tank.FrontRight.value : rmotor}

class TwoMotorTankDrive(TankDrive):
    def MotorDrive(self, x, y ,r):
        superOutput = TankDrive.MotorDrive(self, x, y, r)
        return {TwoMotorTank.Left.value:superOutput[Tank.FrontLeft.value],
                TwoMotorTank.Right.value:superOutput[Tank.FrontRight.value]}

class SwerveDrive:
    """
    L = 30
    W = 30

    def MotorDrive(self, x,y,r):
        optimizedStates = movementKinematics.transformations(x,y,r)

        backRightSpeed = optimizedStates[3].speed
        backLeftSpeed = optimizedStates[2].speed
        frontRightSpeed = optimizedStates[1].speed
        frontLeftSpeed = optimizedStates[0].speed

        currentAngle = moduleStates()

        backRightAngle = math.atan2 (a, d) / math.pi
        backLeftAngle = math.atan2 (a, c) / math.pi
        frontRightAngle = math.atan2 (b, d) / math.pi
        frontLeftAngle = math.atan2 (b, c) / math.pi
        return {Swerve.BackRight.value:backRightSpeed,
                Swerve.BackLeft.value:backLeftSpeed,
                Swerve.FrontRight.value:frontRightSpeed,
                Swerve.FrontLeft.value:frontLeftSpeed,
                Swerve.BackRightRotation.value:backRightAngle,
                Swerve.BackLeftRotation.value:backLeftAngle,
                Swerve.FrontRightRotation.value:frontRightAngle,
                Swerve.FrontLeftRotation.value:frontLeftAngle}
        """

class XYRDrive:
    driveTrainType: str
    TankDrive = TankDrive()
    driveTrain = DriveTrain()
    SwerveDrive = SwerveDrive()
    TwoMotorTankDrive = TwoMotorTankDrive()
    Motorspeeds = {}
    currentSource = None
    prevSource = None
    controlMode = None

    def __init__(self):
        self.transformDict = {"Tank":self.TankDrive, "Swerve":self.SwerveDrive, "TwoMotorTank":self.TwoMotorTankDrive}
    def xyrdrive(self, requestSource, vector:XYRInput):
        """
        Pass in self as requestSource
        """

        transformKey = self.driveTrainType

        if transformKey in self.transformDict.keys():
            transformer = self.transformDict[transformKey]
            self.setDriveTrain(requestSource, transformer.MotorDrive(vector.getX(), vector.getY(), vector.getR()))
        else:
            log.error("Unrecognized drivetrain type "+str(self.driveTrainType))

    def setDriveTrain(self, requestSource, Motorspeeds):
        if self.currentSource != requestSource:
            self.requestControl(requestSource)

        if self.currentSource == requestSource:
            self.Motorspeeds = Motorspeeds
            return True
        else:
            return False

    def requestControl(self, requestSource):
        """
        (The preferred way to gain control is to call the set method,
        which will request control through this method anyway.)
        This method will request control of the drivetrain. If
        your request is approved (True is returned),
        then you can call the set method to
        get the DriveTrain to move.
        Only call when you want to access drivetrain.
        Priority Tree:
        High Priority:
        Driver input
        Low Priority:
        Everything Else
        (Priority is given to components who held control on previous frame)
        (Therefor, control is given to components who request control first immediately after
        driver control is relinquished. Play nice, I guess.)
        """
        # If the request comes from a descendant of MagicRobot
        # (If the request comes from robot.py)
        # give it control
        if issubclass(type(requestSource), MagicRobot):
            self.currentSource = requestSource
            return True
        if issubclass(type(requestSource), AutonomousStateMachine):
            self.currentSource = requestSource
            return True

        # I think this works.
        elif self.currentSource == None:
            if self.prevSource == None:
                self.currentSource = requestSource
                return True
            elif self.prevSource == requestSource:
                self.currentSource = requestSource
                return True
            else:
                return False

        else:
            return False

    def execute(self):
        self.driveTrain.setMotors(self, self.Motorspeeds)

        self.Motorspeeds = {}

        # You must request control every frame.
        self.prevSource = self.currentSource
        self.currentSource = None