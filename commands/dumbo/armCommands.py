import commands2
import commands2.button
import commands2.cmd
from subsystems.actuators.dumboArmController import ArmController


def createArmPositionCommands(controller: commands2.button.CommandGenericHID, armController: ArmController):
    """
    Creates commands for each arm position
    """


    controller.POVDownLeft().onTrue(commands2.cmd.run(lambda: armController.setFrontBottom(), armController.getReqSubsystems()))
    controller.POVLeft().onTrue(commands2.cmd.run(lambda: armController.setFrontCenter(), armController.getReqSubsystems()))
    controller.POVUpLeft().onTrue(commands2.cmd.run(lambda: armController.setFrontTop(), armController.getReqSubsystems()))
    controller.POVUp().onTrue(commands2.cmd.run(lambda: armController.setTop(), armController.getReqSubsystems()))
    controller.POVUpRight().onTrue(commands2.cmd.run(lambda: armController.setBackTop(), armController.getReqSubsystems()))
    controller.POVRight().onTrue(commands2.cmd.run(lambda: armController.setBackCenter(), armController.getReqSubsystems()))
    controller.POVDownRight().onTrue(commands2.cmd.run(lambda: armController.setBackBottom(), armController.getReqSubsystems()))
