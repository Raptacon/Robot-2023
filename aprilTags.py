from photonvision import PhotonCamera
from photonvision import PoseStrategy
from photonvision import RobotPoseEstimator
from photonvision import SimVisionSystem
from wpimath import geometry
import robotpy_apriltag
import ntcore


class AprilTags():
    def __init__(self) -> None:
        
        '''variables for camera simulation'''
        name = "Camera"
        camDaigFov = 68.06

        'camera to robot should change once the real camera is put on the robot'
        cameraPitch = 0
        cameraHeight = 0
        translation = geometry.Translation3d(0, 0, cameraHeight)
        rotation = geometry.Rotation3d(0, cameraPitch, 0)
        cameraToRobot = geometry.Transform3d(translation, rotation)

        maxLEDRange = 9000
        cameraResWidth = 320
        cameraResHeight = 240
        minTargetArea = 0


        '''TODO: change the if statemnt below to detect whether the sim is running, if it is run sim vision system'''
        if(True):
            nt = ntcore.NetworkTableInstance.getDefault()
            nt.startClient3("test code")
            nt.setServer("10.32.0.2")
            while not nt.isConnected():
                print("Connecting")
            self.camera = PhotonCamera(name)
            if nt.isConnected():
                print('Connected')
        else:
             self.camera = SimVisionSystem(name, camDaigFov, cameraToRobot, maxLEDRange, cameraResWidth, cameraResHeight, minTargetArea)
        
        '''grabs this year's feild data'''
        'atfl means AprilTagFieldLayout'
        #.AprilTagFieldrobotpy_apriltag.AprilTagField.k2023ChargedUp
        #atfl = robotpy_apriltag._apriltag.AprilTagFieldLayout(robotpy_apriltag.AprilTagField.k2023ChargedUp.loadAprilTagLayoutField())
        atfl = robotpy_apriltag.loadAprilTagLayoutField(robotpy_apriltag.AprilTagField.k2023ChargedUp)
        '''the closest to last pose can be, and probaly should be changed/evaluated, as closest to last pose is just what my example uses'''
        self.estimator = RobotPoseEstimator(atfl, PoseStrategy.CLOSEST_TO_LAST_POSE, self.camera)

    def updatePose(self) -> geometry.Pose3d:
        '''returns a pose 3d with the pose of the robot'''
        estimatorTuple = self.estimator.update()
        return(estimatorTuple)
    
'test code'
test = AprilTags()
test2 = test.updatePose()
test3 = test2[0]
print(test3.X())