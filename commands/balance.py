import navx
import commands2

class Balance(commands2.CommandBase):
    
    def __init__(self, xKey, driveTrain):
        print("blance init")
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
        print("Helloooooo") 
        x = self.navx.getRoll() - self.startOrientation["x"]
        if x > 2.5 and x < -2.5:
            while True:
                if x < 2.5 and x > -2.5:
                    self.stop()
                if x > 2.5:
                    self.driveBackwards()
                if x < 2.5:
                    self.driveForward()
        
    def initialize(self) -> None:
        print("initialize 12345678")
        

    def execute(self) -> None:
        print("xKey")
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


# def testPeriodic(self) -> None:   
#         x = self.navx.getRoll() - self.startOrientation["x"]
#         if x < 2.5 and x > -2.5:
#             def execute(self):
#                 # x = self.navx.getRoll() - self.startOrientation["x"]

#                 while True:
#                     if x < 2.5 and x > -2.5:
#                         self.stop()
#                     if x > 2.5:
#                         self.driveForward()
#                     if x < 2.5:
#                         self.driveBackwards()



   

    