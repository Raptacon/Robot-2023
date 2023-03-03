import commands2
from commands.goToDist import GoToDist
#from commands.turnToAngle import TurnToAngle
from commands.balance import Balance
from commands.breadbox.breadboxAutoArm import AutoArm
from commands.breadbox.intakeAuto import AutoIntake
from subsystems.arm.grader import Grabber
from subsystems.drivetrains.westcoast import Westcoast
import navx
import commands2.cmd
class Autonomous(commands2.SequentialCommandGroup):
    def __init__(self, drive : Westcoast, navx : navx.AHRS, arm, grabber : Grabber) -> None:
        super().__init__()

        self.addCommands(
            AutoArm(arm, 135),
            AutoIntake(grabber, False, 2),
        )
