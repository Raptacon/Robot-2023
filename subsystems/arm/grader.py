import commands2
import logging
import utils
import wpilib
import wpilib.interfaces
from subsystems.actuators.dumboArm import Arm
hwFactory = utils.hardwareFactory.getHardwareFactory()

log = logging.getLogger("grabber")

class Grabber(commands2.SubsystemBase):
    ConesInverted = False
    CubeInverted = False
    grabberMotor: wpilib.interfaces._interfaces.MotorController
    def __init__(self, *kargs,
                 **kwargs):
        super().__init__()
        print(kargs)
        print(kwargs)

        if len(kargs) > 0:
            self.grabberMotor = kargs[0] if len(kargs) > 0 else None
            if not (self.grabberMotor):
                raise Exception("Grabber motor must be provided")

        else:
            self.grabberMotor = hwFactory.getHardwareComponent("grabber" , "grader")

    def useIntake(self, output : float, arm : Arm):
        if arm.getPostion() <= 32:
            self.useIntakeCubes(output) #At the set position 30 the intake should be set up for cube intake
        elif arm.getPostion() > 32 and arm.getPostion() <= 62:
            self.useOutputCubes(output) #At the set position 60 the intake should be set up for cube outake
        elif arm.getPostion() >= 98 and arm.getPostion() <= 132:
            self.useOutputCones(output) #At the set position 130 or 100 the intake should be set up for the cone outake
        elif arm.getPostion() >= 198:
            self.useIntakeCones(output) #At the set position 200 the intake should be set up for the cone intake
        else:
            self.stop()

    def useOutputCones(self, output: float):
        self.speed = output
        self.grabberMotor.setVoltage(self.speed * 12)

    def useIntakeCones(self, output : float):
        self.speed = -1 * output
        self.grabberMotor.setVoltage(self.speed * 12)

    def useOutputCubes(self, output: float):
        self.speed = output * -1
        self.grabberMotor.setVoltage(self.speed * 12)

    def useIntakeCubes(self, output : float):
        self.speed = output
        self.grabberMotor.setVoltage(self.speed * 8)

    def stop(self):
        self.grabberMotor.setVoltage(0)
