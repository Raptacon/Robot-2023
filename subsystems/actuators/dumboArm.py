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

log = logging.getLogger("Arm")


class Arm(commands2.PIDSubsystem):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    def __init__(self, subsystem, armFeedFordward, offset = 0, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            kwargs requires
            armMotor
            endoder
        '''

        pidController = wpimath.controller.PIDController(9.7, 0, 74,6)

        pidController.setTolerance(0.1)
        super().__init__(pidController, 0)
        #TODO Fix factor
#        self.config = kwargs
#        self.motor = hwFactory.getHardwareComponet("arm", "motor")
#        self.encoder = hwFactory.getHardwareComponet("arm", "encoder")
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
        self.addChild("Encoder", self.encoder)
        
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
        return math.fmod(2*math.pi - (self.encoder.getAbsolutePosition() + self.offset) * (2*math.pi), 2*math.pi)
        
    def _getMeasurement(self) -> float:
        #print(f"dist {self.encoder.getDistance() : 01.03}, {self.encoder.getAbsolutePosition(): 01.03} , {self.offset: 01.03}, {self.getPostion(): 01.03}, {math.degrees(self.getPostion()): 01.03}, {self.getSetpoint()}")
        #print(f"ang {math.degrees(self.getPostion())}, {self.encoder.getAbsolutePosition()}")
        return self.getPostion()

    def setSetpoint(self, goal: float) -> None:
        self.goal = goal
        super().setSetpoint(self.goal)
