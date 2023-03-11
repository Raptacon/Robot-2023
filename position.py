from enum import Enum
import wpilib

class Position(Enum):

    def chooser(self) -> None:
        LEFT = 1
        CENTER = 2
        RIGHT = 3
        
        self.chooser = wpilib.SendableChooser()
        self.chooser.setDefaultOption("Left", Position.LEFT)
        self.chooser.addOption("Center", Position.CENTER)
        self.chooser.addOption("Right", Position.RIGHT)
        self.chooser.addOption("None", None)

        wpilib.SmartDashboard.putData("Autonomous Mode", self.chooser)