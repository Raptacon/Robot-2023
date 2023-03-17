from enum import Enum
import wpilib

class EPosition(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3
class PositionChooser():

    def position(self) -> None:
        self.chooser = wpilib.SendableChooser()
        self.chooser.setDefaultOption("Left", 1)
        self.chooser.addOption("Center", 2)
        self.chooser.addOption("Right", 3)
        self.chooser.addOption("None", None)

        wpilib.SmartDashboard.putData("Autonomous Mode", self.chooser)

    def getPosition(self):
        return self.chooser.getSelected()

