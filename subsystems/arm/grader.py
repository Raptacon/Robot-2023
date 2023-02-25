import commands2
import logging
import utils
hwFactory = utils.hardwareFactory.getHardwareFactory()

log = logging.getLogger("grabber")

class Grabber(commands2.SubsystemBase):
    ConesInverted = False
    CubeInverted = False
    def __init__(self, *kargs,
                 **kwargs):
        super().__init__()
        print(kargs)
        print(kwargs)

        if len(kargs) > 0:
            self.graberMotor = kargs[0] if len(kargs) > 0 else None
            if not (self.graberMotor):
                raise Exception("Grabber motor must be provided")

        else:
            self.graberMotor = hwFactory.getHardwareComponent("grabber" , "grader")

    def useOutputCones(self, output: float):
        self.speed = output
        if self.ConesInverted:
            self.speed *= -1
        self.graberMotor.setVoltage(self.speed * 12)

    def switchCones(self, state : bool):
        self.ConesInverted = state

    def useOutputCubes(self, output: float):
        self.speed = output * -1
        if self.CubeInverted:
            self.speed = output
        else:
            self.speed = self.speed / 2
        self.graberMotor.setVoltage(self.speed * 12)

    def switchCubes(self, state : bool):
        self.CubeInverted = state
