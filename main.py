from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from models.topup import TopupRequest, TopupResponse
from services.token_service import TokenService
import aiohttp
from models.package import PackageActivationRequest, PackageActivationResponse
# Add to existing imports
from models.balance import BalanceRequest, BalanceResponse
from fastapi import FastAPI, HTTPException
import httpx
import base64
BASE_URL = "https://192.168.102.3:443/gettoken"  # Placeholder for the actual URL
CREDENTIALS = "samartapi:samartapi"
ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS.encode()).decode()
AUTH_HEADER = {"Authorization": f"Basic {ENCODED_CREDENTIALS}"}
app = FastAPI(
    title="Authentication API",
    description="""
    Authentication API for token generation.
    
    ## Authentication
    This API uses Basic Authentication for token generation
    """,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
)
@app.post("/gettoken")
async def get_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, headers=AUTH_HEADER)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"token": data.get("token")}
            else:
                raise HTTPException(status_code=400, detail="Failed to retrieve token")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from token service")


# Initialize token service
token_service = TokenService()

@app.post(
    "/topup",
    response_model=TopupResponse,
    tags=["topup"],
    summary="Process topup request",
    responses={
        200: {
            "description": "Successful topup",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Successful operation",
                        "errorcode": "0",
                        "system_transaction_id": 12
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Invalid request",
                        "errorcode": "400",
                        "system_transaction_id": 0
                    }
                }
            }
        }
    }
)
async def topup(request: TopupRequest):
    """
    Process a topup request
    
    ## Request Body
    * vendor_wallet: The vendor wallet account that will pay
    * mpin: The pin of the msisdn
    * dest_msisdn: The msisdn that will get paid
    * amount: The amount that will be paid
    * transaction_id: Optional unique transaction ID
    
    ## Error Codes
    * 0 = success
    * 400 = Invalid request or missing parameter
    * 500 = connection error
    * 21 = Invalid msisdn
    * 22 = msisdn is blocked
    * 30 = invalid MPIN
    * 41 = destination msisdn not found
    * 42 = destination msisdn is blocked
    * 50 = source msisdn and destination msisdn are the same
    * 61 = balance is not enough
    * 62 = amount is less than minimum (minimum is 5)
    * 63 = amount is more than maximum
    * 71 = operation rule are not met
    * 72 = operation is not permitted
    * 99 = Unknown error
    """
    # Get valid token
    token = await token_service.get_valid_token()
    if not token:
        return TopupResponse(
            success=False,
            message="Failed to obtain authentication token",
            errorcode="500",
            system_transaction_id=0
        )

    # Call topup API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://192.168.102.3:443/evc2/topup",
            headers={"Authorization": token},
            json=request.dict(exclude_none=True)
        ) as response:
            data = await response.json()
            return TopupResponse(
                success=data.get("success", False),
                message=data.get("message", "Unknown error"),
                errorcode=str(data.get("errorcode", "99")),
                system_transaction_id=data.get("system_transaction_id", 0)
            )

@app.post(
    "/package-activation",
    response_model=PackageActivationResponse,
    tags=["package"],
    summary="Activate package for subscriber",
    responses={
        200: {
            "description": "Successful package activation",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Successful operation",
                        "errorcode": "0",
                        "system_transaction_id": 12
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Invalid request",
                        "errorcode": "400",
                        "system_transaction_id": 0
                    }
                }
            }
        }
    }
)
async def activate_package(request: PackageActivationRequest):
    """
    Activate a package for a subscriber through EVC account
    
    ## Request Body
    * subscriber_msisdn: The msisdn that will get the package
    * agent_msisdn: The agent wallet that will pay
    * mpin: The pin of the agent_msisdn
    * amount: The amount of the package
    * package_group: The package group
    * transaction_id: Optional unique transaction ID
    
    ## Error Codes
    * 0 = success
    * 400 = invalid request
    * 500 = connection error
    * 10 = cannot find package at specified amount
    * 20 = incorrect pack code. waiting 1/2/3
    * 30 = incorrect mpin
    * 40 = Incorrect subscriber's MDN
    * 50 = Agent's MDN does not exist
    * 999 = Unspecified error
    """
    # Get valid token
    token = await token_service.get_valid_token()
    if not token:
        return PackageActivationResponse(
            success=False,
            message="Failed to obtain authentication token",
            errorcode="500",
            system_transaction_id=0
        )

    # Call package activation API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://192.168.102.3:443/evc2/package-activation",
            headers={"Authorization": token},
            json=request.dict(exclude_none=True)
        ) as response:
            data = await response.json()
            return PackageActivationResponse(
                success=data.get("success", False),
                message=data.get("message", "Unknown error"),
                errorcode=str(data.get("errorcode", "999")),
                system_transaction_id=data.get("system_transaction_id", 0)
            )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Authentication API",
        version="1.0.0",
        description="API for token generation",
        routes=app.routes,
    )
    
    # Add basic auth security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {
            "type": "http",
            "scheme": "basic"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add after existing endpoints
@app.post(
    "/query-balance",
    response_model=BalanceResponse,
    tags=["balance"],
    summary="Query dealer EVC account balance",
    responses={
        200: {
            "description": "Successful balance query",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Success",
                        "errorcode": "0",
                        "balance": 1503
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Invalid request",
                        "errorcode": "400",
                        "balance": 0
                    }
                }
            }
        }
    }
)
async def query_balance(request: BalanceRequest):
    """
    Query dealer EVC account balance
    
    ## Request Body
    * dealer_account: The dealer EVC account
    * mpin: The pin of the dealer account
    
    ## Error Codes
    * 0 = success
    * 400 = invalid request
    * 500 = connection error
    * 11 = connection error with OCS
    * 21 = Invalid msisdn
    * 22 = msisdn is blocked
    * 30 = invalid MPIN
    * 99 = Unknown error
    """
    # Get valid token
    token = await token_service.get_valid_token()
    if not token:
        return BalanceResponse(
            success=False,
            message="Failed to obtain authentication token",
            errorcode="500",
            balance=0
        )

    # Call balance query API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://192.168.102.3:443/evc2/query-balance",
            headers={"Authorization": token},
            json=request.dict()
        ) as response:
            data = await response.json()
            return BalanceResponse(
                success=data.get("success", False),
                message=data.get("message", "Unknown error"),
                errorcode=str(data.get("errorcode", "99")),
                balance=float(data.get("balance", 0))
            )