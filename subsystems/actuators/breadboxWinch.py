import commands2
import logging
import utils
import wpilib
import wpilib.interfaces
hwFactory = utils.hardwareFactory.getHardwareFactory()
import utils.sensorFactory
import utils.motorHelper

log = logging.getLogger("winch")

class Winch(commands2.CommandBase):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    wayPoint = 0
    def __init__(self, *kargs, **kwargs) -> None:
        super().__init__()
        motorSettings = {
            "type":"SparkMax",
            "inverted": False,
            "motorType": "kBrushless",
            "sensorPhase": True,
            "channel": 60
        }
        self.motor = utils.motorHelper.createMotor(motorSettings)
        encoderSettings = {
            "type": "wpilib.DutyCycleEncoder",
            "channel": 1,
            "offset": 0.0,
            "unitsPerRotation": 6.28318530718,
            "minDutyCycle": 0.0,
            "maxDutyCycle": 1.0}

        self.encoder = utils.sensorFactory.create("wpilib.DutyCycleEncoder", encoderSettings)
        self.encoder.reset()


    def setDistance(self, distance : float):
        self.wayPoint = distance
        if self.encoder.getPositionOffset() > self.wayPoint:
            self.forward = False
        else:
            self.forward = True

    def setSpeed(self, speed : float):
        self.motor.setVoltage(speed * 12)

    def getPosition(self):
        return self.encoder.getPositionOffset()

    def execute(self) -> None:
        self.distance = self.encoder.getPositionOffset()
        if self.forward and self.distance < self.wayPoint:
            self.motor.setVoltage(8)
        elif not self.forward and self.distance > self.wayPoint:
            self.motor.setVoltage(-8)

    def end(self, interrupted: bool) -> None:
        self.motor.setVoltage(0)
        self.encoder.reset()

    def isFinished(self) -> bool:
        if self.forward and self.distance >= self.wayPoint:
            return True
        elif not self.forward and self.distance <= self.wayPoint:
            return True
        return False
