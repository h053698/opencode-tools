from aiohttp import ClientSession
import platform
import uuid


def generate_user_agent() -> str:
    """Generate a realistic User-Agent string based on the current platform"""
    system = platform.system()

    if system == "Darwin":  # macOS
        os_version = platform.mac_ver()[0].replace(".", "_")
        platform_str = f"Macintosh; Intel Mac OS X {os_version}"
    elif system == "Windows":
        platform_str = "Windows NT 10.0; Win64; x64"
    else:  # Linux
        platform_str = "X11; Linux x86_64"

    chrome_version = "131.0.0.0"

    return (
        f"Mozilla/5.0 ({platform_str}) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_version} Safari/537.36"
    )


class OpenAIBackendAPI:

    def __init__(self):
        self.session = ClientSession()

    def _build_browser_headers(
        self, token: str, device_id: str, referral: str, user_agent: str
    ):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {token}",
            "oai-client-build-number": "4195295",
            "oai-client-version": "prod-db9ecebcc798846f5535282d71389bd2e15c025b",
            "oai-device-id": device_id,
            "oai-language": "en-US",
            "priority": "u=1, i",
            "Referer": referral,
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "User-Agent": user_agent,
        }

    async def get_codex_usage(self, token: str, device_id: str = None) -> dict:
        """
        Get Codex usage information

        Args:
            token: OAuth access token
            device_id: Device ID (optional, will generate if not provided)

        Returns:
            dict: Usage information from wham/usage endpoint
        """
        if device_id is None:
            device_id = str(uuid.uuid4())

        user_agent = generate_user_agent()

        default_headers = self._build_browser_headers(
            token, device_id, "https://chatgpt.com/codex/settings/usage", user_agent
        )

        async with ClientSession() as client:
            async with client.get(
                "https://chatgpt.com/backend-api/wham/usage", headers=default_headers
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise Exception(f"Error {resp.status}: {error_text}")

                return await resp.json()

    async def close(self):
        """Close the session"""
        await self.session.close()
