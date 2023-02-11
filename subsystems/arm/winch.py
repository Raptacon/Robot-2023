import commands2
import logging
import rev

log = logging.getLogger("winch")

class Winch(commands2.SubsystemBase):
    def __init__(self, hwFactory, *kargs,
                 **kwargs):
        super().__init__()
        print(kargs)
        print(kwargs)

        if len(kargs) > 0:
            self.winchM = kargs[0] if len(kargs) > 0 else None
            log.info("Obtained components in subsystem class from args")
            #self.winchEncoder = kargs[1] if len(kargs) > 1 else None
        else:
            self.winchM = hwFactory.getHardwareComponet("Arm", "winch")
            log.info("Obtained components in subsystem class from HWFactory")

            #self.winchEncoder = self.winchM.getEncoder() if isinstance(self.winchM, rev.CANSparkMax) else None
        
        if not (self.winchM):
            raise Exception("winch motor must be provided")

"""
    def log(self):
        '''
        Log telemetry to smartdashboard
        '''
        if self.winchEncoder:
            sensor = self.winchEncoder.getSensorCollection()
           wpilib.SmartDashboard.putNumber("Winch Distance", sensor.getIntegratedSensorAbsolutePosition())
           wpilib.SmartDashboard.putNumber("Winch Speed", sensor.getIntegratedSensorVelocity())
"""