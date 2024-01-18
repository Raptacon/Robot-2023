import wpilib
import wpimath.filter
import wpimath

class Input:

    def getStickSlew(axis: wpilib.XboxController.Axis, port : int, invert: bool = False):
        sign = -1.0 if invert else 1.0
        slew = wpimath.filter.SlewRateLimiter(3)
        if wpilib.XboxController(port).isConnected():
            return lambda: slew.calculate(wpimath.applyDeadband(sign * wpilib.XboxController(port).getRawAxis(axis), 0.1))
        else:
            return lambda: 0.0

    def getStick(axis: wpilib.XboxController.Axis, port : int, invert: bool = False):
        sign = -1.0 if invert else 1.0
        
        if wpilib.XboxController(port).isConnected():
            return lambda: wpimath.applyDeadband(sign *  wpilib.XboxController(port).getRawAxis(axis), 0.1)
        else:
            return lambda: 0.0

    def getButton(self, ButtonName : str, XboxController : wpilib.XboxController):
        """
        Takes in a string which acts as the key for a button and returns whether or not the button is pressed.
        """
        #Check if controller exists
        if not XboxController.isConnected(): 
            return False

        buttons = {
            "XButton" : XboxController.getXButton(),
            "AButton" : XboxController.getAButton(),
            "BButton" : XboxController.getBButton(),
            "YButton" : XboxController.getYButton(), 
            "RightTrigger" : XboxController.getRightTriggerAxis(),
            "RightBumper" : XboxController.getRightBumper(), 
            "LeftTrigger" : XboxController.getLeftTriggerAxis(),
            "LeftBumper" : XboxController.getLeftBumper(), 
            "RightStickButton" : XboxController.getRightStickButton(),
            "LeftStickButton" : XboxController.getLeftStickButton()
        }
        return buttons[ButtonName]

    def getPOV(self, XboxController : wpilib.XboxController) -> int:
        """
        returns the POV of the controller at the index of 0. Returns an angle from 0 - 360
        """
        return XboxController.getPOV()
