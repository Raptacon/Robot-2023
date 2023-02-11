import navx
import commands2

class Balance:
    
    def __init__(self):
        self.navx = navx._navx.AHRS.create_spi()
        self.startOrientation = {
            "x": self.navx.getRoll(),
            "y": self.navx.getPitch(), 
            "Z" : self.navx.getYaw()
            }
        
    def execute(self):
        x = self.navx.getRoll() - self.startOrientation["x"]
        if x < 2.5 and x > -2.5:
            pass
        elif x > 2.5:
            # move bot forward
        else:
            # move bot backward



   

    