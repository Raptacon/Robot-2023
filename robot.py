import wpilib
import wpilib.drive


class myRobot(wpilib.TimedRobot):
    def robotInit(self):
            'sets the motor and input'
            self.Motor = wpilib.Jaguar(1)
            self.stick = wpilib.Joystick(0)

    'moves the motor forword when the joystick is given forward'
    def teleopPeriodic(self):
        self.Motor.setInverted(True)
        self.Motor.set(self.stick.getY())

'starts the code'
if __name__ == '__main__':
    wpilib.run(myRobot)