
import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
       
        self.right_motor = wpilib.Spark(1)
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.right_motor.set(self.stick.getY())


if __name__ == "__main__":
    wpilib.run(MyRobot)