import base64
import logging
from typing import Optional
import aiohttp
import json

class TokenService:
    def __init__(self):
        self._token = None
        self._base_url = "https://www.chinguitel.mr"

    async def get_valid_token(self) -> Optional[str]:
        # In real application, get token from DB
        if self._token:
            return self._token
        
        # If no token or invalid, get new token
        return await self._fetch_new_token()
    
    async def _fetch_new_token(self) -> Optional[str]:
            credentials = "samartapi:samartapi"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            auth_header = f"Basic {encoded_credentials}"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://www.chinguitel.mr/evc2/gettoken",
                        headers={"Authorization": auth_header}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("success"):
                                self._token = data.get("token")
                                return self._token
                            else:
                                logging.error("Failed to fetch token: %s", data.get("errorcode"))
                        else:
                            logging.error("HTTP error occurred: %s", response.status)
            except Exception as e:
                logging.exception("Exception occurred while fetching token: %s", e)
            return None