import navx
from swerve.swerveModule import SwerveModuleMk4L1FalcFalcCanCoder as SwerveModule

import wpilib
import commands2
import wpimath.kinematics
from wpimath.geometry import Rotation2d
import math

class Drivetrain(commands2.SubsystemBase):
    kMaxVoltage = 12.0
    kWheelBaseMeters = 0.5461 # front to back distance
    kTrackBaseMeters = 0.5461 # left to right distance
    kMaxVelocityMPS = 4.14528
    kMaxAngularVelocityRadPS = kMaxVelocityMPS / math.hypot(kWheelBaseMeters / 2.0, kTrackBaseMeters / 2.0)

    kModuleProps = [
            {"name": "frontLeft", "channel": 50, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "frontRight", "channel": 53, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": kWheelBaseMeters/2.0 },
            {"name": "rearLeft", "channel": 56, "encoderCal": 0.0, "trackbase": kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 },
            {"name": "readRight", "channel": 59, "encoderCal": 0.0, "trackbase": -kTrackBaseMeters/2.0, "wheelbase": -kWheelBaseMeters/2.0 }
    ]

    def __init__(self):
        super().__init__()
        self.swerveModules = []
        for module in Drivetrain.kModuleProps:
            name = module["name"]
            wheelbase = module["wheelbase"]
            trackbase = module["trackbase"]
            channel = module["channel"]
            encoderCal = module["encoderCal"]
            self.swerveModules.append(SwerveModule((trackbase, wheelbase, name), channel, encoderCal))

        self.imu = navx.AHRS.create_spi()

        self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(
            self.swerveModules[0].getTranslation(),
            self.swerveModules[1].getTranslation(),
            self.swerveModules[2].getTranslation(),
            self.swerveModules[3].getTranslation()
        )

        self.odometry = wpimath.kinematics.SwerveDrive4Odometry(self.kinematics, self.getHeading())


    def getHeading(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.imu.getFusedHeading())

    def drive(self, xSpeed: float, ySpeed: float, rot: float, fieldRelative: bool):
        chassisSpeeds = None
        if fieldRelative:
            chassisSpeeds = wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rot)
        else:
            chassisSpeeds = wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(xSpeed, ySpeed, rot, self.getHeading())
        swerveModuleStates = self.kinematics.toSwerveModuleStates(chassisSpeeds)
        self.kinematics.desaturateWheelSpeeds(swerveModuleStates)

        for mod, state in zip(self.swerveModules, swerveModuleStates):
            mod.setDesiredState(state)

    def updateOdometry(self):
        self.odometry.update(self.getHeading(),
                             self.swerveModules[0].getPosition(),
                             self.swerveModules[1].getPosition(),
                             self.swerveModules[2].getPosition(),
                             self.swerveModules[3].getPosition())