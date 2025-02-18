from pydantic import BaseModel, Field
from typing import Optional

class TokenResponse(BaseModel):
    success: bool = Field(
        description="Indicates if the token generation was successful",
        example=True
    )
    token: str = Field(
        description="Authentication token valid for 24 hours",
        example="b33d87767ed06a1c4b4bcdaaec6142d6"
    )
    errorcode: str = Field(
        description="Error code (0 for success)",
        example="0"
    )

class Credentials(BaseModel):
    username: str
    password: str