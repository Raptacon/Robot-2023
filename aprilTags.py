from photonvision import PhotonCamera
from photonvision import PoseStrategy
from photonvision import RobotPoseEstimator
from photonvision import SimVisionSystem
from wpimath import geometry
import robotpy_apriltag
import ntcore


class AprilTags():
    lastPose : geometry.Pose3d
    def __init__(self) -> None:
        
        '''variables for camera simulation'''
        name = "Camera"
        camDaigFov = 68.06

        'camera to robot should change once the real camera is put on the robot'
        cameraPitch = 0
        cameraHeight = 0
        translation = geometry.Translation3d(0, 0, cameraHeight)
        rotation = geometry.Rotation3d(0, cameraPitch, 0)
        self.cameraToRobot = geometry.Transform3d(translation, rotation)

        maxLEDRange = 9000
        cameraResWidth = 320
        cameraResHeight = 240
        minTargetArea = 0

        '''Check whether the camera is running on the robot, and sets the camera up for beign on the robot or being in the sim'''
        '''TODO: change the if statemnt below to detect whether the sim is running, if it is run sim vision system'''
        if(True):
            '''sets up network tables'''
            nt = ntcore.NetworkTableInstance.getDefault()
            nt.startClient3("test code")
            nt.setServer("10.32.0.13")
            '''lets people know whether it was connected'''
            while not nt.isConnected():
                print("Network tables Connecting   ", end='\r')
                print("Network tables Connecting.  ", end='\r')
                print("Network tables Connecting.. ", end='\r')
                print("Network tables Connecting...", end='\r')
            if nt.isConnected():
                print('Network tables Connected')

            '''connects a camera object to the network tables'''
            self.camera = PhotonCamera(nt, name)
            '''Creates a camera that has a position on the robot'''
            self.robotCamera = [(self.camera, self.cameraToRobot)]
        else:
            '''sets up a camera for the sim'''
            self.camera = SimVisionSystem(name, camDaigFov, self.cameraToRobot, maxLEDRange, cameraResWidth, cameraResHeight, minTargetArea)
        
        '''grabs this year's feild data'''
        'atfl means AprilTagFieldLayout'
        atfl = robotpy_apriltag.loadAprilTagLayoutField(robotpy_apriltag.AprilTagField.k2023ChargedUp)
        '''the closest to last pose can be, and probaly should be changed/evaluated, as closest to last pose is just what my example uses'''
        self.estimator = RobotPoseEstimator(atfl, PoseStrategy.AVERAGE_BEST_TARGETS, self.robotCamera)


    def updatePose(self) -> geometry.Pose3d:
        '''
        Gets the position of the robot based off of Apriltag vision systems
        Parameters: None
        Return: a 3d pose of the robot in the field
        '''
        '''the estimator update function returns a tuple, or basically an array, with the pose and a variable that doesnt seem to be anything'''
        if(self.camera.getLatestResult().hasTargets()):
            estimatorTuple = self.estimator.update()
            retVal = estimatorTuple[0]
            self.lastPose = retVal
            return(retVal)
        else:
            return(self.lastPose)
