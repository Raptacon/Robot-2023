from enum import Enum
import wpilib

class EPosition(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3 
class PositionChooser():

    def position(self) -> None:
        self.chooser = wpilib.SendableChooser()
        self.chooser.setDefaultOption("Left", EPosition.LEFT)
        self.chooser.addOption("Center", EPosition.CENTER)
        self.chooser.addOption("Right", EPosition.RIGHT)
        self.chooser.addOption("None", None)

        wpilib.SmartDashboard.putData("Autonomous Mode", self.chooser) 

    def getPosition(self):
        return self.chooser.getSelected() 

  
