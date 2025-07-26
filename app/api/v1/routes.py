from fastapi import APIRouter, HTTPException
from app.model.kyc_model import KycRequest
from app.services.Kyc_service import perform_kyc_verification

router = APIRouter()

@router.post("/kyc-verify")
async def kyc_verify_endpoint(request: KycRequest):
    print(request)
    try:
        # Perform KYC verification
        result = perform_kyc_verification(
            document_front_path=request.document_front_path,
            document_back_path=request.document_back_path,
            user_image_path=request.user_image_path,
            user_info={
                "name": request.name,
                "document_number": request.document_number
            }
        )
        print(result)
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))