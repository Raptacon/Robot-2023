import commands2
import commands2.cmd
from commands.goToDist import GoToDist
from commands.autoGrabber import AutoGrabber
from subsystems.actuators.breadboxArmController import ArmController, getArmInstantCommand
from commands.turnToAngle import TurnToAngle
from subsystems.arm.grader import Grabber
from subsystems.drivetrains.westcoast import Westcoast
import wpilib
import navx
import logging
from position import EPosition
log = logging.getLogger("Auto")
class Autonomous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Westcoast, navx : navx.AHRS, armController : ArmController, grabber : Grabber, position : int) -> None:
        super().__init__()
       
        distance1 = wpilib.SmartDashboard.getNumber("Auto Distance 1", 7.25)
        distance2 = wpilib.SmartDashboard.getNumber("Auto Distance 2", 7.25)
        turnAngle = 30

        log.info(f"Auto Distance 1: {distance1}")
        log.info(f"Auto Distance 2: {distance2}")
        log.info(f"Auto Turn Angle: {turnAngle}")
       
        if (position == EPosition.CENTER):
            self.addCommands(
                getArmInstantCommand(armController, armController.setBackTop),
                commands2.WaitCommand(2),
                commands2.PrintCommand("Arm movement finished"),
                AutoGrabber(grabber, 1, False),
                commands2.PrintCommand("output cone"),
                GoToDist(distance1, drive),
                commands2.PrintCommand(f"GoToDist finished {distance1}")
                )
        if position == EPosition.LEFT:
                        self.addCommands(
                getArmInstantCommand(armController, armController.setBackTop),
                commands2.WaitCommand(2),
                commands2.PrintCommand("Arm movement finished"),
                AutoGrabber(grabber, 1, False),
                commands2.PrintCommand("output cone"),
                GoToDist(distance1, drive),
                commands2.PrintCommand(f"GoToDist finished {distance1}"),
                TurnToAngle(turnAngle, drive, navx),
                GoToDist(distance2, drive)
                )
        if position == EPosition.RIGHT:
            pass

