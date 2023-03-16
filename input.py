import wpilib
import wpimath.filter
import wpimath

class Input:

    def getStickSlew(axis: wpilib.XboxController.Axis, port : int, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(port).getRawAxis(axis), 0.1))

    def getStick(axis: wpilib.XboxController.Axis, port : int, invert: bool = False):
        sign = -1.0 if invert else 1.0
        return lambda: wpimath.applyDeadband(sign * wpilib.XboxController(port).getRawAxis(axis), 0.1)

    def getButton(self, ButtonName : str, XboxController : wpilib.XboxController):
        """
        Takes in a string which acts as the key for a button and returns whether or not the button is pressed.
        """
        buttons = {"XButton" : XboxController.getXButton(),
        "AButton" : XboxController.getAButton(),"BButton" : XboxController.getBButton(),
        "YButton" : XboxController.getYButton(), "RightTrigger" : XboxController.getRightTriggerAxis(),
        "RightBumper" : XboxController.getRightBumper(), "LeftTrigger" : XboxController.getLeftTriggerAxis(),
        "LeftBumper" : XboxController.getLeftBumper(), "RightStickButton" : XboxController.getRightStickButton(),
        "LeftStickButton" : XboxController.getLeftStickButton()}
        return buttons[ButtonName]

    def getPOV(self, XboxController : wpilib.XboxController) -> int:
        """
        returns the POV of the controller at the index of 0. Returns an angle from 0 - 360
        """
        return XboxController.getPOV()
