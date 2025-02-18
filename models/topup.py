from pydantic import BaseModel, Field
from typing import Optional

class TopupRequest(BaseModel):
    vendor_wallet: str = Field(..., example="22222222")
    mpin: str = Field(..., example="0000")
    dest_msisdn: str = Field(..., example="20941919")
    amount: float = Field(..., example=1.0)
    transaction_id: Optional[str] = Field(None, example="yakjxvcb1")

class TopupResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Successful operation")
    errorcode: str = Field(..., example="0")
    system_transaction_id: int = Field(..., example=12)