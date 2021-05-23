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

    def SendPhoto(self, img, msg):
        message = self.bot.sendPhoto(photo=img, caption=msg, chat_id=self.chat_id)
        return message

class FaceDetector():
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

    def Detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        return len(faces) > 0, len(faces), img

def CameraStream(cap_source): 
    LastHasFace = False

    cam_bot = HomeCamBot()
    detector = FaceDetector()
    
    cap = cv2.VideoCapture(cap_source)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret :
            cap.release()
            raise Exception("Invalid image!") 
        try :
            HasFace, NumFace, img = detector.Detect(img)
            if HasFace and not LastHasFace:
                CurrDetectionTime = time.time()
                TimeStr = datetime.datetime.now().strftime("%H:%M:%S")
                msg = "Detected %d faces in image at %s" % (NumFace, TimeStr)
                imgPath = "image/photo_%s.jpg" % TimeStr
                cv2.imwrite(imgPath, img)
                try :
                    message = cam_bot.SendPhoto(open(imgPath, 'rb'), msg)
                    print("[INFO] Detecting face, send image to Telegram with message :\n%s\n" % message)
                except Exception as e:
                    print("[ERROR] 'error when send to telegram,' ", e)

                LastHasFace = True
            else : 
                LastHasFace = False

            try : 
                if datetime.datetime.now().minute in {0, 15, 30, 45} :
                    bot.sendMessage(chat_id=chat_id, text="[INFO] heart beat msg, camera status : %r " % ret)
            except Exception as e:
                print("[ERROR] 'error when send to telegram,' ", e)

        except Exception as e:
            print("[ERROR] ", e)

if __name__ == '__main__':
    print("Face Detection service starting!")
    cap_source = os.environ['MJPEG_URL']
    CameraStream(cap_source)
