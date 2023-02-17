import wpilib
import wpilib.interfaces
import wpimath.controller
import ctre
import commands2
import logging
import utils
hwFactory = utils.hardwareFactory.getHardwareFactory()
import utils.sensorFactory
import utils.motorHelper

log = logging.getLogger("Arm")


class Arm(commands2.SubsystemBase):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    def __init__(self, subsystem, armFeedFordward, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            kwargs requires
            armMotor
            endoder
        '''
        super().__init__()
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
            "unitsPerRotation": 360.0,
            "minDutyCycle": 0.0,
            "maxDutyCycle": 1.0,       }
        self.encoder = utils.sensorFactory.create("wpilib.DutyCycleEncoder", encoderSettings)

        aff = wpimath.controller.ArmFeedforward(**armFeedFordward)
        
    def setPostion(self, degrees: float):
        self.motor.set(0.1)
    
    def getPostion(self) -> float:
        return self.encoder