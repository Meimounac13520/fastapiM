from typing import Optional
import aiohttp
import json

class TokenService:
    def __init__(self):
        self._token = None
        self._base_url = "http://end_point_url"

    async def get_valid_token(self) -> Optional[str]:
        # In real application, get token from DB
        if self._token:
            return self._token
        
        # If no token or invalid, get new token
        return await self._fetch_new_token()
    
    async def _fetch_new_token(self) -> Optional[str]:
        auth_header = "Basic dGVzdDpteXBhc3M="  # test:mypass
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base_url}/gettoken",
                headers={"Authorization": auth_header}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self._token = data.get("token")
                        return self._token
        return None