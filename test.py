import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import random
import cvzone
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(maxHands=1, detectionCon=0.8)


class SnackGame:
    def __init__(self):
        self.points = []  # all points of the snake

        self.maxFood = 5
        self.lenSnack = 3
        self.score = 0
        self.foodPoint = random.randint(150, 1000), random.randint(100, 600)
        self.playGame = True
        self.textGame = ""

    def update(self, img, lastpoints, imgFood):

        if self.playGame:
            hFood, wFood, _ = imgFood.shape

            # draw point and head
            self.points.append(lastpoints)
            head = self.points[-1]
            cv2.circle(img, head, 10, (0, 255, 0), cv2.FILLED)

            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(img, self.points[i-1],
                             self.points[i], (255, 0, 0), 10)

            # move snack
            if len(self.points) > self.lenSnack:
                self.points.pop(0)
            # draw food
            img = cvzone.overlayPNG(
                img, imgFood, (int(self.foodPoint[0] - (wFood//2)), int(self.foodPoint[1] - (hFood//2))))

        # check point to food
            px, py = self.points[-1]
            if int(self.foodPoint[0]-(wFood//2)) < px < int(self.foodPoint[0]+(wFood//2)) and int(self.foodPoint[1] - (hFood//2)) < py < int(self.foodPoint[1] + (hFood//2)):

                self.randomFoodLocation()
                self.score += 1
                self.lenSnack += 1
                if (self.score >= self.maxFood):

                    self.playGame = False
                    self.textGame = f'YOU WIN Your score is {self.score}'

            # check collosion
            distance = []
            for i, point in enumerate(self.points):
                if i > 2:
                    px, py = self.points[0]
                    cx, cy = point
                    distance.append(int(math.hypot(cx - px, cy - py)))
            if len(distance) > 2:
                if min(distance) < 15:
                    self.playGame = False
                    self.textGame = "GAME OVER:collosin"

        return img

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)


foodImg = cv2.imread("Donut.png", cv2.IMREAD_UNCHANGED)

game = SnackGame()
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=True, flipType=False)
    if game.playGame:
        cvzone.putTextRect(img, f'your score is {game.score}', (50, 50),)

    else:
        cvzone.putTextRect(
            img, game.textGame, (50, 100))

        cvzone.putTextRect(
            img, "to restart press r ", (50, 250))

    if hands:
        lmList = hands[0]["lmList"]
        pointIndex = lmList[8][0:2]

        img = game.update(img, pointIndex, foodImg)
    cv2.imshow("img", img)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
    elif key == ord("r"):
        game.points = []  # all points of the snake

        game.lenSnack = 3
        game.score = 0
        game.playGame = True
