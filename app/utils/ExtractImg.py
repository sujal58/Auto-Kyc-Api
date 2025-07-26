import cv2
import tempfile
from deepface import DeepFace;
import os
import numpy as np

def extract_face(document_path):
    try:
        # we will load image here
        doc_img = cv2.imread(document_path)
        if doc_img is None:
            print("Error: Cannot read image.")
            return None

        # image will be converted to grayscale for face detection
        gray = cv2.cvtColor(doc_img, cv2.COLOR_BGR2GRAY)

        # Face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            print("No face found.")
            return None

        # Get the largest face
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        face_crop = doc_img[y:y+h, x:x+w]

        # Resize slightly larger (helps DeepFace)
        face_resized = cv2.resize(face_crop, (224, 224), interpolation=cv2.INTER_CUBIC)

        # Light sharpening filter
        kernel = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])
        sharpened = cv2.filter2D(face_resized, -1, kernel)

        # Gentle brightness/contrast tweak
        enhanced = cv2.convertScaleAbs(sharpened, alpha=1.1, beta=10)  # slightly brighter and higher contrast


        # Show the face image
        # cv2.imshow("Extracted Face", enhanced)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Save cleaned face
        base_filename = os.path.basename(document_path).split(".")[0]
        base_path = "D:/python/Auto-Kyc-Api/extractedImg"
        if not os.path.exists(base_path):
            os.mkdir(base_path)

        
        save_path = os.path.join(base_path, f"soft_enhanced_{base_filename}.jpg")
        cv2.imwrite(save_path, enhanced)

        print(f"Saved enhanced face at: {save_path}")
        return save_path
    
    except Exception as e:
        print(f"Error in Extracting img: {str(e)}")
        raise ValueError(f"Image extraction failed: {str(e)}")




