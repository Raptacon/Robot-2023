import commands2
import commands2.button
import commands2.cmd
from subsystems.actuators.breadboxArmController import ArmController
from subsystems.actuators.breadboxArmRotation import ArmRotation
from subsystems.actuators.breadboxWinch import Winch


def createArmPositionCommands(controller: commands2.button.CommandGenericHID, xbox: commands2.button.CommandXboxController, armController: ArmController, arm_subsystem: ArmRotation):
    """
    Creates commands for each arm position
    """

    xbox.back().onTrue(commands2.cmd.run(lambda: armController.setFrontBottom(), armController.getReqSubsystems()))
    xbox.start().onTrue(commands2.cmd.run(lambda: armController.setFrontCenter(), armController.getReqSubsystems()))
    xbox.X().onTrue(commands2.cmd.run(lambda: armController.setFrontTop(), armController.getReqSubsystems()))
    controller.POVUp().onTrue(commands2.cmd.run(lambda: armController.setTop(), armController.getReqSubsystems()))
    xbox.Y().onTrue(commands2.cmd.run(lambda: armController.setBackTop(), armController.getReqSubsystems()))
    xbox.B().onTrue(commands2.cmd.run(lambda: armController.setBackCenter(), armController.getReqSubsystems()))
    xbox.A().onTrue(commands2.cmd.run(lambda: armController.setBackBottom(), armController.getReqSubsystems()))
    xbox.rightStick().onTrue(commands2.cmd.runOnce(lambda: arm_subsystem.toggleBrake(), [arm_subsystem]))
