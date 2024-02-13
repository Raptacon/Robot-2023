import commands2
import rev
import wpilib

class ShooterPivot(commands2.SubsystemBase):
    def __init__(self) -> None:
        self.pivotMotor = rev.CANSparkMax(31, rev.CANSparkLowLevel.MotorType.kBrushless)

    def runPivot(self, speed):
        self.pivotMotor.set(speed)