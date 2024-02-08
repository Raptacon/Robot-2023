import commands2
import rev
import math
import wpilib
import wpimath.controller

class SwerveIntakePivot(commands2.PIDSubsystem):
    kMinPostion = 0
    kMaxPostion = 1.0 * 2 * math.pi
    kRolloverDeadZoneDeg = 340
    def __init__(self) -> None:
        self.pivotMotor = rev.CANSparkMax(22, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.encoder = self.pivotMotor.getAbsoluteEncoder(rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle)

        self.pidController = wpimath.controller.PIDController(0.5, 0, 0)
        self.pidController.setTolerance(0.02)
        super().__init__(self.pidController, 0)

        self.encoder.setZeroOffset(0)

        self.motorFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(12, 0, 0)

        self.setSetpoint(self.getPostion())

    def useOutput(self, output: float, setpoint: float):
        feedforward = self.motorFeedforward.calculate(setpoint, 0)
        self.pivotMotor.setVoltage(output + feedforward)

    def getPostion(self) -> float:
        absPos = math.fmod(2*math.pi - self.encoder.getPosition() * (2*math.pi), 2*math.pi)
        currPos = absPos
        currDeg = math.degrees(currPos)
        wpilib.SmartDashboard.putNumber("Intake offset", -self.encoder.getPosition())
        wpilib.SmartDashboard.putNumber("Intake Angle Degrees", math.degrees(currPos))

        if self.pivotMotor.getFault(self.pivotMotor.FaultID.kHardLimitFwd):
            #log.info("Forward Limit hit")
            self.forwardHit = True

        if self.pivotMotor.getFault(self.pivotMotor.FaultID.kHardLimitRev):
            #log.info("Forward Limit hit")
            self.reverseHit = True


        #below 0 sensor set point, we treat 0-kRolloverDeadZoneDeg for control purposes
        if currDeg > self.kRolloverDeadZoneDeg:
            absPos = currPos - 2*math.pi

        return absPos

    def setSetpoint(self, goal: float) -> None:
        if goal < self.kMinPostion:
            return
        if goal > self.kMaxPostion:
            return

        self.goal = goal
        super().setSetpoint(self.goal)

    def setSetpointDegrees(self, setpoint: float) -> None:
        return self.setSetpoint(math.radians(setpoint))

    def atSetpoint(self) -> bool:
        return self.getController().atSetpoint()

    def closeToSetpoint(self, tolerance) -> bool:
        return self.getController().getPositionError() < tolerance

    def getMeasurement(self) -> float:
        return self.encoder.getPosition()

    def setIntakePivot(self, percent : float):
        self.pivotMotor.set(percent)

    def atSetpoint(self) -> bool:
        return self.getController().atSetpoint()
    