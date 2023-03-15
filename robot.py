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


        '''starts the camera server for apriltags'''
        wpilib.CameraServer.launch()
        '''starts feild representation in smartdashboard'''

        '''starts the feild available on glass'''
        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)

        '''sets up network tables'''
        nt = ntcore.NetworkTableInstance.getDefault()
        nt.startClient3("test code")
        nt.setServer("10.32.0.13")
        '''lets people know whether it was connected'''
        if nt.isConnected():
            print('Network tables Connected')

        '''connects a camera object to the network tables'''
        self.camera = PhotonCamera(nt, aprilTags.AprilTags.name)

        '''starts april tags'''
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

        '''updates the visual feild representation'''
        '''changes the 3d pose gotten from the april tags to a 2D pose'''
        '''this should also probably be in other periodics'''
        robotPose3D = self.AprilTags.updatePose()
        robotPose2D = robotPose3D.toPose2d()
        self.field.setRobotPose(robotPose2D)
        print(robotPose2D)
        
    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
        self.container.testInit()
        if(self.camera.hasTargets()):
            getInitPos = aprilTags.AprilTags.updatePose
            initPos = self.AprilTags.updatePose()
            oneMeter = Translation2d(x = 1, y = 0).X()
            finalPos = Pose2d(x = initPos.translation().X() + oneMeter, y = initPos.translation().Y(), rotation = initPos.rotation().toRotation2d())
            self.pathFinder = pathFinder.PathFinder(self.container.driveTrain, getInitPos, finalPos)


    def testPeriodic(self) -> None:
        self.container.testPeriodic()
        self.pathFinder.execute()


if __name__ == "__main__":
    wpilib.run(MyRobot)

