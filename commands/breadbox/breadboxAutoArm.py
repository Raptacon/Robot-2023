from subsystems.actuators.breadboxArmRotation import ArmRotation
import commands2
import commands2.cmd
import math

class AutoArm(commands2.CommandBase):
    def __init__(self, arm : ArmRotation, degrees : float) -> None:
        super().__init__()
        self.arm = arm
        self.degrees = degrees
        self.arm.enable()

    def execute(self) -> None:
        commands2.cmd.runOnce(lambda: self.moveArmDegrees(self.degrees), [self.arm])

    def moveArm(self, radians: float) -> None:
        self.arm.setSetpoint(radians)

    def moveArmDegrees(self, degrees: float) -> None:
        self.moveArm(math.radians(degrees))

    def end(self, interrupted: bool) -> None:
        self.arm.disable()
    
    def isFinished(self) -> bool:
        return self.arm.atSetpoint()