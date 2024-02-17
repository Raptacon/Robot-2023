import commands2
import rev
import math
import wpilib
import wpimath
import wpimath.controller
from rev import SparkMaxLimitSwitch
from wpilib import DigitalInput
class SwerveIntakePivot(commands2.PIDSubsystem):
    kMinPostion = 0
    kMaxPostion = 1.0 * 2 * math.pi
    kRolloverDeadZoneDeg = 340
    def __init__(self) -> None:
        self.pivotMotor = rev.CANSparkMax(22, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.pivotMotor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.pivotMotor.setInverted(False)

        self.pivotRelEncoder = self.pivotMotor.getEncoder(rev.SparkRelativeEncoder.Type.kHallSensor)

        self.encoder = wpilib.DutyCycleEncoder(0)
        self.encoderOffset = 0.551

        self.pidController = wpimath.controller.PIDController(10, 0, 0)
        self.pidController.setTolerance(0.1)
        super().__init__(self.pidController, 0)

        self.motorFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(0, 0, 0)

        self.handOffSwitch = DigitalInput(4)

        self.setSetpoint(self.getPostion())

    def useOutput(self, output: float, setpoint: float):
        feedforward = self.motorFeedforward.calculate(setpoint, 0)
        wpilib.SmartDashboard.putNumber("Pivot Current", self.pivotMotor.getOutputCurrent())
        wpilib.SmartDashboard.putNumber("Pivot Velocity", self.pivotRelEncoder.getVelocity())

        self.voltage = output + feedforward
        self.voltage = max(-10, min(self.voltage, 10))
        self.pivotMotor.setVoltage(self.voltage)

    def getPostion(self) -> float:
        absPos = (((self.getAbsolutePosition() - self.encoderOffset) % 1.0) * (2*math.pi))

        if self.getLimit():
            self.encoderOffset = self.getAbsolutePosition()

        currDeg = (math.degrees(absPos))
        wpilib.SmartDashboard.putNumber("Intake Angle Degrees", currDeg)

        return absPos
    
    def getAbsolutePosition(self):
        #print(f"absPos:{self.encoder.getAbsolutePosition()}")
        return self.encoder.getAbsolutePosition()

    def setSetpoint(self, goal: float) -> None:
        if goal < self.kMinPostion:
            print("min")
            return
        if goal > self.kMaxPostion:
            print("max")
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
        return self.getPostion()

    def setIntakePivot(self, percent : float):
        self.pivotMotor.set(percent)

    def atSetpoint(self) -> bool:
        return self.getController().atSetpoint()
    
    def getLimit(self):
        return self.handOffSwitch.get()
