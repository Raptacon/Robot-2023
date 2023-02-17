import wpilib
import wpilib.interfaces
import wpimath.controller
import wpimath.trajectory
import ctre
import commands2
import logging
import utils
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
        contstraints = wpimath.trajectory.TrapezoidProfile.Constraints(1.0, 1.0)
        profileController = wpimath.controller.ProfiledPIDController(0.1, 0, 0, contstraints, 0.02)
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

        aff = wpimath.controller.ArmFeedforward(**armFeedFordward)

        self.setGoal(self.encoder.getDistance())

    def useOutput(self, output: float, setpoint: wpimath.trajectory.TrapezoidProfile.State) -> None:
        feedforward = self.aff.calculate(setpoint.position, setpoint.velocity)
        log.info(f"output: {output}, feedforward: {feedforward}")
        self.motor.set(output + feedforward)

    def getPostion(self) -> float:
        return self.encoder.getAbsolutePosition()