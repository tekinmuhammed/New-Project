import cv2 as cv
import mediapipe as mp
import pyautogui as pg


#camera
cam = cv.VideoCapture(0)
mphand = mp.solutions.hands
hands = mphand.Hands()

clk = 1

#virtual keyboard layout
key = [['q','w','e','r','t','y','u','i','o','p'],
       ['a','s','d','f','g','h','j','k','l',':'],
       ['z','x','c','v','b','n','m',',','.','?']]
size = 100/100
buttonList = []
for i in range(len(key)):
    for j, keyy in enumerate(key[i]):
        x = int((j*60 *size)+25)
        y = int((i*60 *size)+25)
        h = int(x+ 50*size)
        w = int(y + 50*size)
        buttonList.append([x,y,h,w,keyy])

def S_key():
    xs = lambda i: int((i*60 *size)+25)
    ys = lambda y: int((y*60 *size)+60)
    hws = lambda hw: int(hw + 50*size)
    buttonList.append([xs(0), ys(len(key)), hws(xs(3)), hws(ys(len(key))), "delete"])
    buttonList.append([xs(4), ys(len(key)), hws(xs(6)), hws(ys(len(key))), "capslock"])
    buttonList.append([xs(7), ys(len(key)), hws(xs(9)), hws(ys(len(key))), "enter"])
    buttonList.append([xs(1), ys(len(key)+1), hws(xs(8)), hws(ys(len(key)+1)), "."])
S_key()

def drawKey(img, buttonList):
    for x, y, h, w, keyy in buttonList:
        cv.rectangle(img, (x, y), (h, w), (0, 255, 255), 2)
        cv.putText(img, keyy, (x+12, y+29), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

while True:
    succses, img = cam.read()
    img = cv.flip(img, 1)
    h, w, c = img.shape
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    if (result.multi_hand_landmarks):
        lmlist = []
        for handsLms in result.multi_hand_landmarks:
            for id, landmark in enumerate(handsLms.landmark):
                x, y = int(landmark.x * w ), int(landmark.y * h )
                lmlist.append([id, x, y])
 # koordinates of the tip of the middle finger (landmark 12)
        X = lmlist[12][1]
        Y = lmlist[12][2]
        cv.circle(img, (X, Y), 9, (255, 0, 255), cv.FILLED)


        """Click"""
        if lmlist[8][2] > lmlist[7][2] and clk >0:
            cv.circle(img, (X, Y), 9, (0, 0, 255), cv.FILLED)
            for x, y, h, w, keyy in buttonList:
                if x < lmlist[12][1] < h and y < lmlist[12][2] < w:
                    pg.press(key)
            clk = -1
        
        elif lmlist[8][2] < lmlist[7][2]:
            clk = 1

    drawKey(img, buttonList)
    cv.imshow("Virtual Keyboard", img)
    if cv.waitKey(20) &  0xFF == ord("d"):
        break


# release camera and close windows
cv.destroyAllWindows()