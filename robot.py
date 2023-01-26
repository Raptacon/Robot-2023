import wpilib
import ctre

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.motor = wpilib.Talon(0)
        self.motor.setInverted(True)
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        self.motor.set(self.stick.getY())


if __name__ == "__main__":
    wpilib.run(MyRobot)
