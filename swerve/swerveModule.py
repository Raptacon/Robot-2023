
import math
import ctre
import wpimath.geometry
import wpimath.kinematics

from .steerController import SteerController

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
        self._driveInverted = True
        self._steerReduction = (15.0 / 32.0) * (10.0 / 60.0)
        self._steerInverted = True
        self._moduleType = "Mk4L1"


class SwerveModuleMk4L1FalcFalcCanCoder() :
    '''
    Module for Mk4L1 with 2 faclon 500 and a cancoder swerve drive
    '''
    driveId : int
    steerId: int
    cancoderId: int
    encoder : ctre.CANCoder

    kNominalVoltage = 12.0
    kDriveCurrentLimit = 80.0
    kSteerCurrentLimit = 20.0

    ''' https://github.com/SwerveDriveSpecialties/swerve-lib/blob/develop/src/main/java/com/swervedrivespecialties/swervelib/ctre/Falcon500DriveControllerFactoryBuilder.java '''
    kTicksPerRotation = 2048.0
    kCanTimeoutMs = 250
    kStatusFrameGeneralPeriodMs = 250
    kSteerPID = (0.2, 0.0, 0.1)
    kCanStatusFrameMs = 10

    def __init__(self, location : tuple[float, float, str], channelBase: int, encoderCal: float = 0):
        '''
        Creates a new swerve module at location in robot. With channesl channelBase = drive
        channelBase + 1 = steer
        channelBase + 2 = cancoder
        and the encoders rotated by encoderCal.
        location [x (trackbase + is left side), y (wheelbase + is front), name]
        '''
        self.consts = SwerveModuleMk4L1Consts()
        self.driveId = channelBase + 0
        self.steerId = channelBase + 1
        self.cancoderId = channelBase + 2
        self.name = location[2]
        self.translation = wpimath.geometry.Translation2d(location[0], location[1])

        #create can encoder
        self.encoder = ctre.WPI_CANCoder(self.cancoderId)
        encoderConfig = ctre.CANCoderConfiguration()
        encoderConfig.absoluteSensorRange = ctre.AbsoluteSensorRange.Unsigned_0_to_360
        encoderConfig.magnetOffsetDegrees = encoderCal
        encoderConfig.sensorDirection = True
        status = self.encoder.configAllSettings(encoderConfig, 250)
        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure CAN encoder on id {self.cancoderId}. Error {status}")
        status = self.encoder.setStatusFramePeriod(ctre.CANCoderStatusFrame.SensorData, self.kCanStatusFrameMs, 250)
        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure CAN encoder on status frame on id {self.cancoderId}. Error {status}")

        #create drive motor
        self.driveSensorPositionCoefficient = math.pi * self.consts.getWheelDiameter() * self.consts.getDriveReduction() / self.kTicksPerRotation
        self.driveSensorVelocityCoefficient = self.driveSensorPositionCoefficient * 10.0
        motorConfig = ctre.TalonFXConfiguration()
        motorConfig.voltageCompSaturation = self.kNominalVoltage
        supplyCurrConfig = ctre.SupplyCurrentLimitConfiguration()
        supplyCurrConfig.currentLimit = self.kDriveCurrentLimit
        supplyCurrConfig.enable = True
        motorConfig.supplyCurrLimit = supplyCurrConfig

        self.driveMotor = ctre.WPI_TalonFX(self.driveId)

        status = self.driveMotor.configAllSettings(motorConfig, 250)

        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Drive Motor on id {self.driveId}. Error {status}")
        self.driveMotor.enableVoltageCompensation(True)
        self.driveMotor.setNeutralMode(ctre.NeutralMode.Brake)
        self.driveMotor.setInverted(self.consts.getDriveInverted())
        self.driveMotor.setSensorPhase(True)

        status = self.driveMotor.setStatusFramePeriod(ctre.StatusFrameEnhanced.Status_1_General, self.kCanStatusFrameMs, 250)

        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Drive Motor Status Frame on id {self.driveId}. Error {status}")

        #create steer motor
        self.steerSensorPositionCoefficient = 2.0 * math.pi / self.kTicksPerRotation * self.consts.getSteerReduction()
        self.steerSensorVelocityCoefficient = self.steerSensorPositionCoefficient * 10.0
        self.steerMotor = ctre.WPI_TalonFX(self.steerId)

        motorConfig = ctre.TalonFXConfiguration()
        motorConfig.slot0.kP = self.kSteerPID[0]
        motorConfig.slot0.kI = self.kSteerPID[1]
        motorConfig.slot0.kD = self.kSteerPID[2]
        motorConfig.voltageCompSaturation = self.kNominalVoltage
        supplyCurrConfig.currentLimit = self.kSteerCurrentLimit
        motorConfig.supplyCurrLimit = supplyCurrConfig

        status = self.steerMotor.configAllSettings(motorConfig, 250)

        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor on id {self.steerId}. Error {status}")

        self.steerMotor.enableVoltageCompensation(True)

        status = self.steerMotor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor, 0, 250)
        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor Feedback on id {self.steerId}. Error {status}")
        self.steerMotor.setSensorPhase(True)
        self.steerMotor.setInverted(self.consts.getSteerInverted())
        self.steerMotor.setNeutralMode(ctre.NeutralMode.Brake)
        status = self.steerMotor.setSelectedSensorPosition(self.getAbsoluteAngle() / self.steerSensorPositionCoefficient, 0, 250)
        if status != ctre.ErrorCode.OK:
            raise RuntimeError(f"Failed to configure Steer Motor position on id {self.steerId}. Error {status}")

        status = self.driveMotor.setStatusFramePeriod(ctre.StatusFrameEnhanced.Status_1_General, self.kCanStatusFrameMs, 250)

        if status != ctre.ErrorCode.OK:
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
        self.driveMotor.set(ctre.TalonFXControlMode.PercentOutput, voltage / self.kNominalVoltage)
    def setDrivePercent(self, percent : float):
        '''sets module drive percent (0-1.0)'''
        self.driveMotor.set(ctre.TalonFXControlMode.PercentOutput, percent)

    def getDriveVelocity(self):
        '''gets module drive voltage (speed)'''
        return self.driveMotor.getSelectedSensorVelocity() * self.driveSensorVelocityCoefficient
    def getSteerAngle(self):
        '''gets current angle in deg of module setpoint'''
        return self.steerController.getStateAngle()
    def getCurrentAngle(self):
        return self.encoder.getAbsolutePosition()

    def setSteerAngle(self, angle: float):
        self.steerController.setReferenceAngle(math.radians(angle))

    def setSwerveModuleState(self, state: wpimath.kinematics.SwerveModuleState, maxSpeedMps: float):
        speed = state.speed / maxSpeedMps * self.kNominalVoltage
        steer = state.angle.radians()
        print(f"Steer {steer} {state.angle.degrees}")
        self.set(speed, steer)

    def set(self, driveVoltage: float, steerAngleDeg: float):
        '''
        Sets the modules drive voltage and steer angle.
        Trys to prevent 180 degree turns on module if can rotate closer one direction
        '''
        #convert to radians
        steerAngle = math.radians(steerAngleDeg % 360)
        if steerAngle < 0.0:
            steerAngle += 2.0 * math.pi

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

        #self.setDriveVoltage(driveVoltage)
        self.steerController.setReferenceAngle(steerAngle)

    def getSteerMotor(self) -> ctre.WPI_TalonFX:
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

    def getPosition(self) -> [float, float]:
        return [self.getDriveVelocity(), self.getSteerAngle()]

    def disable(self, drive = True, steer = True):
        if drive:
            self.driveMotor.disable()
        if steer:
            self.steerMotor.disable()
