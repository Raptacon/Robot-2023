import wpilib
import wpilib.interfaces
import wpimath.controller
import wpimath.trajectory
import ctre
import commands2
import logging
import utils
import math
hwFactory = utils.hardwareFactory.getHardwareFactory()
import utils.sensorFactory
import utils.motorHelper

log = logging.getLogger("Arm")


class Arm(commands2.ProfiledPIDSubsystem):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    def __init__(self, subsystem, armFeedFordward, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            kwargs requires
            armMotor
            endoder
        '''
        contstraints = wpimath.trajectory.TrapezoidProfile.Constraints(20, 50)
        profileController = wpimath.controller.ProfiledPIDController(12.763, 0, 0, contstraints, 0.02)
        profileController.setTolerance(0.2)
        super().__init__(profileController, 0)
        #TODO Fix factor
#        self.config = kwargs
#        self.motor = hwFactory.getHardwareComponet("arm", "motor")
#        self.encoder = hwFactory.getHardwareComponet("arm", "encoder")
#        log.error("Robot Arm not done")
        motorSettings = {
            "type":"SparkMax",
            "inverted": True,
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
            "maxDutyCycle": 1.0,       }
        self.encoder = utils.sensorFactory.create("wpilib.DutyCycleEncoder", encoderSettings)


        self.aff = wpimath.controller.ArmFeedforward(**armFeedFordward)

        self.addChild("Encoder", self.encoder)
        #self.addChild("Motor", self.motor) //spark max is not sendable
        #self.addChild("AFF", self.aff)

        self.setGoal(self.getPostion())

    def _useOutput(self, output: float, setpoint: wpimath.trajectory.TrapezoidProfile.State) -> None:
        feedforward = self.aff.calculate(setpoint.position, setpoint.velocity)
        #print(f"output: {output}, feedforward: {feedforward} curr {self.getPostion()} set {self.goal}")
        if not self.disabled:
            self.motor.setVoltage(output + feedforward)
        else:
            print("Disabled")
            self.motor.setVoltage(0)
            self.motor.disable()

    def disable(self) -> None:
        self.disabled = True
        return super().disable()
    def enable(self) -> None:
        self.disabled = False
        return super().enable()

    def getPostion(self) -> float:
        return math.fmod(self.encoder.getDistance(), 2*math.pi)

    def _getMeasurement(self) -> float:
        return self.getPostion()

    def setGoal(self, goal: float) -> None: 
        print(f"set goal {goal}, {self.getPostion()}")
        self.goal = goal
        super().setGoal(goal)

    def moveArm(self, radians: float) -> None:
        self.setGoal(radians)
        self.enable()

    def moveArmDegrees(self, degrees: float) -> None:
        self.moveArm(math.radians(degrees))