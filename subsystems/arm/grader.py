import commands2
import logging
import utils
import rev
hwFactory = utils.hardwareFactory.getHardwareFactory()

log = logging.getLogger("grader")

class Grader(commands2.SubsystemBase):
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
            self.graderM = hwFactory.getHardwareComponet("arm" , "grader")