import commands2
import rev
import math
import wpilib
import wpimath
import wpimath.controller
class SwerveShooterPivot(commands2.SubsystemBase):
    def __init__(self) -> None:
        self.pivotMotor = rev.CANSparkMax(31, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.pivotMotor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.pivotMotor.setInverted(False)

        self.encoder = wpilib.DutyCycleEncoder(1)
        self.encoderOffset = 0.422749383068735

    def runPivot(self, speed : float):
        self.pivotMotor.set(speed)

        wpilib.SmartDashboard.putNumber("Shooter pos", self.encoder.getAbsolutePosition())
