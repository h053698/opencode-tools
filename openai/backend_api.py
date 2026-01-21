from aiohttp import ClientSession

class OpenAIBackendAPI:
    BASE_URL = "https://chatgpt.com/backend-api"

    def __init__(self):
        session = ClientSession()

    async def get_codex_usage(self):