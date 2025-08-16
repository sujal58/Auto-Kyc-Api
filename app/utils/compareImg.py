import cv2
import tempfile
from deepface import DeepFace;
import os;


def compareImg(first_img, second_img):
    try:
        # Load the second image
        img = cv2.imread(second_img)


         # Load OpenCV's built-in face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)

        if len(faces) == 0:
            raise ValueError("No face detected in the second image.")

        # Extract the first  face detected
        x, y, w, h = faces[0]
        face_crop = gray[y:y+h, x:x+w] 

        # Convert grayscale face to BGR 
        face_bgr = cv2.cvtColor(face_crop, cv2.COLOR_GRAY2BGR)


        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            temp_filename = tmp.name
            cv2.imwrite(temp_filename, face_bgr)

        print("Temp file exists?: ", os.path.exists(temp_filename))
        # cv2.imshow("temp file", cv2.imread(temp_filename))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        try:
            # Perform face comparison using processor mtcnn or 'retinaface'
            result = DeepFace.verify(img1_path=first_img, img2_path=temp_filename, detector_backend='mtcnn',  
            enforce_detection=False)
            print((result["distance"]/0.68))
            return result
        finally:
          
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                print(f"Temporary file deleted: {temp_filename}")
            
    except Exception as e:
        print(f"Error in compareImg: {str(e)}")
        raise ValueError(f"Face comparison failed: {str(e)}")
