from Input import input
import wpilib
import enum
from wpilib.shuffleboard import Shuffleboard
class Selector:

    class Selection(enum.Enum):
        Top = enum.auto()
        TopRight = enum.auto()
        Right = enum.auto()
        BottomRight = enum.auto()
        Bottom = enum.auto()
        BottomLeft = enum.auto()
        Left = enum.auto()
        TopLeft = enum.auto()
        Middle = enum.auto()

    selections = {-1 : Selection.Middle, 0 : Selection.Top, 45 : Selection.TopRight, 90 : Selection.Right, 135 : Selection.BottomRight, 180 : Selection.Bottom, 225 : Selection.BottomLeft, 270 : Selection.Left, 315 : Selection.TopLeft}
    selectionsView = {Selection.Middle : "Middle", Selection.Top : "Top", Selection.TopRight : "TopRight", Selection.Right : "Right", Selection.BottomRight : "BottomRight",Selection.Bottom : "Bottom", Selection.BottomLeft : "BottomLeft", Selection.Left : "Left", Selection.TopLeft : "TopLeft"}
    selection = Selection.Middle

    def __init__(self) -> None:
        """
        Sets up the shuffleboard to display the current selection
        """
        self.dashboard = Shuffleboard.getTab("Selections")
        self.ControllerEntry = self.dashboard.add(title ="Selection",defaultValue=self.selectionsView[self.selection]).getEntry()

    def GetSelection(self, XboxController : wpilib.XboxController):
        """
        sets the current selection and sends the value to shuffleboard to display
        """
        self.selection = self.selections[input().getPOV(XboxController)]
        self.ControllerEntry.setString(self.selectionsView[self.selection])
