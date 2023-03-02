from subsystems.actuators.breadboxArmRotation import ArmRotation
import commands2
import commands2.cmd
import math
import typing

class AutoArm(commands2.CommandBase):
    ArmCommand: typing.Optional[commands2.PIDSubsystem] = None
    def __init__(self, arm : ArmRotation, degrees : float) -> None:
        super().__init__()
        self.autonomousCommand = None
        self.arm = arm
        self.degrees = degrees
        self.moveArmDegrees(self.degrees)
        self.ArmCommand = self.arm
        self.ArmCommand.run(lambda : self.moveArmDegrees(degrees))

    def moveArm(self, radians: float) -> None:
        self.arm.setSetpoint(radians)

    def moveArmDegrees(self, degrees: float) -> None:
        self.arm.enable()
        self.moveArm(math.radians(degrees))

    def end(self, interrupted: bool) -> None:
        self.arm.disable()
    
    def isFinished(self) -> bool:
        return self.arm.atSetpoint()