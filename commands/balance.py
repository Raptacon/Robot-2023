import navx
import commands2
import wpimath.controller
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

class Balance(commands2.CommandBase):


    # def init is being called
    def __init__(self, xKey : bool, driveTrain : DriveTrain):
        super().__init__()
        self.navx = navx._navx.AHRS.create_spi()
        self.startOrientation = {
            "x": self.navx.getRoll(),
            "y": self.navx.getPitch(),
            "z" : self.navx.getYaw()
            }

        self.pid = wpimath.controller.PIDController(0.024, 0.00095, 0.0001, 0.0001)
        self.pid.setTolerance(.8)
        self.xKey = xKey
        self.driveTrain = driveTrain

    def getPitch(self):
        return self.navx.getPitch() - self.startOrientation["y"]

    def dobalance(self) -> None:
        # z = self.navx.getYaw() - self.startOrientation["z"]
        y = self.navx.getPitch() - self.startOrientation["y"]
        # print(f"yaw: {z}")
        print(f"Trying to balance:: {y}")
        if y < 2.5 and y > -2.5:

            return 0
        # if z < -170 and z > -150:
        #     pass

        if y > 2.5:

            return self.pid.calculate(y)
        # if z < 20:
        #     return self.pid.calculate(z)

        if y < -2.5:

            return self.pid.calculate(y)

    def execute(self) -> None:
        print(f"XKey: {self.xKey}")
        if self.xKey:
            self.dobalance()

    def driveForward(self) -> None:
        self.driveTrain.drive(.5, .5)
        print("Forward")

    def driveBackwards(self) -> None:
        self.driveTrain.drive(.5, .5)
        print("Backwards")

    def stop(self) -> None:
        self.driveTrain.drive(0,0)
        print("stop")

