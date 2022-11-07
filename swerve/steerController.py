import math
import ctre

class SteerController ():
    """Controller for sterring a swerve drive module. Cancoder and FX500 only"""
    kEncoderResetIterations = 500
    kEncoderResetMaxAngVel = math.radians(0.5)

    def __init__(self, swerveModule):
        self.module = swerveModule
        self.referenceAngleRadians = 0.0
        self.resetIteration = 0


    def getReferenceAngle(self):
        """Gets current set angle in radians"""
        return self.referenceAngleRadians

    def setReferenceAngle(self, referenceAngleRadians : float):
        '''https://github.com/SwerveDriveSpecialties/swerve-lib/blob/f6f4de65808d468ed01cc5ca39bf322383838fcd/src/main/java/com/swervedrivespecialties/swervelib/ctre/Falcon500SteerControllerFactoryBuilder.java#L181'''
        motor = self.module.getSteerMotor()
        motorEncoderVelocityCoefficient = self.module.getSteerSensorVelocityCoefficient()
        motorEncoderPositionCoefficient = self.module.getSteerSensorPositionCoefficient()
        currentAngleRadians = motor.getSelectedSensorPosition() * motorEncoderPositionCoefficient

        if motor.getSelectedSensorVelocity() * motorEncoderVelocityCoefficient < self.kEncoderResetMaxAngVel:
            self.resetIteration +=1
            if self.resetIteration >= self.kEncoderResetIterations:
                self.resetIteration = 0
                absoluteAngle = self.module.getAbsoluteAngle()
                motor.setSelectedSensorPosition(absoluteAngle / motorEncoderPositionCoefficient)
                currentAngleRadians = absoluteAngle
        else:
            self.resetIteration = 0

        currentAngleRadiansMod = currentAngleRadians % (2.0 * math.pi)
        if currentAngleRadiansMod < 0.0:
            currentAngleRadiansMod += 2.0 * math.pi

        adjustedReferenceAngleRadians = referenceAngleRadians + currentAngleRadians - currentAngleRadiansMod
        if (referenceAngleRadians - currentAngleRadiansMod) > math.pi:
            adjustedReferenceAngleRadians -= 2.0 * math.pi
        elif (referenceAngleRadians - currentAngleRadiansMod) < -math.pi:
            adjustedReferenceAngleRadians += 2.0 * math.pi

        motor.set(ctre.TalonFXControlMode.Position, adjustedReferenceAngleRadians / motorEncoderPositionCoefficient)
        self.referenceAngleRadians = referenceAngleRadians

    def getStateAngle(self) -> float:
        '''
        gets current postion in radians
        '''
        motorAngleRadians = self.module.getSteerMotor() * self.module.getSteerSensorPositionCoefficient()
        motorAngleRadians %= 2.0 * math.pi
        if motorAngleRadians < 0.0:
            motorAngleRadians += 2.0 * math.pi
        return motorAngleRadians
