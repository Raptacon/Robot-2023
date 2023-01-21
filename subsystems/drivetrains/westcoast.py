import wpilib
import wpilib.interfaces
import wpilib.drive
import ctre
import commands2


class Westcoast(commands2.SubsystemBase):
    def __init__(self,
                 leftM: wpilib.interfaces._interfaces.MotorController,
                 rightM: wpilib.interfaces._interfaces.MotorController,
                 leftEncoder: ctre.WPI_TalonFX = None,
                 rightEncoder: ctre.WPI_TalonFX = None,
                 gyro: wpilib.interfaces.Gyro = None):
        ''' TODO update to be more generic, hard coding talons'''
        super().__init__()

        if leftM is None or rightM is None:
            raise Exception("Left and Right Motors must be provided")
        self.leftM = leftM
        self.rightM = rightM
        self.leftEncoder = leftEncoder
        self.rightEncoder = rightEncoder
        self.gyro = gyro

        self.driveTrain = wpilib.drive.DifferentialDrive(leftM, rightM)

        self.addChild("Drive", self.driveTrain)
        self.addChild("Left Encoder", self.leftEncoder)
        self.addChild("Right Encoder", self.rightEncoder)
        self.addChild("Gyto", self.gyro)

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

    def getHeading(self) -> float:
        '''
        Returns the heading if known. If not returns NaN
        '''
        if self.gyro:
            return self.gyro.getAngle()
        return float('NaN')

    def getDistance(self) -> float:
        '''
        returns the average distance driven since last reset
        '''

        left = self.leftEncoder.getSensorCollection().getIntegratedSensorPosition() if self.leftEncoder else 0
        right = self.rightEncoder.getSensorCollection().getIntegratedSensorPosition if self.rightEncoder else 0

        return (left + right) / 2.0

    def reset(self) -> None:
        if self.gyro:
            self.gyro.reset()

        if self.leftEncoder:
            self.leftEncoder.getSensorCollection().setIntegratedSensorPosition(0.0, 10)

        if self.rightEncoder:
            self.rightEncoder.getSensorCollection().setIntegratedSensorPosition(0.0, 10)

    def periodic(self) -> None:
        self.log()
