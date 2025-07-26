from fastapi import HTTPException
import os
from PIL import Image
import pytesseract

from app.utils.ExtractImg import extract_face
from app.utils.compareImg import compareImg
from app.utils.textExtract import textExtract
from app.model.KycResponse import KycVerificationResponse

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def textExtract_no_input(documentPath, user_info):
    img = Image.open(documentPath)
    text = pytesseract.image_to_string(img, lang="eng").lower()
    text = ' '.join(text.split())
    print(text)

    checks = {
        "name_match": user_info["name"].lower() in text,
        "document_number_match": user_info["document_number"].lower() in text
    }

    print(checks)

    for key, result in checks.items():
        print(f"{key}: {'✅ Match' if result else '❌ Not Found'}")

    if all(checks.values()):
        print("\n✅ Citizenship document VERIFIED.")
        return 1
    else:
        print("\n❌ Citizenship document could NOT be verified.")
        return 0

def perform_kyc_verification(document_front_path: str, document_back_path: str, user_image_path: str, user_info: dict):
    print("user image path: ", user_image_path)
    print("user front path: ", document_front_path)
    print("user back path: ", document_back_path)


    # Validate file paths exist
    for path in [document_front_path, document_back_path, user_image_path]:
        if not os.path.exists(path):
            raise HTTPException(status_code=400, detail=f"File not found: {path}")

    # Extract face from document front
    face_path = extract_face(document_front_path)
    if face_path is None:
        raise HTTPException(status_code=400, detail="No face found in document front.")

    # Compare faces
    image_status = compareImg(face_path, user_image_path)
    print(image_status)

    # Verify document text
    document_text_status = textExtract(document_back_path, user_info)

    #calculate confidence score
    confidence = calculate_confidence(image_status["distance"])

    # Final verification
    verified = image_status["verified"] and document_text_status == 1

    return KycVerificationResponse(
        status="success" if verified else "failed",
        code=200 if verified else 400,
        message="KYC verified ✅" if verified else "KYC verification failed ❌",
        kyc_score=image_status["distance"],
        confidence=confidence
    )

    # if image_status["verified"] and document_text_status == 1:
    #     return {"status": "✅ Kyc verified ✅"}
    # else:
    #     return {"status": "Fake document detected"}
    

def calculate_confidence(distance: float, threshold = 0.68) -> float:
    return round(max(0.0, min(1.0, (threshold - distance) / threshold)) * 100, 2)