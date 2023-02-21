import wpilib
import wpimath.filter
import wpimath

class input:

    def getStick(axis: wpilib.XboxController.Axis, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))

    def getButton(self, ButtonName : str, XboxController : wpilib.XboxController):
        """
        Takes in a string which acts as the key for a button and returns whether or not the button is pressed.
        """
        buttons = {"XButton" : XboxController.getXButton(),
        "AButton" : XboxController.getAButton(),"BButton" : XboxController.getBButtonPressed(),
        "YButton" : XboxController.getYButtonPressed(), "RightTrigger" : XboxController.getRightTriggerAxis(),
        "RightBumper" : XboxController.getRightBumperPressed(), "LeftTrigger" : XboxController.getLeftTriggerAxis(),
        "LeftBumper" : XboxController.getLeftBumperPressed(), "RightStickButton" : XboxController.getRightStickButtonPressed(),
        "LeftStickButton" : XboxController.getLeftStickButtonPressed()}
        return buttons[ButtonName]

    def getPOV(self, XboxController : wpilib.XboxController) -> int:
        """
        returns the POV of the controller at the index of 0. Returns an angle from 0 - 360
        """
        return XboxController.getPOV()
