from subsystems.arm.grader import Grabber
import commands2
import time

class AutoGrabber(commands2.CommandBase):
    def __init__(self, Grabber : Grabber, maxTime : float, Intaking : bool) -> None:
        super().__init__()
        self.grabber = Grabber
        self.maxTime = maxTime
        self.intaking = Intaking
        self.startingTime = time.time()

    def execute(self) -> None:
        self.currentTime = time.time() - self.startingTime
        if self.intaking:
            self.grabber.useIntakehCones(True)
        else:
            self.grabber.useOutputCones(1)
    
    def isFinished(self) -> bool:
        return self.currentTime >= self.maxTime
    
    def end(self, interrupted: bool) -> None:
        self.grabber.stop()
