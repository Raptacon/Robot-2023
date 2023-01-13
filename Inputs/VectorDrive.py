from Inputs.InputXYR import XYRInput
from utils.motorEnums import Tank, TwoMotorTank
import logging as log
from magicbot import AutonomousStateMachine, MagicRobot
from networktables import NetworkTables
from utils.motorHelper import WPI_TalonFXFeedback
import ctre

class TankDrive:

    compatString = ["doof","teapot","greenChassis", "minibot"]
    # Note - The way we will want to do this will be to give this component motor description dictionaries from robotmap and then creating the motors with motorhelper. After that, we simply call wpilib' differential drive
    driveMotorsMultiplier = .7
    creeperMotorsMultiplier = .25

    smartDashTable = NetworkTables.getTable("SmartDashboard")

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

        lmotor *= self.driveMotorsMultiplier
        rmotor *= self.driveMotorsMultiplier

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
    SwerveDrive = SwerveDrive()
    TwoMotorTankDrive = TwoMotorTankDrive()
    Motorspeeds = {}
    currentSource = None
    prevSource = None
    controlMode = None
    motors_driveTrain: dict

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

    def setup(self):
        self.motorSpeedInfo = {}
        self.creeperMode = False
        log.info("DriveTrain setup completed")

    def setBraking(self, braking:bool):
        """
        This isn't incorporated into the handler
        (I'm not sure if it should be)
        """
        if braking:
            for motor in self.motors_driveTrain.keys():
                if type(self.motors_driveTrain[motor]) == WPI_TalonFXFeedback:
                    self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Brake)
        else:
            for motor in self.motors_driveTrain.keys():
                if type(self.motors_driveTrain[motor]) == WPI_TalonFXFeedback:
                    self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Coast)

    def setMotors(self, motorSpeedInfo:dict):
        """
        DO NOT CALL THIS, ONLY THE HANDLER SHOULD HAVE CONTROL
        Accepts motorSpeedInfo, a dictionary of motor names and speeds.
        """
        self.motorSpeedInfo = motorSpeedInfo

    def getSpecificMotor(self, motorName):
        """
        returns object for motorName
        if no object exists, returns nothing
        """
        try:
            return self.motors_driveTrain[motorName].get()
        except:
            return

    def enableCreeperMode(self):
        """when left bumper is pressed, it sets the driveMotorsMultiplier to .25"""
        if self.creeperMode:
            return
        self.prevMultiplier = self.driveMotorsMultiplier
        self.driveMotorsMultiplier = self.creeperMotorsMultiplier
        self.creeperMode = True

    def disableCreeperMode(self):
        """when left bumper is released, it sets the multiplier back to it's original value"""
        if not self.creeperMode:
            return
        self.driveMotorsMultiplier = self.prevMultiplier
        self.creeperMode = False

    def stop(self):
        self.motorSpeedInfo = {}
        for key in self.motors_driveTrain.keys():
            self.motorSpeedInfo[key] = 0

    def getSpecificMotorDistTraveled(self, motorName):
        """
        Returns a specific motor's distance traveled
        (Only works with Falcon 500s)
        """
        if type(self.motors_driveTrain[motorName]) == WPI_TalonFXFeedback:
            # self.leftDistInch = (self.motors_driveTrain[motorName].getPosition(0, positionUnits.kRotations) / self.gearRatio) * self.wheelCircumference
            if self.leftSideSensorInverted:
                return -1 * self.leftDistInch
            else:
                return self.leftDistInch
        return 0

    def resetMotorsDistTraveled(self):
        for motor in self.motors_driveTrain.keys():
            if type(self.motors_driveTrain[motor]) == self.WPI_TalonFXFeedback:
                motor.resetPosition()

    def resetSpecificMotorDistTraveled(self, motorName):
        if type(self.motors_driveTrain[motorName]) == self.WPI_TalonFXFeedback:
            self.motors_driveTrain[motorName].resetPosition()

    def execute(self):

        self.setMotors(self.Motorspeeds)
        self.run()
        self.Motorspeeds = {}

        # You must request control every frame.
        self.prevSource = self.currentSource
        self.currentSource = None

    def run(self):
        # Make sure motors are the same between parameter information and drivetrain
        # then set motors
        speedInfoKeys = sorted(dict(self.motorSpeedInfo).keys())
        driveTrainKeys = sorted(self.motors_driveTrain.keys())
        if speedInfoKeys != driveTrainKeys:
            print("Not Matching!")
            self.stop()
            speedInfoKeys = sorted(dict(self.motorSpeedInfo).keys())

        for key in speedInfoKeys:
            self.motors_driveTrain[key].set(self.motorSpeedInfo[key])
