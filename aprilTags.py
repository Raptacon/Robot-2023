from photonvision import PhotonCamera
from photonvision import PoseStrategy
from photonvision import RobotPoseEstimator
from photonvision import SimVisionSystem
from wpimath import geometry
import robotpy_apriltag
from wpilib import RobotBase

'''
The april tag class is used to get a position on the feild using photon vision
'''
class AprilTags():
    '''
    lastPose contains the previous position calculated by photon vision
    it's purpose is so the 'updatePose' function can return a position no matter what, allowing for the code to not error
    '''
    lastPose : geometry.Pose3d


    '''variables for camera simulation, which currently isnt implemented'''
    name = "Camera"
    camDaigFov = 68.06
    maxLEDRange = 9000
    cameraResWidth = 320
    cameraResHeight = 240
    minTargetArea = 0

    'camera to robot should change once the real camera is put on the robot'
    '''
    These next variables are the postion of the camera to the center of the robot
    TODO: change the variable to allign with where the camera is on the robot
    TODO: to make this more modular: these variables should probs be class parameters
    '''
    cameraPitch = 0
    cameraHeight = 0
    translation = geometry.Translation3d(0, 0, cameraHeight)
    rotation = geometry.Rotation3d(0, cameraPitch, 0)
    cameraToRobot = geometry.Transform3d(translation, rotation)





    def __init__(self, camera : PhotonCamera) -> None:
        '''
        Parameter(s): a PhotonCamera object
        sets up the pose estimator with all the information it needs, so when updatePose is called, you get a pose on the feild 
        '''
        self.camera = camera
        '''Check whether the camera is running on the robot, and sets the camera up for being on the robot or being in the sim'''
        if(RobotBase.isReal()):
            '''Creates a camera that has a position on the robot'''
            self.robotCamera = [(camera, self.cameraToRobot)]
        else:
            '''sets up a camera for the sim'''
            self.robotCamera = SimVisionSystem(self.name, self.camDaigFov, self.cameraToRobot, self.maxLEDRange, self.cameraResWidth, self.cameraResHeight, self.minTargetArea)
        
        '''atft(short for april tag feild layout) is set to a file containing the date for a years feild date'''
        '''TODO: change the file it looks to to be the correct year's file when a new year happens'''
        atfl = robotpy_apriltag.loadAprilTagLayoutField(robotpy_apriltag.AprilTagField.k2023ChargedUp)
        '''TODO: look at diffrent pose strategys and choose the best one for the year'''
        self.estimator = RobotPoseEstimator(atfl, PoseStrategy.AVERAGE_BEST_TARGETS, self.robotCamera)

        self.lastPose = geometry.Pose3d()





    def updatePose(self) -> geometry.Pose3d:
        '''
        Parameters: none
        return: a wpimath.geometry.pose3d

        uses the pose estimator to get our current position
        '''
        print(self.camera.getLatestResult().hasTargets())
        '''checks whether the camera has any april tag targets'''
        if(self.camera.getLatestResult().hasTargets()):
            '''the estimator.update() returns a tuple, the 3d pose is the first element'''
            estimatorTuple = self.estimator.update()
            retVal = estimatorTuple[0]
            '''TODO: i removed a (hopefully) unesseary if statement for the next line, double check it still works'''
            self.lastPose = retVal
    
            return(retVal)
        else:
            '''if the camera doesnt have a target, it returns the last pose it got'''
            return(self.lastPose)
        




    def distToTag(self) -> int:
        '''
        Parameters: none
        return: an int in meters of the distance to 'the best' target, set in the photon vision site
        '''
        photonTrackedTarget = self.camera.getLatestResult().getBestTarget()
        lenToTag = photonTrackedTarget.getBestCameraToTarget().X()
        return(lenToTag)
