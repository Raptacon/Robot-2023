import commands2
from commands.goToDist import GoToDist
from commands.turnToAngle import TurnToAngle
from subsystems.drivetrains.westcoast import Westcoast
import navx

class Autonoumous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Westcoast, navx : navx.AHRS) -> None:
        super().__init__()

        self.addCommands(
            GoToDist(.5, 10, drive),
            commands2.PrintCommand("Started TurnToAngle"),
            TurnToAngle(.35, 180, drive, navx),
            commands2.PrintCommand("Finished TurnToAngle"),
            GoToDist(.4, 10, drive)
        )

