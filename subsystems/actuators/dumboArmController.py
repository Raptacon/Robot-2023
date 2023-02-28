import commands2

import logging

log = logging.getLogger("Arm Controller")

class ArmController(commands2.SubsystemBase):

    def __init__(self, subsystem, *kargs,
                 **kwargs):
        super().__init__()
        #save for later use
        self.savedArgs = kargs
        self.savedKwargs = kwargs

        self.configMapper = kwargs["configMapper"]
        self.setAnglesDegrees = kwargs["setArmAnglesDegrees"]
        self.setArmLength = kwargs["setArmLengthUnits"]

    def setArmRotationSubsystem(self, armRotationSubsystem):
        self.armRotationSS = armRotationSubsystem

    def setArmExtensionSubsystem(self, armExtensionSubsystem):
        self.armExtensionSS = armExtensionSubsystem

    def getArmRotation(self):
        """TODO Make this work by lookup in future

        Returns:
            _type_: _description_
        """
        if hasattr(self, "armRotationSS"):
            return self.armRotationSS
        else:
            return None
            #TODO
            #self.getArmRotation = self.configMapper.getSubsystem("armRotation")
            #return self.armRotationSS

    def getArmExtension(self):
        return None
        if hasattr(self, "armExtensionSS"):
            return self.armExtensionSS
        else:
            self.getArmExtension = self.configMapper.getSubsystem("armExtension")
            return self.armExtensionSS

    def isArmPositioned(self):
        """
        Returns if arm is in postion
        """
        #TODO add support for length
        return self.getArmRotation().atSetpoint()

    def getReqSubsystems(self) -> list[commands2.Subsystem]:
        return [self, self.getArmRotation()]

    def setManipulator(self, angleDegrees, armLength):
        """Sets the angle and length of the manipulator
        Args:
            angleDegrees (_type_): angle of arm in degrees
            armLength (_type_): length of arm in units
        """
        self.getArmRotation().setSetpointDegrees(angleDegrees)

    def setFrontBottom(self):
        """
        sets the manipulator to the front bottom position
        """
        self.setManipulator(self.setAnglesDegrees["frontBottom"], self.setArmLength["frontBottom"])

    def setFrontCenter(self):
        """
        sets the manipulator to the front center position
        """
        self.setManipulator(self.setAnglesDegrees["frontMiddle"], self.setArmLength["frontMiddle"])

    def setFrontTop(self):
        """
        sets the manipulator to the front top position
        """
        self.setManipulator(self.setAnglesDegrees["frontTop"], self.setArmLength["frontTop"])

    def setTop(self):
        """
        sets the manipulator to the top position
        """
        self.setManipulator(self.setAnglesDegrees["top"], self.setArmLength["top"])

    def setBackTop(self):
        """
        sets the manipulator to the back top position
        """
        self.setManipulator(self.setAnglesDegrees["backTop"], self.setArmLength["backTop"])

    def setBackCenter(self):
        """
        sets the manipulator to the back center position
        """
        self.setManipulator(self.setAnglesDegrees["backMiddle"], self.setArmLength["backMiddle"])

    def setBackBottom(self):
        """
        sets the manipulator to the back bottom position
        """
        self.setManipulator(self.setAnglesDegrees["backBottom"], self.setArmLength["backBottom"])

