import commands2

from typing import Callable

from subsystem.swerveIntakePivot import SwerveIntakePivot

import wpilib

class pivotController(commands2.SubsystemBase):

    def __init__(self,):
        super().__init__()
        #save for later use

    def setIntakeRotationSubsystem(self, RotationSubsystem):
        self.intakeRotationSS = RotationSubsystem

    def getIntakeRotation(self) -> SwerveIntakePivot:
        """TODO Make this work by lookup in future

        Returns:
            _type_: _description_
        """
        if hasattr(self, "intakeRotationSS"):
            return self.intakeRotationSS
        else:
            return None
            #TODO
            #self.getArmRotation = self.configMapper.getSubsystem("armRotation")
            #return self.armRotationSS

    def isPivotPositioned(self, tolerance = None):
        """
        Returns if arm is in postion
        """
        #TODO add support for length
        if tolerance:
            return self.getIntakeRotation().closeToSetpoint(tolerance)
        else:
            return self.getIntakeRotation().atSetpoint()
    isPivotPositioned

    def getReqSubsystems(self) -> list[commands2.Subsystem]:
        return [self, self.getIntakeRotation()]

    def setManipulator(self, angleDegrees):
        """Sets the angle and length of the manipulator
        Args:
            angleDegrees (_type_): angle of arm in degrees
        """
        self.getIntakeRotation().setSetpointDegrees(angleDegrees)
        self.getIntakeRotation().enable()

    def setGroundPickup(self):
        """
        sets the manipulator to the ground position
        """
        self.setManipulator(335)
        wpilib.SmartDashboard.putBoolean("Intake grounded", True)

    def setHandOffPickup(self):
        """
        sets the manipulator to the handoff position
        """
        self.setManipulator(50)
        wpilib.SmartDashboard.putBoolean("Intake grounded", False)

def getPivotFunctionalCommand(pivotController: pivotController, func: Callable, tolerance = 0.1):
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

    cmd = commands2.FunctionalCommand(func, lambda *args, **kwargs: None, lambda x: print("Done"), lambda : pivotController.isArmPositioned(tolerance))
    cmd.addRequirements(pivotController.getReqSubsystems())
    return cmd


def getPivotInstantCommand(pivotController: pivotController, func: Callable, tolerance = 0.1):
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
    cmd.addRequirements(pivotController.getReqSubsystems())
    return cmd
