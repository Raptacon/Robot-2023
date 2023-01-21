import cv2
import pupil_apriltags


LINE_LENGTH = 5
CENTER_COLOR = (0, 255, 0)
CORNER_COLOR = (255, 0, 255)

### Some utility functions to simplify drawing on the camera feed
# draw a crosshair
def plotPoint(image, center, color):
    center = (int(center[0]), int(center[1]))
    image = cv2.line(image,
                     (center[0] - LINE_LENGTH, center[1]),
                     (center[0] + LINE_LENGTH, center[1]),
                     color,
                     3)
    image = cv2.line(image,
                     (center[0], center[1] - LINE_LENGTH),
                     (center[0], center[1] + LINE_LENGTH),
                     color,
                     3)
    return image

# plot a little text
def plotText(image, center, color, text):
    center = (int(center[0]) + 4, int(center[1]) - 4)
    return cv2.putText(image, str(text), center, cv2.FONT_HERSHEY_SIMPLEX,
                       1, color, 3)

# setup and the main loop
detector = pupil_apriltags.Detector()
cam = cv2.VideoCapture(0)

looping = True

while looping:
    result, image = cam.read()
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# look for tags
    detections = detector.detect(grayimg)
    if not detections:
        print("Nothing")
    else:
	    # found some tags, report them and update the camera image
        for detect in detections:
            print("tag_id: %s, center: %s" % (detect.tag_id, detect.center))
            image = plotPoint(image, detect.center, CENTER_COLOR)
            image = plotText(image, detect.center, CENTER_COLOR, detect.tag_id)
            for corner in detect.corners:
                image = plotPoint(image, corner, CORNER_COLOR)
	# refresh the camera image
    cv2.imshow('Result', image)
	# let the system event loop do its thing
    key = cv2.waitKey(100)
	# terminate the loop if the 'Return' key his hit
    if key == 13:
        looping = False

# loop over; clean up and dump the last updated frame for convenience of debugging
cv2.destroyAllWindows()
cv2.imwrite("final.png", image)