from PIL import Image
import pytesseract
import numpy as np

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def textExtract(documentPath, user_info):
    # Load the citizenship document image
    img = Image.open(documentPath)
    text = pytesseract.image_to_string(img, lang="eng").lower()

    # remove extra spaces/newlines
    text = ' '.join(text.split())  

    print(text)

    # Check conditions
    checks = {
        "name_match": user_info["name"].lower() in text,
        "document_number_match": user_info["document_number"].lower() in text
    }

    print(checks)

    # Print results
    for key, result in checks.items():
        print(f"{key}: {'✅ Match' if result else '❌ Not Found'}")

    # Final decision
    if all(checks.values()):
        print("\nCitizenship document VERIFIED.✅ ")
        return 1
    else:
        print("\nCitizenship document could NOT be verified.❌")
        return 0




