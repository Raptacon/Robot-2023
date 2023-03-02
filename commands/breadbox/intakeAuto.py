from subsystems.arm.grader import Grabber
import time
import commands2

class AutoIntake(commands2.CommandBase):
    def __init__(self, grabber : Grabber, intaking : bool, maxTime : float) -> None:
        super().__init__()
        self.grabber = grabber
        self.intaking = intaking
        self.startTime = time.time()
        self.maxTime = maxTime

    def execute(self) -> None:
        self.time = time.time() - self.startTime
        if self.intaking:
            self.grabber.useIntakehCones(True)
        else:
            self.grabber.useOutputCones(True)
    
    def isFinished(self) -> bool:
        return self.time > self.maxTime
    
    def end(self, interrupted: bool) -> None:
        return self.grabber.stop()