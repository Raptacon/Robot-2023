import commands2
from commands.goToDist import GoToDist
#from commands.turnToAngle import TurnToAngle
from subsystems.drivetrains.westcoast import Westcoast
from commands.balance import Balance
from commands.autoBalance import AutoBalance
import wpilib
import navx
import logging
log = logging.getLogger("Auto")
class Autonomous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Westcoast, navx : navx.AHRS) -> None:
        super().__init__()
        
        distance1 = wpilib.SmartDashboard.getNumber("Auto Distance 1", 7.25)
        distance2 = wpilib.SmartDashboard.getNumber("Auto Distance 2", 7.25)
        turnAngle = 180

        log.info(f"Auto Distance 1: {distance1}")
        log.info(f"Auto Distance 2: {distance2}")
        log.info(f"Auto Turn Angle: {turnAngle}")

        self.addCommands(
            GoToDist(distance1, drive),
            commands2.PrintCommand(f"GoToDist finished {distance1}"),
            AutoBalance(drive, Balance(True, drive)),
            commands2.PrintCommand("Balance finished"),
        )
