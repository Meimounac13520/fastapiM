from pydantic import BaseModel, Field
from typing import Optional

class PackageActivationRequest(BaseModel):
    subscriber_msisdn: str = Field(..., example="20941818")
    agent_msisdn: str = Field(..., example="22222222")
    mpin: str = Field(..., example="0000")
    amount: float = Field(..., example=100)
    package_group: str = Field(..., example="5")
    transaction_id: Optional[str] = Field(None, example="e321")

class PackageActivationResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Successful operation")
    errorcode: str = Field(..., example="0")
    system_transaction_id: int = Field(..., example=12)