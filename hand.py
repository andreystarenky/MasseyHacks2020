import cv2
import imutils
from sklearn.metrics import pairwise
import pyautogui
import atexit

bg = None

def run_avg(image, aWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image, bg, aWeight)
def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    (cnts,hierarchy) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        chull = cv2.convexHull(segmented)

        extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
        extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
        extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
        extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

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
        writeDir = "Assets\\movement"

        try:
            with open(writeDir, 'w', ) as file:
                file.write(leftRight + "\n" + upDown + "\n" + frontBack)
                file.close()

        except:
            print("bruh")



        return (thresholded, segmented)

def exit_handler():
    writeDir = "Assets\\movement"

    try:
        with open(writeDir, 'w', ) as file:
            file.write("null" + "\n" + "null" + "\n" + "null")
            file.close()

    except:
        print("bruh")

atexit.register(exit_handler)


if __name__ == "__main__":

    aWeight = 0.5

    camera = cv2.VideoCapture(0)

    top, right, bottom, left = 10, 350, 225, 590

    num_frames = 0

    while(True):
        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            hand = segment(gray)

            if hand is not None:
                (thresholded, segmented) = hand

                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        num_frames += 1

        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF

        if keypress == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()

