import wpilib
import wpilib.interfaces
import wpilib.drive
import ctre
import commands2
import logging
import utils
hwFactory = utils.hardwareFactory.getHardwareFactory()


log = logging.getLogger("westcoast")


class Westcoast(commands2.SubsystemBase):
    def __init__(self, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            iff kargs is used
            0 = leftM
            1 = rightM
            2 = leftEncoder = None
            3 = rightEncoder = None
            4 = gyro = None
        '''
        super().__init__()

        #leftM: wpilib.interfaces._interfaces.MotorController,
        #rightM: wpilib.interfaces._interfaces.MotorController,
        #leftEncoder: ctre.WPI_TalonFX = None,
        #rightEncoder: ctre.WPI_TalonFX = None,
        #gyro: wpilib.interfaces.Gyro = None
        print(kargs)
        print(kwargs)

        #TODO remove support after refactoring to config or make better
        if len(kargs) > 0:
            self.leftM = kargs[0] if len(kargs) > 0 else None
            self.rightM = kargs[1] if len(kargs) > 1 else None
            self.leftEncoder = kargs[2] if len(kargs) > 2 else None
            self.rightEncoder = kargs[3] if len(kargs) > 3 else None
            self.gyro = kargs[4] if len(kargs) > 4 else None

            if not (self.leftM and self.rightM):
                raise Exception("Left and Right Motors must be provided")
        else:
            self.leftM = hwFactory.getHardwareComponet("drivetrain", "leftMotor")
            self.rightM = hwFactory.getHardwareComponet("drivetrain", "rightMotor")

            self.leftEncoder = self.leftM if isinstance(self.leftM, ctre.WPI_TalonFX) else None
            self.rightEncoder = self.rightM if isinstance(self.rightM, ctre.WPI_TalonFX) else None
            self.gyro = None #TODO fix me to use hardware factory

        self.driveTrain = wpilib.drive.DifferentialDrive(self.leftM, self.rightM)

        self.addChild("Drive", self.driveTrain)
        self.addChild("Left Encoder", self.leftEncoder)
        self.addChild("Right Encoder", self.rightEncoder)
        self.addChild("Gyro", self.gyro)

    def log(self):
        '''
        Log telemetry to smartdashboard
        '''
        if self.leftEncoder:
            sensor = self.leftEncoder.getSensorCollection()
            wpilib.SmartDashboard.putNumber("Left Distance", sensor.getIntegratedSensorAbsolutePosition())
            wpilib.SmartDashboard.putNumber("Left Speed", sensor.getIntegratedSensorVelocity())

        if self.rightEncoder:
            sensor = self.rightEncoder.getSensorCollection()
            wpilib.SmartDashboard.putNumber("Right Distance", sensor.getIntegratedSensorAbsolutePosition())
            wpilib.SmartDashboard.putNumber("Right Speed", sensor.getIntegratedSensorVelocity())
        if self.gyro:
            wpilib.SmartDashboard.putNumber("Gryo", self.gyro.getAngle())


    def drive(self, left: float, right: float) -> None:
        '''
        Sets the left and right speed of robot
        '''
        self.driveTrain.tankDrive(left, right)

    def arcadeDrive(self, speed : float, rotation : float) -> None:
        self.driveTrain.arcadeDrive(speed, rotation)

    def getHeading(self) -> float:
        '''
        Returns the heading if known. If not returns NaN
        '''
        if self.gyro:
            return self.gyro.getAngle()
        return float('NaN')

    def getGyro(self):
        return self.gyro

    def getDistance(self) -> float:
        '''
        returns the average distance driven since last reset
        '''

        left = self.leftEncoder.getSensorCollection().getIntegratedSensorPosition() if self.leftEncoder else 0
        right = self.rightEncoder.getSensorCollection().getIntegratedSensorPosition() if self.rightEncoder else 0

        return (left + right) / 2.0

    def getRightEncoder(self) -> float:
        return self.rightEncoder.getSensorCollection().getIntegratedSensorPosition() if self.rightEncoder else 0

    def reset(self) -> None:
        if self.gyro:
            self.gyro.reset()

        if self.leftEncoder:
            self.leftEncoder.getSensorCollection().setIntegratedSensorPosition(0.0, 10)

        if self.rightEncoder:
            self.rightEncoder.getSensorCollection().setIntegratedSensorPosition(0.0, 10)

    def periodic(self) -> None:
        self.log()
