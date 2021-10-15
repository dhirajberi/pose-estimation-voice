import cv2
import time
# from pose_estimation_class import PoseDetector
import mediapipe as mp
import argparse
import pyttsx3
import threading
import time
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
pTime = 0

class PoseDetector:

    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):
        print("inside init..............")
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)
        print("inside init..............")
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        return lmList
        
# global bodycount
def body():
    try:
        engine.say("Body is not visible properly!")
        engine.runAndWait() 
    except:
        pass
        

def feet():
    try:
        engine.say("Please maintain some distance between your feets")
        engine.runAndWait() 
    except:
        pass

def leftup():
    try:
        engine.say("Please up your left hand")
        engine.runAndWait() 
    except Exception as e:
        pass


def leftdown():
    try:
        engine.say("Please little bit down your left hand")
        engine.runAndWait()
    except:
        pass

def rightup():
    try:
        engine.say("Please up your right hand")
        engine.runAndWait() 
    except:

        pass


def rightdown():
    try:
        engine.say("Please little bit down your right hand")
        engine.runAndWait() 
    except:
        pass

def perfect():
    try:
        engine.say("Perfect posture")
        engine.runAndWait() 
    except Exception as e:
        pass
        
    
    

cap = cv2.VideoCapture(0)


detector = PoseDetector()

while(cap.isOpened()):
    success, img = cap.read()
    
    if success == False:
        break
    
    img, p_landmarks, p_connections = detector.findPose(img, False)
    
    # draw points
    mp.solutions.drawing_utils.draw_landmarks(img, p_landmarks, p_connections)
    lmList = detector.getPosition(img)
    
    try:
        if lmList[0][2] > 10 and lmList[31][2] < 500:# full body condition
            if lmList[31][1]- lmList[32][1] > 100: #feet condition
                
                # For left hand
                if lmList[23] and lmList[15]:
                    if lmList[15][1]-lmList[23][1] < 100:
                        
                        lu = threading.Thread(target=leftup)
                        lu.start()
                        cv2.putText(img, str("Please up your left hand!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                    if lmList[15][1]-lmList[23][1] > 130:
                        ld = threading.Thread(target=leftdown)
                        ld.start()
                        cv2.putText(img, str("Please little bit down your left hand!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                    if lmList[15][1]-lmList[23][1] > 100 and lmList[15][1]-lmList[23][1] < 150:
                        
                        # For Right Hand
                        if lmList[24][1]-lmList[16][1] < 100:
                            ru = threading.Thread(target=rightup)
                            ru.start()
                            cv2.putText(img, str("Please up your right hand!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                        if lmList[24][1]-lmList[16][1] > 130:
                            rd = threading.Thread(target=rightdown)
                            rd.start()
                            cv2.putText(img, str("Please little bit down your right hand!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                        if lmList[24][1]-lmList[16][1] > 100 and lmList[24][1]-lmList[16][1] < 150:
                            p1 = threading.Thread(target=perfect)
                            p1.start()
                            cv2.putText(img, str("Perfect Right and Left hand!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            else:
                f = threading.Thread(target=feet)
                f.start()
                cv2.putText(img, str("Please maintain some distance between your feets!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
                           
        else:
            
            b = threading.Thread(target=body)
            b.start()
            cv2.putText(img, str("Body is not visible properly!"), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            
    except Exception as e:
        pass

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()