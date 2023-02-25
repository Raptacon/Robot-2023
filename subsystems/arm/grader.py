import commands2
import logging
import utils
import rev
hwFactory = utils.hardwareFactory.getHardwareFactory()

log = logging.getLogger("grader")

class Grader(commands2.SubsystemBase):
    ConesInverted = False
    CubeInverted = False
    def __init__(self, *kargs,
                 **kwargs):
        super().__init__()
        print(kargs)
        print(kwargs)

        if len(kargs) > 0:
            self.graderM = kargs[0] if len(kargs) > 0 else None
            if not (self.graderM):
                raise Exception("grader motor must be provided")

        else:
            self.graderM = hwFactory.getHardwareComponent("grabber" , "grader")

    def useOutputCones(self, output: float):
        self.speed = output
        if self.ConesInverted:
            self.speed *= -1
        self.graderM.setVoltage(self.speed)

    def switchCones(self, state : bool):
        self.ConesInverted = state

    def useOutputCubes(self, output: float):
        self.speed = output * -1
        if self.CubeInverted:
            self.speed = output
        self.graderM.setVoltage(self.speed)

    def switchCubes(self, state : bool):
        self.CubeInverted = state
