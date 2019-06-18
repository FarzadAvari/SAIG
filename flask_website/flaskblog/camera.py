from pyfacy import face_recog
from pyfacy import utils
import cv2
cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)

class Camera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        #"rtsp://nmims:NMIMS123@192.168.2.16/8000/Streaming/channels/1/preview?channel=1&subtype=0"

        
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        mdl = face_recog.Face_Recog_Algorithm()
        mdl.load_model('/Users/tejasvijay/Desktop/flask_website/model.pkl')
        
        success, image = self.video.read()
        image = cv2.resize(image, (639,480), interpolation = cv2.INTER_AREA)

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # RGB is gray

        face_locations = utils.detect_faces_locations_from_dlib(rgb)
        predictions = mdl.predict(rgb)
        #print(predictions)
        # print(len(face_locations),len(predictions))
        if predictions != 0:
            for face_location,prediction in zip(face_locations, predictions):
                top,right,bottom,left = utils.dlib_rect_to_css(face_location)
                cv2.putText(image, prediction[0], (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 1)
       #  faces = faceCascade.detectMultiScale(
       #     image,
       #     scaleFactor=1.1,
       #     minNeighbors=5,
       #     minSize=(30, 30),
       #     flags=cv2.CASCADE_SCALE_IMAGE
       #  )

       # # Draw a rectangle around the faces
       #  for (x, y, w, h) in faces:
       #      cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()