import commands2
import rev

class SwerveIntake(commands2.SubsystemBase):
    def __init__(self) -> None:
        self.intakeMotor = rev.CANSparkMax(21, rev.CANSparkLowLevel.MotorType.kBrushless)

    def runIntake(self, percent : float):
        self.intakeMotor.set(percent)