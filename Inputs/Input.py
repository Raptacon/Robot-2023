from wpilib import Joystick, XboxController
from wpilib.interfaces import GenericHID
import typing

class JoystickMap():
    """
    Sets up and gets the input from a joystick
    """
    def __init__(self, joystick: Joystick):
        #initializes joysticks
        self.drive = joystick
        self.JoystickInput()

    def JoystickInput(self):
        self.driveX = self.drive.getRawAxis(0)
        self.driveY = self.drive.getRawAxis(1)
        self.driveZ = self.drive.getRawAxis(2)
        self.trigger = Joystick.getTrigger(self.drive)
        self.button2 = self.drive.getRawButton(0)
        self.button3 = self.drive.getRawButton(1)
        self.button4 = self.drive.getRawButton(2)
        self.button5 = self.drive.getRawButton(3)
        self.button6 = self.drive.getRawButton(4)
        self.button7 = self.drive.getRawButton(5)
        self.button8 = self.drive.getRawButton(6)
        self.button9 = self.drive.getRawButton(7)
        self.button10 = self.drive.getRawButton(8)
        self.button11 = self.drive.getRawButton(9)
        self.POV = self.drive.getPOV()

    def getDriveJoystick(self):
        return self.drive

    def getDriveXAxis(self):
        return self.driveX

    def getDriveYAxis(self):
        return self.driveY

    def getDriveZAxis(self):
        return self.driveZ

    def getTrigger(self):
        return self.trigger

    def getButton2(self):
        return self.button2

    def getButton3(self):
        return self.button3

    def getButton4(self):
        return self.button4

    def getButton5(self):
        return self.button5

    def getButton6(self):
        return self.button6

    def getButton7(self):
        return self.button7

    def getButton8(self):
        return self.button8

    def getButton9(self):
        return self.button9

    def getButton10(self):
        return self.button10

    def getButton11(self):
        return self.button11

    def getPOV(self):
        return self.POV

class XboxMap():
    """
    Holds the mappings to TWO Xbox controllers, one for driving, one for mechanisms
    """
    def __init__(self, Xbox1: XboxController, Xbox2: XboxController):
        self.drive = Xbox1
        self.mech = Xbox2
        self.controllerInput()
        #Button mappings

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        (Should only be used for axes while buttonManager has no equal for axes)
        """
        #Drive Controller inputs
        self.driveLeft = self.drive.getRawAxis(XboxController.Axis.kLeftY)
        self.driveRight = self.drive.getRawAxis(XboxController.Axis.kRightY)
        self.driveLeftHoriz = self.drive.getRawAxis(XboxController.Axis.kLeftX)
        self.driveRightHoriz = self.drive.getRawAxis(XboxController.Axis.kRightX)
        self.driveRightTrig = self.drive.getRawAxis(XboxController.Axis.kRightTrigger)
        self.driveLeftTrig = self.drive.getRawAxis(XboxController.Axis.kLeftTrigger)
        self.driveDPad = self.drive.getPOV()
        self.driveA = self.drive.getAButton()
        self.driveX = self.drive.getXButton()
        #Mechanism controller inputs
        self.mechLeft = self.mech.getRawAxis(XboxController.Axis.kLeftY)
        self.mechRight = self.mech.getRawAxis(XboxController.Axis.kRightY)
        self.mechLeftHoriz = self.mech.getRawAxis(XboxController.Axis.kLeftX)
        self.mechRightHoriz = self.mech.getRawAxis(XboxController.Axis.kRightX)
        self.mechRightTrig = self.mech.getRawAxis(XboxController.Axis.kRightTrigger)
        self.mechLeftTrig = self.mech.getRawAxis(XboxController.Axis.kLeftTrigger)
        self.mechX = self.mech.getXButton()
        self.mechA = self.mech.getAButton()
        self.mechDPad = self.mech.getPOV()
        self.mechLeftBumper = self.mech.getLeftBumper()

    def getDriveController(self):
        return self.drive

    def getMechController(self):
        return self.mech

    def getDriveLeft(self):
        return self.driveLeft

    def getDriveRight(self):
        return self.driveRight

    def getDriveLeftHoriz(self):
        return self.driveLeftHoriz

    def getDriveRightHoriz(self):
        return self.driveRightHoriz

    def getDriveRightTrig(self):
        return self.driveRightTrig

    def getDriveLeftTrig(self):
        return self.driveLeftTrig

    def getDriveDPad(self):
        return self.driveDPad

    def getDriveA(self):
        return self.driveA

    def getDriveX(self):
        return self.driveX

    def getMechLeft(self):
        return self.mechLeft

    def getMechRight(self):
        return self.mechRight

    def getMechLeftHoriz(self):
        return self.mechLeftHoriz

    def getMechRightHoriz(self):
        return self.mechRightHoriz

    def getMechRightTrig(self):
        return self.mechRightTrig

    def getMechLeftTrig(self):
        return self.mechLeftTrig

    def getMechDPad(self):
        return self.mechDPad

    def getMechLeftBumper(self):
        return self.mechLeftBumper

    def getMechX(self):
        return self.mechX

    def getMechA(self):
        return self.mechA

class KeyboardMap():
    def keyboardInput(self):
        self.driveX = typing.Callable[[], float]
        self.driveY = typing.Callable[[], float]
        self.driveZ = typing.Callable[[], float]