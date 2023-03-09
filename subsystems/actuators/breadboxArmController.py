import commands2

import logging
from typing import Callable

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
        if hasattr(self, "armExtensionSS"):
            return self.armExtensionSS
        else:
            return None

    def isArmPositioned(self, tolerance = None):
        """
        Returns if arm is in postion
        """
        #TODO add support for length
        if tolerance:
            return self.getArmRotation().closeToSetpoint(tolerance)
        else:
            return self.getArmRotation().atSetpoint()
    isArmPositioned

    def getReqSubsystems(self) -> list[commands2.Subsystem]:
        return [self, self.getArmRotation()]

    def setManipulator(self, angleDegrees, armLength):
        """Sets the angle and length of the manipulator
        Args:
            angleDegrees (_type_): angle of arm in degrees
        """
        self.getArmRotation().setSetpointDegrees(angleDegrees)
        self.getArmRotation().enable()
        self.getArmExtension().setDistance(armLength)
        self.getArmExtension().execute()

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



def getArmFunctionalCommand(armController: ArmController, func: Callable, tolerance = 0.1):
    """
    Creates a functional command for the arm
    Args:
        armController (ArmController): arm controller to use
        func (Callable): function from arm controller to run
    Returns: functional command
    """

    #example usage without command group
    #cmd = getArmFunctionalCommand(self.robot_arm_controller, self.robot_arm_controller.setTop)
    #commands2.CommandScheduler.schedule(commands2.CommandScheduler.getInstance(), cmd)

    cmd = commands2.FunctionalCommand(func, lambda *args, **kwargs: None, lambda x: print("Done"), lambda : armController.isArmPositioned(tolerance))
    cmd.addRequirements(armController.getReqSubsystems())
    return cmd


def getArmInstantCommand(armController: ArmController, func: Callable, tolerance = 0.1):
    """
    Creates a functional command for the arm
    Args:
        armController (ArmController): arm controller to use
        func (Callable): function from arm controller to run
    Returns: functional command
    """

    #example usage without command group
    #cmd = getArmFunctionalCommand(self.robot_arm_controller, self.robot_arm_controller.setTop)
    #commands2.CommandScheduler.schedule(commands2.CommandScheduler.getInstance(), cmd)

    cmd = commands2.InstantCommand(func)
    cmd.addRequirements(armController.getReqSubsystems())
    return cmd
