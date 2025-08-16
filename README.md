# Auto-Kyc-Api

Auto-Kyc-Api is a Python-based API for automating Know Your Customer (KYC) verification. It leverages advanced image processing, face comparison, and optical character recognition (OCR) to validate the identity and documents of users in a seamless workflow.

## Features

- **Automated Face Extraction and Comparison**: Detects and extracts faces from user-uploaded documents and compares them to a selfie image for biometric verification.
- **Document Text Extraction and Validation**: Uses OCR to extract and verify user information (name, document number) from citizenship documents.
- **Confidence Scoring**: Returns a verification score and confidence metric.
- **REST API**: Powered by FastAPI for efficient and scalable endpoints.

## Workflow Overview

1. **User submits KYC data**: Front and back images of the document, a selfie, and personal info.
2. **Face extraction**: The system detects and extracts the face from the document using OpenCV and Haar cascades.
3. **Face comparison**: The extracted face is compared with the user's selfie using DeepFace for robust biometric verification.
4. **Text extraction**: The back of the document is processed using Tesseract OCR to extract text and validate user information.
5. **Scoring**: The results are processed, and a verification score is generated and returned.

## Tools & Libraries Used

### 1. FastAPI
- **Purpose**: The core web API framework.
- **Usage**: All API endpoints (see `app/main.py` and `app/api/v1/routes.py`).
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### 2. OpenCV (`cv2`)
- **Purpose**: Image loading, preprocessing, and face detection.
- **Usage**: Extracts faces from documents and selfie images (`app/utils/ExtractImg.py`, `app/utils/compareImg.py`).
- **Details**:
  - Uses Haar cascades for face detection.
  - Applies filters for image enhancement.

### 3. DeepFace
- **Purpose**: Deep learning-based face verification.
- **Usage**: Compares the extracted document face to the user's selfie (`app/utils/compareImg.py`).
- [DeepFace GitHub](https://github.com/serengil/deepface)

### 4. Pillow (`PIL`)
- **Purpose**: Image file handling.
- **Usage**: Opens images for OCR (`app/utils/textExtract.py`, `app/services/Kyc_service.py`).

### 5. pytesseract
- **Purpose**: OCR to extract text from documents.
- **Usage**: Reads and parses user details from the document (`app/services/Kyc_service.py`, `app/utils/textExtract.py`).
- **Details**:
  - Requires Tesseract installed and path configured.
  - Extracts and cleans text for validation.

### 6. Pydantic
- **Purpose**: Data validation and serialization.
- **Usage**: Models API requests and responses (`app/model/kyc_model.py`, `app/model/KycResponse.py`).

### 7. NumPy
- **Purpose**: Numeric operations for image processing.
- **Usage**: Manipulates image arrays for filtering and enhancement.

## API Endpoints

- `POST /api/v1/kyc-verify`
  - Accepts images and user info.
  - Returns verification status, score, and confidence.

## Example Request

```json
POST /api/v1/kyc-verify
{
  "document_front_path": "path/to/front.jpg",
  "document_back_path": "path/to/back.jpg",
  "user_image_path": "path/to/selfie.jpg",
  "name": "John Doe",
  "document_number": "123456789"
}
```

## Directory Structure

```
app/
  ├── api/v1/routes.py          # API route definitions
  ├── main.py                   # API application entry point
  ├── model/
  │   ├── kyc_model.py          # Request models
  │   └── KycResponse.py        # Response models
  ├── services/
  │   └── Kyc_service.py        # KYC service logic
  └── utils/
      ├── ExtractImg.py         # Face extraction logic
      ├── compareImg.py         # Face comparison logic
      └── textExtract.py        # OCR and text validation
```

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn opencv-python deepface pillow pytesseract numpy
   ```
2. **Install Tesseract OCR**:
   - Download from [here](https://github.com/tesseract-ocr/tesseract).
   - Set the path in code (see `pytesseract.pytesseract.tesseract_cmd`).

3. **Run the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Notes

- **Temporary files**: Face crops and enhanced images are temporarily saved and deleted for processing.
- **Error handling**: Detailed exceptions are raised for missing files, failed face detection, or verification mismatches.

## License

This project is released under the MIT License.

---

**Contact:** sujal58