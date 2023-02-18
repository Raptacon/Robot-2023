import wpilib
import wpimath.filter
import wpimath

class input:

    def getStick(axis: wpilib.XboxController.Axis, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(0).getRawAxis(axis), 0.1))

    def getButton(self, ButtonName : str, XboxController : wpilib.XboxController):
        buttons = {"XButton" : wpilib.XboxController.getXButtonPressed(XboxController),
        "AButton" : wpilib.XboxController.getAButton(XboxController),"BButton" : wpilib.XboxController.getBButtonPressed(XboxController),
        "YButton" : wpilib.XboxController.getYButtonPressed(XboxController), "RightTrigger" : wpilib.XboxController.getRightTriggerAxis(XboxController),
        "RightBumper" : wpilib.XboxController.getRightBumperPressed(XboxController), "LeftTrigger" : wpilib.XboxController.getLeftTriggerAxis(XboxController),
        "LeftBumper" : wpilib.XboxController.getLeftBumperPressed(XboxController), "RightStickButton" : wpilib.XboxController.getRightStickButtonPressed(XboxController),
        "LeftStickButton" : wpilib.XboxController.getLeftStickButtonPressed(XboxController)}
        return buttons[ButtonName]
