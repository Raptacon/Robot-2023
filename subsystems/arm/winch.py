import commands2
import logging
import utils
import rev
hwFactory = utils.hardwareFactory.getHardwareFactory()

log = logging.getLogger("winch")

class Winch(commands2.SubsystemBase):
    def __init__(self, *kargs,
                 **kwargs):
        super().__init__()
        print(kargs)
        print(kwargs)

        if len(kargs) > 0:
            self.winchM = kargs[0] if len(kargs) > 0 else None
            #self.winchEncoder = kargs[1] if len(kargs) > 1 else None
            if not (self.winchM):
                raise Exception("winch motor must be provided")

        else:
            self.winchM = hwFactory.getHardwareComponet("Arm" , "winch")

            #self.winchEncoder = self.winchM.getEncoder() if isinstance(self.winchM, rev.CANSparkMax) else None
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