import cv2
import mediapipe as mp
import pyautogui as pg

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
widthFrame = 640
heightFrame = 480
screen_width, screen_height = pg.size()
indexFinger_x, indexFinger_y = 0, 0
thumb_x, thumb_y = 0, 0
lastFinger_x, lastFinger_y = 0, 0
mFinger_y = 0
pg.FAILSAFE = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (widthFrame, heightFrame))
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    outputHand = hand_detector.process(rgb_frame)
    hands = outputHand.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(img, hand)
            allLandmarks = hand.landmark

            for index, landmark in enumerate(allLandmarks):
                x = int(landmark.x * widthFrame)
                y = int(landmark.y * heightFrame)

                # Index Finger Landmark
                if index == 8:
                    cv2.circle(img=img, center=(x, y), color=(153, 0, 153), radius=15, thickness=3)
                    indexFinger_x = (screen_width / widthFrame) * x
                    indexFinger_y = (screen_height / heightFrame) * y
                    pg.moveTo(indexFinger_x, indexFinger_y)

                # Thumb landmark
                if index == 4:
                    cv2.circle(img=img, center=(x, y), color=(153, 0, 153), radius=15, thickness=3)
                    thumb_x = (screen_width / widthFrame) * x
                    thumb_y = (screen_height / heightFrame) * y

                    if abs(indexFinger_y - thumb_y) < 35:
                        print('click')
                        pg.click()
                        pg.sleep(1)

                # lastFinger Landmark
                if index == 20:
                    cv2.circle(img=img, center=(x, y), color=(113, 0, 123), radius=15, thickness=3)
                    lastFinger_y = (screen_height / heightFrame) * y

                    if abs(thumb_y - lastFinger_y) < 35:
                        print('right click')
                        pg.rightClick()
                        pg.sleep(1)

                # MiddleFinger landmark
                # if index == 12:
                #     cv2.circle(img=img, center=(x, y), color=(113, 0, 123), radius=15, thickness=3)
                #     mFinger_y = (screen_height / heightFrame) * y
                #
                #     if abs(thumb_y - mFinger_y) < 35:
                #         print('double click')
                #         pg.doubleClick()
                #         pg.sleep(1)

    cv2.imshow('Virtual Mouse', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
