import navx
import commands2
from subsystems.drivetrains.westcoast import Westcoast as DriveTrain

class Balance(commands2.CommandBase):

    
    # def init is being called
    def __init__(self, xKey : bool, driveTrain : DriveTrain):
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
        y = self.navx.getPitch() - self.startOrientation["y"]
        print(f"Trying to balance:: {y}")
        if y < 2.5 and y > -2.5:
          
            return 0
        if y > 2.5:
          
            return -.35
        if y < -2.5:
          
            return .35
 
    def execute(self) -> None:
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
