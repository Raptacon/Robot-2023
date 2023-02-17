import wpilib
import wpilib.interfaces
import wpilib.drive
import ctre
import commands2
import logging
import utils
hwFactory = utils.hardwareFactory.getHardwareFactory()


log = logging.getLogger("Arm")


class Arm(commands2.SubsystemBase):
    motor: wpilib.interfaces._interfaces.MotorController
    encoder: wpilib.DutyCycleEncoder
    def __init__(self, *kargs,
                 **kwargs):
        ''' TODO update to be more generic, hard coding talons
            kwargs requires
            armMotor
            endoder
        '''
        super().__init__()

        self.config = kwargs
        self.motor = hwFactory.getHardwareComponet(kwargs["subsystem"], "armMotor")
        self.encoder = hwFactory.getHardwareComponet(kwargs["subsystem"], "encoder")
        log.error("Robot Arm not done")

    def setPostion(self, degrees: float):
        self.motor.set(0.1)
    
    def getPostion(self) -> float:
        return self.encoder