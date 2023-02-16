import navx
import commands2

class Balance(commands2.CommandBase):
    # def init is being called
    def __init__(self, xKey, driveTrain):
        super().__init__()
        self.navx = navx._navx.AHRS.create_spi()
        self.startOrientation = {
            "x": self.navx.getRoll(),
            "y": self.navx.getPitch(), 
            "Z" : self.navx.getYaw()
            }
        
        self.xKey = xKey
        self.driveTrain = driveTrain

    def dobalance(self) -> None:
        x = self.navx.getRoll() - self.startOrientation["x"]
        print(f"Trying to balance:: {x}")
        if x < 2.5 and x > -2.5:
            self.stop()
        if x > 2.5:
            self.driveBackwards()
        if x < -2.5:
            self.driveForward()
             
    def execute(self) -> None:
        if self.xKey() > 0:
            self.dobalance()

    def driveForward(self) -> None:
        self.driveTrain.drive(.25, -.25)

    def driveBackwards(self) -> None:
        self.driveTrain.drive(-.25, -.25)

    def turnLeft(self) -> None:
        self.driveTrain.drive(0,-.25)

    def turnRight(self) -> None:
        self.driveTrain.drive(.25,0)

    def stop(self) -> None:
        self.driveTrain.drive(0, 0)



   

    