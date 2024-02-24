import commands2

from typing import Callable
from subsystem.sparkyIntakePivot import IntakePivot
class pivotController(commands2.SubsystemBase):

    def __init__(self,):
        super().__init__()
        self.calibrated = False
        #save for later use

    def calibrate(self):
        if(not self.calibrated):
            self.getIntakeRotation().pivotMotor.set(-0.2)
            if(self.getIntakeRotation().getLimit()):
                self.calibrated = True
                self.getIntakeRotation().encoderOffset = self.getIntakeRotation().encoder.getAbsolutePosition()

    def setIntakeRotationSubsystem(self, RotationSubsystem):
        self.intakeRotationSS = RotationSubsystem

    def getIntakeRotation(self) -> IntakePivot:
        """TODO Make this work by lookup in future

        Returns:
            _type_: _description_
        """
        if hasattr(self, "intakeRotationSS"):
            return self.intakeRotationSS
        else:
            return None

    def isPivotPositioned(self, tolerance = None):
        """
        Returns if pviot is in postion
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
            angleDegrees (_type_): angle of pivot in degrees
        """
        if(not self.calibrated):
            self.calibrate()
            return
        self.getIntakeRotation().setSetpointDegrees(angleDegrees)
        self.getIntakeRotation().enable()

    def setGroundPickup(self):
        """
        sets the manipulator to the ground position
        """
        self.setManipulator(270)

    def setHandOffPickup(self):
        """
        sets the manipulator to the handoff position
        """
        self.setManipulator(0)

def getPivotFunctionalCommand(pivotController: pivotController, func: Callable, tolerance = 0.1):
    """
    Creates a functional command for the pivot
    Args:
        pivotController (pivotController): pivot controller to use
        func (Callable): function from pivot controller to run
    Returns: functional command
    """

    #example usage without command group
    #cmd = getPivotFunctionalCommand(self.robot_arm_controller, self.robot_arm_controller.setTop)
    #commands2.CommandScheduler.schedule(commands2.CommandScheduler.getInstance(), cmd)

    cmd = commands2.FunctionalCommand(func, lambda *args, **kwargs: None, lambda x: print("Done"), lambda : pivotController.isArmPositioned(tolerance))
    cmd.addRequirements(pivotController.getReqSubsystems())
    return cmd

def getPivotInstantCommand(pivotController: pivotController, func: Callable, tolerance = 0.1):
    """
    Creates a functional command for the pivot
    Args:
        pivotController (pivotController): pivot controller to use
        func (Callable): function from pivot controller to run
    Returns: functional command
    """

    #example usage without command group
    #cmd = getPivotInstantCommand(self.robot_arm_controller, self.robot_arm_controller.setTop)
    #commands2.CommandScheduler.schedule(commands2.CommandScheduler.getInstance(), cmd)

    cmd = commands2.InstantCommand(func)
    cmd.addRequirements(pivotController.getReqSubsystems())
    return cmd
