
import math
import phoenix5
from phoenix5 import sensors
import wpimath.geometry
import wpimath.kinematics
import wpimath.controller
import rev
import logging as log
import utils.sparkMaxUtils

from .steerController import SteerController
import ntcore

'''
This is a basic swerve drive module for a robot running
https://www.swervedrivespecialties.com/products/mk4-swerve-module
with L1 standard and 2 falcon 500
https://store.ctr-electronics.com/falcon-500-powered-by-talon-fx/
and a
https://store.ctr-electronics.com/cancoder/
Other defaults may be added in future

Constants used from https://github.com/SwerveDriveSpecialties/swerve-lib/tree/develop/src
'''

class SwerveModuleConsts():
    '''Not a valid class. Requires inherited class'''
    _wheelDiameter = math.nan
    _driveReduction = math.nan
    _driveInverted = None
    _steerReduction = math.nan
    _steerInverted = None
    _moduleType = None

    def __init__():
        '''pass'''
        pass

    def getWheelDiameter(self) -> float:
        ''' returns wheel diameter'''
        return self._wheelDiameter
    def getDriveReduction(self) -> float:
        ''' returns drive reduction'''
        return self._driveReduction
    def getSteerReduction(self) -> float:
        ''' returns drive reduction'''
        return self._steerReduction
    def getSteerInverted(self) -> bool:
        ''' returns steer inversion'''
        return self._steerInverted
    def getDriveInverted(self) -> bool:
        ''' returns drive inversion'''
        return self._driveInverted
    def __str__(self):
        return f"{self._moduleType}: Drive Reduction {self._driveReduction}, \
            Drive Inverted {self._driveInverted}, Steer Reduction {self._steerReduction}, \
            steer inverted {self._steerInverted}, wheel diameter {self. _wheelDiameter}"

class SwerveModuleMk4L1Consts(SwerveModuleConsts):
    '''
    https://github.com/SwerveDriveSpecialties/swerve-lib/blob/f6f4de65808d468ed01cc5ca39bf322383838fcd/src/main/java/com/swervedrivespecialties/swervelib/SdsModuleConfigurations.java#L19
        public static final ModuleConfiguration MK4_L1 = new ModuleConfiguration(
            0.10033,
            (14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0),
            true,
            (15.0 / 32.0) * (10.0 / 60.0),
            true
    );
    wheelDiameter, driveDreuction, driveInverted, steerReduction, steerInverted
        '''
    def __init__(self) -> None:
        '''init Mk4L1 values'''
        self._wheelDiameter = 0.10033
        self._driveReduction = (14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)
        self._steerReduction = (15.0 / 32.0) * (10.0 / 60.0)
        self._steerInverted = True
        self._moduleType = "Mk4L1"

class SwerveModuleMK4I_L2Consts(SwerveModuleConsts):
    '''
    https://github.com/SwerveDriveSpecialties/swerve-lib/blob/f6f4de65808d468ed01cc5ca39bf322383838fcd/src/main/java/com/swervedrivespecialties/swervelib/SdsModuleConfigurations.java#L19
        public static final ModuleConfiguration MK4_L1 = new ModuleConfiguration(
            0.10033,
            (14.0 / 50.0) * (27.0 / 17.0) * (15.0 / 45.0),
            true,
            (14.0 / 50.0) * (10.0 / 60.0),
            false
    );
    wheelDiameter, driveDreuction, driveInverted, steerReduction, steerInverted
        '''
    def __init__(self) -> None:
        '''init Mk4I_L2 values'''
        self._wheelDiameter = 0.10033
        self._driveReduction = (14.0 / 50.0) * (27.0 / 17.0) * (15.0 / 45.0)
        self._steerReduction = (14.0 / 50.0) * (10.0 / 60.0)
        self._steerInverted = False
        self._moduleType = "Mk4I_L2"



class SwerveModuleMk4L1SparkMaxNeoCanCoder() :
    '''
    Module for Mk4L1 with 2 brushless neos and a cancoder swerve drive
    '''
    driveId : int
    steerId: int
    cancoderId: int
    encoder : sensors.CANCoder

    kNominalVoltage = 12.0
    kDriveCurrentLimit =  20.0
    kSteerCurrentLimit = 20.0

    ''' https://github.com/SwerveDriveSpecialties/swerve-lib/blob/develop/src/main/java/com/swervedrivespecialties/swervelib/ctre/Falcon500DriveControllerFactoryBuilder.java '''
    kTicksPerRotation = 1
    kCanTimeoutMs = 250
    kStatusFrameGeneralPeriodMs = 250
    kSteerPID = (0.2, 0.0, 0.1)
    kCanStatusFrameMs = 10

    def __init__(self, location : tuple[float, float, str], channelBase: int, inverted, encoderCal: float = 0, table = ntcore.NetworkTable):
        '''
        Creates a new swerve module at location in robot. With channesl channelBase = drive
        channelBase + 1 = steer
        channelBase + 2 = cancoder
        and the encoders rotated by encoderCal.
        location [x (trackbase + is left side), y (wheelbase + is front), name]
        '''
        self.consts = SwerveModuleMK4I_L2Consts()
        self.driveId = channelBase + 0
        self.steerId = channelBase + 1
        self.cancoderId = channelBase + 2
        self.name = location[2]
        self.table = table
        self.translation = wpimath.geometry.Translation2d(location[0], location[1])
        self.distTraveled = 0
        self.driveVoltage = 0.0

        #create can encoder
        self.encoder = sensors.WPI_CANCoder(self.cancoderId)
        encoderConfig = sensors.CANCoderConfiguration()
        encoderConfig.absoluteSensorRange = sensors.AbsoluteSensorRange.Unsigned_0_to_360
        encoderConfig.magnetOffsetDegrees = encoderCal
        encoderConfig.sensorDirection = True
        status = self.encoder.configAllSettings(encoderConfig, 250)
        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure CAN encoder on id {self.cancoderId}. Error {status}")
        status = self.encoder.setStatusFramePeriod(sensors.CANCoderStatusFrame.SensorData, self.kCanStatusFrameMs, 250)
        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure CAN encoder on status frame on id {self.cancoderId}. Error {status}")

        #create drive motor
        self.driveSensorPositionCoefficient = math.pi * self.consts.getWheelDiameter() * self.consts.getDriveReduction() / self.kTicksPerRotation
        self.driveSensorVelocityCoefficient = self.driveSensorPositionCoefficient * 10.0
        motorConfig = phoenix5.TalonFXConfiguration()
        motorConfig.voltageCompSaturation = self.kNominalVoltage
        supplyCurrConfig = phoenix5.SupplyCurrentLimitConfiguration()
        supplyCurrConfig.currentLimit = self.kDriveCurrentLimit
        supplyCurrConfig.enable = True
        motorConfig.supplyCurrLimit = supplyCurrConfig

        self.driveMotor = rev.CANSparkMax(self.driveId, rev.CANSparkLowLevel.MotorType.kBrushless)
        utils.sparkMaxUtils.configureSparkMaxCanRates(self.driveMotor)
        self.driveMotor.setInverted(inverted)

        # status = self.driveMotor.configAllSettings(motorConfig, 250)

        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Drive Motor on id {self.driveId}. Error {status}")
        self.driveMotor.enableVoltageCompensation(12.0)
        # self.driveMotor.setNeutralMode(ctre.NeutralMode.Brake)
        # Inversion should come on a motor by motor basis
        # self.driveMotor.setInverted(self.consts.getDriveInverted())
        self.driveEncoder = self.driveMotor.getAbsoluteEncoder(rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle)
        # self.driveMotor.setSensorPhase(True)

        status = phoenix5.ErrorCode.OK # self.driveMotor.setStatusFramePeriod(ctre.StatusFrameEnhanced.Status_1_General, self.kCanStatusFrameMs, 250)

        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Drive Motor Status Frame on id {self.driveId}. Error {status}")

        #create steer motor
        self.steerSensorPositionCoefficient = 2.0 * math.pi / self.kTicksPerRotation * self.consts.getSteerReduction()
        self.steerSensorVelocityCoefficient = self.steerSensorPositionCoefficient * 10.0
        self.steerMotor = rev.CANSparkMax(self.steerId, rev.CANSparkLowLevel.MotorType.kBrushless)

        utils.sparkMaxUtils.configureSparkMaxCanRates(self.steerMotor)
        self.steerEncoder = self.encoder

        # motorConfig = ctre.TalonFXConfiguration()
        # motorConfig.slot0.kP = self.kSteerPID[0]
        # motorConfig.slot0.kI = self.kSteerPID[1]
        # motorConfig.slot0.kD = self.kSteerPID[2]
        # motorConfig.voltageCompSaturation = self.kNominalVoltage
        # supplyCurrConfig.currentLimit = self.kSteerCurrentLimit
        # motorConfig.supplyCurrLimit = supplyCurrConfig

        # status = self.steerMotor.configAllSettings(motorConfig, 250)

        self.steerPIDController = wpimath.controller.PIDController(0.3 ,1 ,0)#Test Values P: 0.3, I: 1, D: 0
        self.steerPIDController.setTolerance(0.008)

        status = phoenix5.ErrorCode.OK
        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor on id {self.steerId}. Error {status}")

        # self.steerMotor.enableVoltageCompensation(True)

        # status = self.steerMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 250)
        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor Feedback on id {self.steerId}. Error {status}")
        # self.steerMotor.setSensorPhase(True)
        self.steerMotor.setInverted(self.consts.getSteerInverted())
        # self.steerMotor.setNeutralMode(ctre.NeutralMode.Brake)
        # status = self.steerMotor.setSelectedSensorPosition(self.getAbsoluteAngle() / self.steerSensorPositionCoefficient, 0, 250)
        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor position on id {self.steerId}. Error {status}")

        status = phoenix5.ErrorCode.OK # self.driveMotor.setStatusFramePeriod(ctre.StatusFrameEnhanced.Status_1_General, self.kCanStatusFrameMs, 250)

        if status != phoenix5.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor Status Frame on id {self.driveId}. Error {status}")

        self.steerController = SteerController(self)
        

    def getAbsoluteAngle(self) -> float:
        """gets the last abs angle encoder value radians"""
        angle_deg = self.encoder.getAbsolutePosition()
        angle = math.radians(angle_deg)
        angle %= 2.0 * math.pi
        if angle < 0.0:
            angle += 2.0 * math.pi
        print(f"{self.cancoderId}: {angle_deg} - {angle}")
        return angle

    def setDriveVoltage(self, voltage : float):
        '''sets module drive voltage (speed)'''
        #print(f"Voltage: {voltage} ")
        self.driveMotor.setVoltage(voltage)

    def setDrivePercent(self, percent : float):
        '''sets module drive percent (-1.0-1.0)'''
        #print(f"set {self.name}: {percent}")
        self.driveMotor.set(percent)

    def getDriveVelocity(self):
        '''gets module drive voltage (speed)'''
        return self.driveEncoder.getVelocity() * self.driveSensorVelocityCoefficient
    def getSteerAngle(self):
        '''gets current angle in radians of module setpoint'''
        return math.radians(self.encoder.getAbsolutePosition())
    def getCurrentAngle(self):
        return self.encoder.getAbsolutePosition()

    def setSteerAngle(self, angle: float):
        self.steerController.setReferenceAngle(math.radians(angle))

    def setSwerveModuleState(self, state: wpimath.kinematics.SwerveModuleState, maxSpeedMps: float):
        speed = state.speed / maxSpeedMps * self.kNominalVoltage
        steer = state.angle.degrees()
        #print(f"Speed {speed} Steer {steer} {state.angle.degrees}")
        self.set(speed, steer)

    def set(self, driveVoltage: float, steerAngleDeg: float):
        '''
        Sets the modules drive voltage and steer angle.
        Trys to prevent 180 degree turns on module if can rotate closer one direction
        '''
        #convert to radians
        steerAngle = math.radians(steerAngleDeg)
        #if steerAngle < 0.0:
        #    steerAngle += 2.0 * math.pi

        # currVel, currAngle = self.getPosition()

        steerDiff = steerAngle - self.getSteerAngle()
        #print(f"steer deg {steerAngleDeg}, steerAngle {steerAngle} diff {steerDiff}")
        # Change the target angle so the difference is in the range [-pi, pi) instead of [0, 2pi)
        if steerDiff >= math.pi:
            steerAngle -= 2.0 * math.pi
        elif steerDiff < -math.pi:
            steerAngle += 2.0 * math.pi
        steerDiff1 = steerDiff - self.getSteerAngle()

        #print(f"steer deg {steerAngleDeg}, steerAngle {steerAngle} diff {steerDiff}, {steerDiff1}")
        steerDiff = steerDiff1
        #If the difference is greater than 90 deg or less than -90 deg the drive can be inverted so the total
        #movement of the module is less than 90 deg
        if (steerDiff < math.pi / 2.0) or (steerDiff < (-math.pi / 2.0)):
            steerAngle += math.pi
            driveVoltage *= -1.0

        # put steer angle in range of [0, 2pi)
        steerAngle %= 2.0 * math.pi
        if steerAngle < 0.0:
            steerAngle += 2.0 * math.pi

        self.driveVoltage = driveVoltage
        self.setDriveVoltage(self.driveVoltage)
        self.steerController.setReferenceAngle(math.radians(steerAngleDeg))

        if self.table:
            self.table.putNumber("set steer deg", math.degrees(steerAngle))
            self.table.putNumber("drive %", driveVoltage / self.kNominalVoltage)

    #def periodic(self) -> None:
    #    """
    #    Runs in subsystem periodic
    #    """
    #    #TODO replace with PID velocity controller
    #    self.setDriveVoltage(self.driveVoltage)
    #    self.steerController.run()


    def getSteerMotor(self) -> phoenix5.WPI_TalonFX:
        '''gets the motor for steering'''
        return self.steerMotor
    def getSteerSensorPositionCoefficient(self):
        '''gets sensor to postion conversion'''
        return self.steerSensorPositionCoefficient
    def getSteerSensorVelocityCoefficient(self):
        '''gets the steer veleocy to sensor coeffiecent'''
        return self.steerSensorVelocityCoefficient
    def getSteerController(self) -> SteerController:
        '''returns the steer controller'''
        return self.steerController
    def getTranslation(self) -> wpimath.geometry.Translation2d:
        return self.translation

    def getPosition(self):
        vel = self.getDriveVelocity()

        # calculate total distance traveled
        self.distTraveled += vel * .02
        ang = self.getSteerAngle()
        if self.table:
            self.table.putNumber("curr steer deg", math.degrees(ang))
            self.table.putNumber("curr vel", vel)
        return wpimath.kinematics.SwerveModulePosition(self.distTraveled, wpimath.geometry.Rotation2d(math.degrees(ang)))

    def disable(self, drive = True, steer = True):
        if drive:
            self.driveMotor.disable()
        if steer:
            self.steerMotor.disable()

    def setCal(self, enable):
        if enable:
            # self.driveMotor.setNeutralMode(ctre.NeutralMode.Coast)
            encoderConfig = sensors.CANCoderConfiguration()
            encoderConfig.absoluteSensorRange = sensors.AbsoluteSensorRange.Unsigned_0_to_360
            encoderConfig.magnetOffsetDegrees = 0
            encoderConfig.sensorDirection = True
            status = self.encoder.configAllSettings(encoderConfig, 250)
            if status != 0:
                log.error(f"{self.name} failed to set val {status}")
                
        else:
            # self.driveMotor.setNeutralMode(ctre.NeutralMode.Brake)
            pass
