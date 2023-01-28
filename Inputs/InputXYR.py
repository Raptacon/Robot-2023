from cmath import sqrt

class XYRInput():
    """
    3 values ranging from -1 to 1
    X: Translation to the left and right (right being positive)
    Y: Translation forwards and backwards (forward being positive)
    R: Rotation along the horizontal (counterclockwise is positive)
    """

    def __init__(self, x, y, r):
        self.X = x
        self.Y = y
        self.R = r

    def getMagnitudeTranslation(self):
        magnitude = sqrt(self.X **2 , self.Y **2)
        return magnitude

    def setX(self, X):
        self.X = X

    def setY(self, Y):
        self.Y = Y

    def setR(self, R):
        self.R = R

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getR(self):
        return self.R