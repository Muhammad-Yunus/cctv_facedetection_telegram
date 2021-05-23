import telegram
import datetime
import time 
import cv2
import os

class HomeCamBot():
    def __init__(self):
        self.botToken = os.environ['BOT_TOKEN']
        self.chat_id = os.environ['CHAT_ID']
        self.bot = telegram.Bot(token=self.botToken)
        self.HeartBeatSent = False

    def SendPhoto(self, img, msg):
        message = self.bot.sendPhoto(photo=img, caption=msg, chat_id=self.chat_id)
        return message

    def SendMessage(self, message):
        self.bot.sendMessage(chat_id=self.chat_id, text=message)
        self.HeartBeatSent = True

class FaceDetector():
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

    def Detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        return len(faces) > 0, len(faces), img

class CameraStream():
    def __init__(self, cap_source):
        self.cap_source = cap_source
        self.cap = cv2.VideoCapture(self.cap_source)
        self.cam_bot = HomeCamBot()
        self.detector = FaceDetector()
        self.lastFaceSent = 0

    def run(self): 
        while self.cap.isOpened():
            ret, img = self.cap.read()
            if not ret :
                self.cap.release()
                print("[INFO] Invalid image!") 

                print("[INFO] Initialize new camera!") 
                self.cap = None
                self.cap = cv2.VideoCapture(self.cap_source)
                continue
            try :
                HasFace, NumFace, img = self.detector.Detect(img)
                if HasFace and (time.time() - self.lastFaceSent) > 5:
                    self.lastFaceSent = time.time()
                    TimeStr = datetime.datetime.now().strftime("%H:%M:%S")
                    msg = "Detected %d faces in image at %s" % (NumFace, TimeStr)
                    imgPath = "image/photo_%s.jpg" % TimeStr
                    cv2.imwrite(imgPath, img)
                    try :
                        message = self.cam_bot.SendPhoto(open(imgPath, 'rb'), msg)
                        print("[INFO] Detecting face, send image to Telegram with message :\n%s\n" % message)
                    except Exception as e:
                        print("[ERROR] 'error when send to telegram,' ", e)

                try : 
                    CurrTime = datetime.datetime.now()
                    if CurrTime.minute in {0, 15, 30, 45} : 
                        if not self.cam_bot.HeartBeatSent:
                            self.cam_bot.SendMessage("[INFO] heart beat msg, camera status : %r " % ret)
                    else :
                        self.cam_bot.HeartBeatSent = False
                except Exception as e:
                    print("[ERROR] 'error when send to telegram,' ", e)

            except Exception as e:
                print("[ERROR] ", e)

if __name__ == '__main__':
    print("Face Detection service starting!")
    cap_source = os.environ['MJPEG_URL']
    stream = CameraStream(cap_source)
    stream.run()