import  cv2
# WebCam
import cvzone
# Hand Detectior package
from cvzone.HandTrackingModule import HandDetector
import time # For timeing
import random # For Choose Random Answer

# it's use to set for two frame
cap= cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# Detected the hand
detector = HandDetector(maxHands=2)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] # First one for AI and, Second one for Player

while True:
    imgBG =cv2.imread('Resources/BG.png')
    success, img = cap.read()


    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled, draw=True, flipType=True)

    if startGame:
        if stateResult is False:

            # Set Position, Color, During the time
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            # Count the time
            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # User Choose Rock
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    # User Choose Paper
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    # User Choose Scissors
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    # It's AI Code for take any random shape in game
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f"Resources/{randomNumber}.png",cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI,(149,310))

                    # Player Wins [ 1st->(Rock,Scissor) 2nd->(Paper,Rock) 3rd->(Scissors,Paper) ]
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins [ 1st->(Scissor,Rock) 2nd->(Rock,Paper) 3rd->(Paper,Scissors) ]
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    print(playerMove)

    # Frame OverLap Background in WebCam
    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # That is use to Calculate Score AI and User
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("image",img) --> Use just for Testing both of them
    # cv2.imshow("Scaled",imgScaled) --^
    cv2.imshow("BG",imgBG)

    key = cv2.waitKey(1)

    # Use for start the game using 's' key
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult =False