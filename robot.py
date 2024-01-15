#!/usr/bin/env python3

import typing
import wpilib
import commands2
import aprilTags
import pathFinder
import ntcore

from photonvision import PhotonCamera
from wpimath.geometry import Translation2d
from wpimath.geometry import Pose2d
from wpimath.geometry import Rotation2d
from robots.configBasedRobot import ConfigBaseCommandRobot
from robots.greenBot import GreenBot
from robots.breadboxBot import Breadbox
from wpilib import Field2d
from wpilib import SmartDashboard

class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run
    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.

        #determine the robot based on the config file
        #TODO

        if True:
            self.container = GreenBot()
        if False:
            self.container = ConfigBaseCommandRobot()
        if False:
            self.container = Breadbox()


        #starts the camera server for apriltags
        wpilib.CameraServer.launch()
        #starts feild representation in smartdashboard

        #starts the feild available on glass
        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)

        # Sets up Apriltag network tables
        self.nt = ntcore.NetworkTableInstance.getDefault()
        self.nt.setServer("10.32.0.79")
        self.nt.startClient3("3200 robot")

        # The camera name accoridng to the photonvision client (ipAddress:5800/#/dashboard)
        # Should be changed from being hard coded, or set a standard camera name
        cameraName = "Arducam"
        #connects a camera object to the network tables
        self.camera = PhotonCamera(self.nt, cameraName)

        #starts april tags
        self.AprilTags = aprilTags.AprilTags(self.camera)

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        self.container.disabledInit()

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        self.container.disabledPeriodic()

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.container.autonomousInit()
        self.autonomousCommand = None

        try:
            self.autonomousCommand = self.container.getAutonomousCommand()
        except Exception as err:
            wpilib.reportError(f"Autonoms command not found. {err}", True)

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

        self.container.autonomousPeriodic()


    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
        self.container.teleopInit()

        

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        self.container.teleopPeriodic()

        
        
    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        self.container.testInit()
        initPos = self.AprilTags.updatePose()
        finalPos = Pose2d(x = initPos.translation().X() + self.AprilTags.distToTag() - 1, y = initPos.translation().Y(), rotation = Rotation2d.fromDegrees(0))
        self.pathFinder = pathFinder.PathFinder(self.container.driveTrain, finalPos, self.AprilTags)

    def testPeriodic(self) -> None:
        self.container.testPeriodic()

        self.pathFinder.execute()

        '''updates the visual feild representation'''
        '''changes the 3d pose gotten from the april tags to a 2D pose'''
        robotPose3D = self.AprilTags.updatePose()
        robotPose2D = robotPose3D.toPose2d()
        self.field.setRobotPose(robotPose2D)


if __name__ == "__main__":
    wpilib.run(MyRobot)

