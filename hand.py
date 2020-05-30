# organize imports
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import pyautogui
import atexit

# global variables
bg = None

#--------------------------------------------------
# To find the running average over the background
#--------------------------------------------------
def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)

#---------------------------------------------
# To segment the region of hand in the image
#---------------------------------------------
def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    (cnts,hierarchy) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)

        # find the convex hull of the segmented hand region
        chull = cv2.convexHull(segmented)

        # find the most extreme points in the convex hull
        extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
        extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
        extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
        extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

        # find the center of the palm
        cX = int((extreme_left[0] + extreme_right[0]) / 2)
        cY = int((extreme_top[1] + extreme_bottom[1]) / 2)

        #print("x: " + str(cX))
        #print("y: " + str(cY))

        centerX = 119
        centerY = 106
        centerScale = 105

        leftRight = "null"
        upDown = "null"
        frontBack = "null"

        if(cX<centerX-50):
            #print("LEFT")
            pyautogui.moveRel(-20, 0)  # 20 left
            leftRight = "left"
        if (cX > centerX + 50):
            #print("RIGHT")
            pyautogui.moveRel(20, 0)  # 20 right
            leftRight = "right"

        if (cY < centerY - 20):
            #print("UP")
            pyautogui.moveRel(0, -20)  # 20 up
            upDown = "up"
        if (cY > centerY + 50):
            #print("DOWN")
            pyautogui.moveRel(0, 20)  # 20 down
            upDown = "down"

        distance = \
        pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
        maximum_distance = distance[distance.argmax()]

        if (maximum_distance < centerScale - 10):
            #print("back")
            frontBack="back"
        if (maximum_distance > centerScale + 10):
            #print("front")
            frontBack = "front"

        #print("thing: " + str (maximum_distance))


        #writeDir = "movement"
        writeDir = "C:\\Users\\andre_am3qt87\\GoogleVRProject\\Assets\\movement"

        try:
            with open(writeDir, 'w', ) as file:
                file.write(leftRight + "\n" + upDown + "\n" + frontBack)
                file.close()

        except:
            print("bruh")



        return (thresholded, segmented)

def exit_handler():
    writeDir = "C:\\Users\\andre_am3qt87\\GoogleVRProject\\Assets\\movement"

    try:
        with open(writeDir, 'w', ) as file:
            file.write("null" + "\n" + "null" + "\n" + "null")
            file.close()

    except:
        print("bruh")

atexit.register(exit_handler)


#-----------------
# MAIN FUNCTION
#-----------------
if __name__ == "__main__":

    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break




# free up memory
camera.release()
cv2.destroyAllWindows()

