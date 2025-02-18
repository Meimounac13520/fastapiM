from pydantic import BaseModel, Field

class BalanceRequest(BaseModel):
    dealer_account: str = Field(..., example="22222222")
    mpin: str = Field(..., example="0000")

class BalanceResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Success")
    errorcode: str = Field(..., example="0")
    balance: float = Field(..., example=1503)