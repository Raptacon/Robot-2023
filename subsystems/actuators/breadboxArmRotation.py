import wpilib
import wpilib.interfaces
import wpimath.controller
import wpimath.trajectory
import commands2
import logging
import utils
import math
hwFactory = utils.hardwareFactory.getHardwareFactory()
import utils.sensorFactory
import utils.motorHelper
import rev

log = logging.getLogger("Arm Rotation")


class ArmRotation(commands2.PIDSubsystem):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    kMinPostion = 0
    kMaxPostion = 1.0 * 2 * math.pi
    kRolloverDeadZoneDeg = 340 #degrees
    lastPosValDeg = 50 #non intersting value
    def __init__(self, subsystem, armFeedFordward, offset = 0, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            kwargs requires
            armMotor
            endoder
        '''

        pidController = wpimath.controller.PIDController(9.7, 0, 74,6)

        pidController.setTolerance(0.02)
        super().__init__(pidController, 0)
        #TODO Fix factor
#        self.config = kwargs
#        self.motor = hwFactory.getHardwareComponent("arm", "motor")
#        self.encoder = hwFactory.getHardwareComponent("arm", "encoder")
#        log.error("Robot Arm not done")
        motorSettings = {
            "type":"SparkMax",
            "inverted": False,
            "motorType": "kBrushless",
            "sensorPhase": True,
            "channel": 40
        }
        self.motor = utils.motorHelper.createMotor(motorSettings)
        encoderSettings = {
            "type": "wpilib.DutyCycleEncoder",
            "channel": 0,
            "offset": 0.0,
            "unitsPerRotation": 6.28318530718,
            "minDutyCycle": 0.0,
            "maxDutyCycle": 1.0}

        self.encoder = utils.sensorFactory.create("wpilib.DutyCycleEncoder", encoderSettings)
        self.encoder.setPositionOffset(0)
        self.encoder.reset()

        self.aff = wpimath.controller.ArmFeedforward(**armFeedFordward)

        self.addChild("Encoder", self.encoder)
        self.offset = offset

        if "kMinPostion" in kwargs:
            self.kMinPostion = kwargs["kMinPostion"]
        if "kMaxPostion" in kwargs:
            self.kMaxPostion = kwargs["kMaxPostion"]

        self.disabled = True
        self.setSetpoint(self.getPostion())

    def _useOutput(self, output: float, setpoint) -> None:
        feedforward = self.aff.calculate(setpoint, 0)

        if self.disabled:
            self.motor.setVoltage(0)
            return

        if self.getController().atSetpoint():
            self.motor.setVoltage(0)
            return
        #if not self.disabled:
        else:
            self.motor.setVoltage((output + feedforward))

    def disable(self) -> None:
        self.motor.setVoltage(0)
        self.disabled = True
        return super().disable()

    def enable(self) -> None:
        self.disabled = False
        return super().enable()

    def getPostion(self) -> float:
        absPos = math.fmod(2*math.pi - (self.encoder.getAbsolutePosition() + self.offset) * (2*math.pi), 2*math.pi)
        currPos = absPos
        currDeg = math.degrees(currPos)
        wpilib.SmartDashboard.putNumber("Arm offset", -self.encoder.getAbsolutePosition())
        wpilib.SmartDashboard.putNumber("Arm Angle Degrees", math.degrees(currPos))

        if self.motor.getFault(self.motor.FaultID.kHardLimitFwd):
            log.info("Forward Limit hit")
            self.forwardHit = True

        if self.motor.getFault(self.motor.FaultID.kHardLimitRev):
            log.info("Forward Limit hit")
            self.reverseHit = True


        #below 0 sensor set point, we treat 0-kRolloverDeadZoneDeg for control purposes
        if currDeg > self.kRolloverDeadZoneDeg:
            absPos = currPos - 2*math.pi

        return absPos

    def _getMeasurement(self) -> float:
        return self.getPostion()

    def setSetpoint(self, goal: float) -> None:
        if goal < self.kMinPostion:
            log.warning(f"Goal {goal} is less than min {self.kMinPostion}")
            return
        if goal > self.kMaxPostion:
            log.warning(f"Goal {goal} is greater than max {self.kMaxPostion}")
            return

        self.goal = goal
        super().setSetpoint(self.goal)

    def periodic(self) -> None:
        super().periodic()
        self.getPostion()

    def setSetpointDegrees(self, setpoint: float) -> None:
        return self.setSetpoint(math.radians(setpoint))

    def atSetpoint(self) -> bool:
        return self.getController().atSetpoint()

    def toggleBrake(self) -> None:
        if self.motor.getIdleMode() == rev.CANSparkMax.IdleMode.kBrake:
            log.warning("Setting to coast")
            self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        else:
            log.warning("Setting to brake")
            self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
