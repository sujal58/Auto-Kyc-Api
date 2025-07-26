from fastapi import FastAPI
from app.api.v1.routes import router as kyc_router

app = FastAPI(title="KYC Automation API")


app.include_router(kyc_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to KYC Automation API"}