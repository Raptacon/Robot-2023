from enum import Enum
import wpilib

class position(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3 
class Position():

    def __init__(self) -> None:
        self.chooser = wpilib.SendableChooser()
        self.chooser.setDefaultOption("Left", Position.LEFT)
        self.chooser.addOption("Center", Position.CENTER)
        self.chooser.addOption("Right", Position.RIGHT)
        self.chooser.addOption("None", None)

        wpilib.SmartDashboard.putData("Autonomous Mode", self.chooser) 

    def getPosition(self):
        return self.chooser.getSelected() 

  
