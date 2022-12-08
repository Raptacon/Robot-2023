from enum import Enum, auto
import ctre
from cmath import sqrt
import logging as log
from networktables import NetworkTables

class ControlMode(Enum):
    """
    Drive Train Control Modes
    """
    kArcadeDrive = auto()
    kTankDrive = auto()
    kSwerveDrive = auto()
    kDisabled = auto()

class DriveTrain():
    motors_driveTrain: dict
    gearRatio = 10
    driveMotorsMultiplier = .7
    creeperMotorsMultiplier = .25

    smartDashTable = NetworkTables.getTable("SmartDashboard")

    def setup(self):
        self.motorSpeedInfo = {}
        self.creeperMode = False
        log.info("DriveTrain setup completed")

    def setMotors(self, motorSpeedInfo:dict):
        self.motorSpeedInfo = motorSpeedInfo

    def setBraking(self, braking:bool):
        if braking:
            for motor in self.motors_driveTrain.keys():
                self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Brake)
        else:
            for motor in self.motors_driveTrain.keys():
                self.motors_driveTrain[motor].setNeutralMode(ctre.NeutralMode.Coast)

    def getSpecificMotor(self, motorName):
        try:
            return self.motors_driveTrain[motorName].get()
        except:
            return

    def setDriveMotorsMultiplier(self, MotorsMultiplier:float):
        self.driveMotorsMultiplier = MotorsMultiplier

    def setcreeperMotorsMultiplier(self, MotorsMultiplier:float):
        self.creeperMotorsMultiplier = MotorsMultiplier

    def stop(self):
        self.motorSpeedInfo = {}
        for key in self.motors_driveTrain.keys():
            self.motorSpeedInfo[key] = 0

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

    def execute(self):

        # Make sure motors are the same between parameter information and drivetrain
        # then set motors
        speedInfoKeys = sorted(dict(self.motorSpeedInfo).keys())
        driveTrainKeys = sorted(self.motors_driveTrain.keys())
        if speedInfoKeys != driveTrainKeys:
            print("not Matching")
            self.stop()
            speedInfoKeys = sorted(dict(self.motorSpeedInfo).keys())

        for key in speedInfoKeys:
            self.motors_driveTrain[key].set(self.motorSpeedInfo[key])
