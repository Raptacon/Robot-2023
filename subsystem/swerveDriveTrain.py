import navx
from swerve.swerveModule import SwerveModuleMk4L1FalcFalcCanCoder as SwerveModule

import commands2
import wpimath.kinematics
from wpimath.geometry import Rotation2d
import math
import wpilib

from networktables import NetworkTables

class Drivetrain(commands2.SubsystemBase):
    kMaxVoltage = 12.0
    kWheelBaseMeters = 0.5461 # front to back distance
    kTrackBaseMeters = 0.5461 # left to right distance
    #kMaxVelocityMPS = 4.14528
    kMaxVelocityMPS = 1.0
    kMaxAngularVelocityRadPS = kMaxVelocityMPS / math.hypot(kWheelBaseMeters / 2.0, kTrackBaseMeters / 2.0)

    kModuleProps = [
            {"name": "frontLeft", "channel": 50, "encoderCal": 244.5, "trackbase": kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "frontRight", "channel": 53, "encoderCal": 334.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "rearLeft", "channel": 56, "encoderCal": 121.5, "trackbase": kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 },
            {"name": "rearRight", "channel": 59, "encoderCal": 211.5, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 }
    ]
    kModulePropsNoCal = [
            {"name": "frontLeft", "channel": 50, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "frontRight", "channel": 53, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "rearLeft", "channel": 56, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 },
            {"name": "rearRight", "channel": 59, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 }
    ]


#52 - -181.2
#58 -  128.0
#55 - -294.4
#61 - -273.4

#new offests as of 6/30/2023 for swerve chasis
#52 - 31.992
#55 - 153.193
#58 - -23.555
#61 - 34.717
    def __init__(self):
        super().__init__()
        self.swerveModules = []
        NetworkTables.initialize()
        self.table = NetworkTables.getTable("Drivetrain")
        assert(self.table)
        for module in Drivetrain.kModulePropsNoCal:
            name = module["name"]
            subTable = self.table.getSubTable(name)
            assert(subTable)
            wheelbase = module["wheelbase"]
            trackbase = module["trackbase"]
            channel = module["channel"]
            encoderCal = module["encoderCal"]
            self.swerveModules.append(SwerveModule((trackbase, wheelbase, name), channel, encoderCal, subTable))

        self.imu = navx.AHRS.create_spi()

        self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(
            self.swerveModules[0].getTranslation(),
            self.swerveModules[1].getTranslation(),
            self.swerveModules[2].getTranslation(),
            self.swerveModules[2].getTranslation()
        )

        self.odometry = wpimath.kinematics.SwerveDrive4Odometry(self.kinematics, self.getHeading())
        self.setFieldDriveRelative(False)
        self.ang = 0
        self.iteration = 0


    def getHeading(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.imu.getFusedHeading())

    def drive(self, xSpeed: float, ySpeed: float, rot: float, fieldRelative: bool):
        #convert to proper units
        rot = rot * 180.0

        #print(f"drive: x {xSpeed}, y {ySpeed}, rot {rot}, field {fieldRelative}")
        #xSpeed = 0.0
        #ySpeed = 0.0
        #rot = self.ang
        #rot = rot * 360
        #self.ang += 1.0
        #rot = int(rot) % 180
        #self.iteration += 1
        #if(self.iteration % 100 == 0):
        #    print(f"drive: x {xSpeed}, y {ySpeed}, rot {rot}, field {fieldRelative}, speed {xSpeed * self.kMaxVoltage}")


        #for mod in self.swerveModules:
        #    mod.set(xSpeed * self.kMaxVoltage, rot)

        #return

        chassisSpeeds = None
        if not fieldRelative:
            #print("robot relative")
            chassisSpeeds = wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rot)
        else:
            #print("field relative")
            chassisSpeeds = wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(xSpeed, ySpeed, rot, self.getHeading())

        swerveModuleStates = self.kinematics.toSwerveModuleStates(chassisSpeeds)
        self.kinematics.desaturateWheelSpeeds(swerveModuleStates, self.kMaxVelocityMPS)

        for mod, state in zip(self.swerveModules, swerveModuleStates):
            mod.setSwerveModuleState(state, self.kMaxVelocityMPS)

    def updateOdometry(self):
        self.odometry.update(self.getHeading(),
                             self.swerveModules[0].getPosition(),
                             self.swerveModules[1].getPosition(),
                             self.swerveModules[2].getPosition(),
                             self.swerveModules[3].getPosition())
    def disable(self, steer = True, drive = True):
        for m in self.swerveModules:
            m.disable(steer, drive)

    def setSteer(self, angle : float):
        angle %= 360
        for m in self.swerveModules:
            m.setSteerAngle(angle)

    def getCurrentAngles(self):
        angles = []
        for m in self.swerveModules:
            angle = m.getCurrentAngle()
            wpilib.SmartDashboard.putNumber(f"{m.cancoderId}Pos", angle)
            angles.append(angle)
        return angles


    def setDrive(self, speedPercent: float):
        if speedPercent> 100:
            speedPercent = 100
        for m in self.swerveModules:
            m.setDrivePercent(speedPercent)

    def setFieldDriveRelative(self, state: bool):
        self.fieldRelative = state
        wpilib.SmartDashboard.putBoolean("Field Relative", state)

    def getFieldDriveRelative(self) -> bool:
        return self.fieldRelative

    def calWheels(self, enable):
        for m in self.swerveModules:
            m.setCal(enable)
