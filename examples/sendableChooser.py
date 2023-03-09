# This is an example of how to do do a chooser (pulldown menu options) in the SmartDashboard
import wpilib

from enum import Enum
class Position(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3


# SmartDashboard interface
chooser = wpilib.SendableChooser()
chooser.setDefaultOption("Left", Position.LEFT)
chooser.addOption("Right", Position.RIGHT)
chooser.addOption("Center", Position.CENTER)
chooser.addOption("None", None)
# must PutData after setting up objects
wpilib.SmartDashboard.putData("Autonomous Mode", chooser)

# Run this in the sim, open Network Tables, Transitory Values, Smart Dashboard, Autonomous Mode (or whatever you set with putData) and note the values for active and options (should be a list of Left, Right, Center, None)
