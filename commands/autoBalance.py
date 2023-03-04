from commands.balance import Balance
import commands2
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

class AutoBalance(commands2.CommandBase):
    def __init__(self, drive : DriveTrain, balance : Balance) -> None:
        super().__init__()
        self.balance = balance
        self.drive = drive

    def execute(self) -> None:
        self.balance.execute()
        self.drive.drive(self.balance.dobalance(), self.balance.dobalance())

    def isFinished(self) -> bool:
        return self.balance.getPitch() < 2.5 and self.balance.getPitch() > -2.5

    def end(self, interrupted: bool) -> None:
        self.drive.drive(0, 0)
