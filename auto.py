import commands2
import commands2.cmd
from commands.goToDist import GoToDist
from commands.turnToAngle import TurnToAngle
from commands.autoGrabber import AutoGrabber
from subsystems.actuators.breadboxArmController import ArmController
from subsystems.arm.grader import Grabber
from subsystems.drivetrains.westcoast import Westcoast
import wpilib
import navx
import logging
log = logging.getLogger("Auto")
class Autonomous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Westcoast, navx : navx.AHRS, armController : ArmController, grabber : Grabber) -> None:
        super().__init__()

        distance1 = wpilib.SmartDashboard.getNumber("Auto Distance 1", 7.25)
        distance2 = wpilib.SmartDashboard.getNumber("Auto Distance 2", 7.25)
        turnAngle = 180

        log.info(f"Auto Distance 1: {distance1}")
        log.info(f"Auto Distance 2: {distance2}")
        log.info(f"Auto Turn Angle: {turnAngle}")

        self.addCommands(
            commands2.cmd.run(lambda: armController.setBackCenter(), armController.getReqSubsystems()),
            commands2.PrintCommand("Arm movement finished"),
            AutoGrabber(grabber, 2, False),
            commands2.PrintCommand("output cone"),
            GoToDist(distance1, drive),
            commands2.PrintCommand(f"GoToDist finished {distance1}"),
            TurnToAngle(turnAngle, drive, navx),
            commands2.PrintCommand(f"TurnToAngle finished {turnAngle}"),
            GoToDist(distance2, drive),
            commands2.PrintCommand(f"GoToDist2 finished {distance2}")
        )
