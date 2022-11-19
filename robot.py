# Module imports:
import wpilib
from wpilib import XboxController, DriverStation, SerialPort, CameraServer
from magicbot import MagicRobot, tunable

# Component imports:
from tests.axesXYR import AxesTransforms, AxesXYR
from tests.buttonManager import ButtonManager, ButtonEvent
from tests.driveTrain import DriveTrain
from tests.driveTrainHandler import DriveTrainHandler
from tests.XYRDrive import XYRDrive
import os

# Other imports:
from robotMap import RobotMap, XboxMap
from networktables import NetworkTables
from tests.motorHelper import createMotor
from tests.math import expScale

# Test imports:

class MyRobot(MagicRobot):
    """
    Base robot class of Magic Bot Type
    """
    driveTrain: DriveTrain
    xyrDrive: XYRDrive
    buttonManager: ButtonManager
    driveTrainHandler: DriveTrainHandler
    xyrDrive: XYRDrive
    allianceColor: DriverStation.Alliance
    axesXYR: AxesXYR

    # Test code:
    # If controller input is below this value, it will be set to zero.
    # This avoids accidental input, as we are now overriding autonomous
    # components on controller input.
    controllerDeadzone = .06
    sensitivityExponent = 1.8
    # Eventually have a way to change this based on dropdown menu
    controlModes = {"Tank": AxesTransforms.kTank,
                    "Arcade": AxesTransforms.kArcade,
                    "Swerve": AxesTransforms.kSwerve}
    controlmode = AxesTransforms.kTank

    robotDir = os.path.dirname(os.path.abspath(__file__))

    def createObjects(self):
        """
        Robot-wide initialization code should go here. Replaces robotInit
        """
        self.map = RobotMap()
        self.xboxMap = XboxMap(XboxController(1), XboxController(0))
        self.currentRobot = self.map.configMapper.getCompatibility()

        try:
            driveTrainSubsystem = self.map.configMapper.getSubsystem("driveTrain")['driveTrain']
        except TypeError:
            print("Robot does not have a drive train type")
            driveTrainSubsystem = None

        if driveTrainSubsystem != None and "type" in driveTrainSubsystem:
            self.driveTrainType = str(driveTrainSubsystem["type"])
        else:
            self.driveTrainType = "Unknown"

        self.driverStation = DriverStation.getInstance()


        self.allianceColor = self.driverStation.getAlliance()
        if self.allianceColor == self.driverStation.Alliance.kBlue:
            self.allianceColor = "blue"
        elif self.allianceColor == self.driverStation.Alliance.kRed:
            self.allianceColor = "red"
        else:
            self.allianceColor = "???"

        ReadBufferValue = 18

        self.MXPserial = SerialPort(115200, SerialPort.Port.kMXP, 8,
        SerialPort.Parity.kParity_None, SerialPort.StopBits.kStopBits_One)
        self.MXPserial.setReadBufferSize(ReadBufferValue)
        self.MXPserial.setWriteBufferSize(2 * ReadBufferValue)
        self.MXPserial.setWriteBufferMode(SerialPort.WriteBufferMode.kFlushOnAccess)
        self.MXPserial.setTimeout(.1)

        self.smartDashboardTable = NetworkTables.getTable('SmartDashboard')

        # Drop down control mode menu
        self.chooser = wpilib.SendableChooser()

        for key, item in self.controlModes.items():
            if item == self.controlmode:
                self.chooser.setDefaultOption(key, self.controlmode)
            self.chooser.addOption(key, item)

        wpilib.SmartDashboard.putData("Control Mode", self.chooser)

        self.instantiateSubsystemGroup("motors", createMotor)


        # Check each component for compatibility
        componentList = [DriveTrain, ButtonManager, DriveTrainHandler],
        CameraServer.launch()


    def autonomousInit(self):
        """Run when autonomous is enabled."""
        self.shooter.autonomousEnabled()
        self.loader.stopLoading()


    def teleopInit(self):
        # Register button events for doof
        # self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kX, ButtonEvent.kOnPress, self.pneumatics.toggleLoader)
        # self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kA, ButtonEvent.kOnPress, self.loader.setAutoLoading)
        # self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kB, ButtonEvent.kOnPress, self.loader.setManualLoading)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.shooter.startShooting)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.shooter.setManualShooting)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnPress, self.loader.stopLoading)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnRelease, self.shooter.doneShooting)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kY, ButtonEvent.kOnRelease, self.loader.determineNextAction)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.driveTrain.enableCreeperMode)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnPress, self.loader.stopLoading)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnRelease, self.shooter.doneShooting)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnRelease, self.loader.determineNextAction)
        # self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kB, ButtonEvent.kOnRelease, self.autoShoot.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.drive, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.driveTrain.disableCreeperMode)

        """
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnPress, self.elevator.setRaise)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.elevator.setLower)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.elevator.stop)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kRightBumper, ButtonEvent.kOnPress, self.navx.reset)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnPress, self.goToDist.start)
        self.buttonManager.registerButtonEvent(self.xboxMap.mech, XboxController.Button.kLeftBumper, ButtonEvent.kOnRelease, self.goToDist.stop)
        """


        self.driveTrain.setBraking(True)

        self.prevMechAState = False

    def teleopPeriodic(self):
        """
        Must include. Called repeatedly while running teleop.
        """
        self.xboxMap.controllerInput()

        #This variable determines whether to use controller input for the drivetrain or not.
        #If we are using a command (such as auto align) that uses the drivetrain, we don't want to use the controller's input because it would overwrite
        #what the component is doing.

        driveLeftY = expScale(self.xboxMap.getDriveLeft(), self.sensitivityExponent)
        driveRightY = expScale(self.xboxMap.getDriveRight(), self.sensitivityExponent)
        driveLeftX = expScale(self.xboxMap.getDriveLeftHoriz(), self.sensitivityExponent)
        driveRightX = expScale(self.xboxMap.getDriveRightHoriz(), self.sensitivityExponent)
        ##mechLeftX = expScale(self.xboxMap.getMechLeftHoriz(), 2.3)

        Axes = [driveLeftX, driveLeftY, driveRightX, driveRightY]

        # deadzone clamping
        for i, axis in enumerate(Axes):
            if abs(axis) < self.controllerDeadzone:
                Axes[i] = 0

        self.controlmode = self.chooser.getSelected()
        # If the drivers have any input outside deadzone, take control.
        if abs(driveRightY) + abs(driveLeftY) + abs(driveRightX) != 0:
            vector = self.axesXYR.transform(self.controlmode, Axes)
            self.xyrDrive.xyrdrive(self, vector)


        self.prevMechAState = self.xboxMap.getMechA()



    def testInit(self):
        """
        Function called when testInit is called.
        """
        print("testInit was Successful")

    def testPeriodic(self):
        """
        Called during test mode alot
        """
        pass
        #pos counterclockwise, neg clockwise

    def instantiateSubsystemGroup(self, groupName, factory):
        """
        For each subsystem find all groupNames and call factory.
        Each one is saved to groupName_subsystem and subsystem_groupName
        """
        config = self.map.configMapper
        containerName = "subsystem" + groupName[0].upper() + groupName[1:]

        if not hasattr(self, containerName):
            setattr(self, containerName, {})
            self.subsystemGyros = {}

        # note this is a dictionary reference, so changes to it
        # are changes to self.<containerName>
        container = getattr(self, containerName)

        subsystems = config.getSubsystems()
        createdCount = 0
        for subsystem in subsystems:
            items = {key: factory(descp) for (key, descp) in config.getGroupDict(subsystem, groupName).items()}
            if(len(items) == 0):
                continue
            container[subsystem] = items
            createdCount += len(container[subsystem])
            groupName_subsystem = "_".join([groupName,subsystem])
            self.logger.info("Creating %s", groupName_subsystem)
            setattr(self, groupName_subsystem, container[subsystem])

        self.logger.info(f"Created {createdCount} items for {groupName} groups with `{factory.__name__}` into `{containerName}")

    def disabledInit(self):
        """
        What the robot runs on disabled start
        NEVER RUN ANYTHING THAT MOVES ANYTHING HERE
        """
        self.driveTrain.setBraking(False)

    def disabledPeriodic(self):
        """
        Runs repeatedly while disabled
        NEVER RUN ANYTHING THAT MOVES ANYTHING HERE
        """
        pass

if __name__ == '__main__':
    wpilib.run(MyRobot)