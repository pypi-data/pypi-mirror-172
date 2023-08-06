try:
    import cv2
    import mediapipe
    import numpy
except ImportError as i:
    print(f'Error! {i}')


class HandDetector:
    def __init__(
            self,
            cam_index: int = 0,
            win_width: int = 640,
            win_height: int = 360,
            cam_fps: int = 30,
            static_mode: bool = False,
            max_hands: int = 2,
            model_complex: int = 1,
            min_detection_con: float = 0.5,
            min_tracking_con: float = 0.5
    ):
        self.cam_index = cam_index
        self.win_width = win_width
        self.win_height = win_height
        self.cam_fps = cam_fps
        self.static_mode = static_mode
        self.max_hands = max_hands
        self.model_complex = model_complex
        self.min_detection_con = min_detection_con
        self.min_tracking_con = min_tracking_con

        self.mpHands = mediapipe.solutions.hands
        self.mpDraws = mediapipe.solutions.drawing_utils
        self.mpStyle = mediapipe.solutions.drawing_styles
        self.hands = self.mpHands.Hands(
            self.static_mode,
            self.max_hands,
            self.model_complex,
            self.min_detection_con,
            self.min_tracking_con
        )
        self.fingerTipIDs = [4, 8, 12, 16, 20]

    def init_cam(self) -> numpy.ndarray:
        """
        Initiate your Webcam to grab computer vision.
        :return: Grabbed image as numpy ndarray.
        """
        cam = cv2.VideoCapture(self.cam_index, 700)
        cam.set(3, self.win_width)
        cam.set(4, self.win_height)
        cam.set(5, self.cam_fps)
        cam.set(6, cv2.VideoWriter_fourcc(*'MJPG'))

        return cam

    def findHand(self, image: numpy.ndarray, draw_detect: bool = True, hand_connect: bool = True) -> numpy.ndarray:
        """
        Finds your hand and draws some detection over your hands.
        :param image: Grabbed image from your webcam.
        :param draw_detect: Bool value to draw the detection or not.
        :param hand_connect: Bool value to draw the hand connection or not.
        :return: Image as numpy ndarray.
        """
        imageRgb = cv2.cvtColor(image, 4)
        self.results = self.hands.process(imageRgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw_detect:
                    if hand_connect: self.mpDraws.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS,
                                                                 connection_drawing_spec=self.mpDraws.DrawingSpec((51, 255, 102)))
                    else: self.mpDraws.draw_landmarks(image, handLms)

        return image

    def findLocations(self, image: numpy.ndarray, hand_no: int = 0, draw_detect: bool = True, draw_id: int | str = 'ALL') -> tuple:
        """
        Get the location of your hand.
        :param image: Grabbed image from your webcam as numpy ndarray.
        :param hand_no: Number of hand.
        :param draw_detect: Bool value to draw the detection or not.
        :param draw_id: The hand lm to be drawn.
        :return: List of hand landmark locations.
        """
        xList, yList, lmList = [], [], []
        bbox = ()
        self.win_height, self.win_width, c = image.shape

        if self.results.multi_hand_landmarks:
            try: myHand = self.results.multi_hand_landmarks[hand_no]
            except: myHand = self.results.multi_hand_landmarks[hand_no - 1]

            for id, handLm in enumerate(myHand.landmark):
                cx, cy, cz = int(self.win_width * handLm.x), int(self.win_height * handLm.y), round(handLm.z, 2)
                xList.append(cx)
                yList.append(cy)
                lmList.append((id, cx, cy, cz))

                if draw_detect:
                    if draw_id == 'ALL':
                        cv2.circle(image, (cx, cy), 13, (255, 255, 0), 2)
                    else:
                        if id == draw_id:
                            cv2.circle(image, (cx, cy), 13, (255, 255, 0), 2)

            bbox = min(xList), min(yList), max(xList), max(yList)

        return lmList, bbox

    def fingerUp(self, landmark: list) -> list:
        """
        Determines the fingers are up or down.
        :param landmark: 21 hand landmark list.
        :return: List of the fingers.
        """
        fingers = [0, 0, 0, 0, 0]

        if landmark[self.fingerTipIDs[0]][1] > landmark[self.fingerTipIDs[0] - 1][1]:
            fingers.pop(0)
            fingers.insert(0, 1)
        else:
            fingers.pop(0)
            fingers.insert(0, 0)

        for id in range(1, 5):
            if landmark[self.fingerTipIDs[id]][2] < landmark[self.fingerTipIDs[id] - 1][2]:
                fingers.pop(id)
                fingers.insert(id, 1)
            else:
                fingers.pop(id)
                fingers.insert(id, 0)

        return fingers


def main():
    import time

    timeS = time.time()

    class_obj = HandDetector()
    cam = class_obj.init_cam()

    while cam.isOpened():
        success, image = cam.read()
        if not success: continue

        detected_hand = class_obj.findHand(image, draw_detect=True)
        hand_landmark = class_obj.findLocations(image, draw_id=8)

        if hand_landmark[0] and hand_landmark[1]:
            # print(hand_landmark[0][8])

            finger_ups = class_obj.fingerUp(hand_landmark[0])
            # print(finger_ups)

            boundry = hand_landmark[1]
            cv2.rectangle(image, (boundry[0], boundry[1]), (boundry[2], boundry[3]), (0, 255, 255), 2)

        timeE = time.time()
        fps = int(1 / (timeE - timeS))
        timeS = timeE
        cv2.putText(image, str(f'FPS : {fps}'), (10, 30), 4, 1, (0, 255, 255), 3)
        cv2.imshow('Hand Detection - Chanchal Roy', image)
        if cv2.waitKey(1) & 0xff == ord('q'): break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
