import rev

def configureSparkMaxCanRates(motor : rev.CANSparkMax, faultRateMs = 50, motorTelmRateMs = 50, motorPosRateMs = 50, analogRateMs=1833, altEncoderRateMs = 1050, dutyCycleEncRateMs = 2150, dutyCycleEncVelRateMs = 3150):
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus0, faultRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus1, motorTelmRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus2, motorPosRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus3, analogRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus4, altEncoderRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus5, dutyCycleEncRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus6, dutyCycleEncVelRateMs)
    motor.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus7, 500) #Unknown frame type? default 250ms prob not important?
    
