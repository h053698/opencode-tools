from asyncio import run
from aiohttp import ClientSession
from utils import PKCEGenerator, build_auth_url, generate_state, get_code, APP_ID

from dataclasses import dataclass


@dataclass
class OpenAICodexSession:
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str
    scope: str
    token_type: str


async def get_session(code: str, verifier: str) -> dict:
    client = ClientSession()
    async with client.post(
        "https://auth.openai.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": verifier,
            "redirect_uri": "http://localhost:1455/auth/callback",
            "client_id": APP_ID,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ) as resp:
        return await resp.json()


async def get_oauth_token():
    verifier, challenge = PKCEGenerator.generate_pkce()
    print(f"Code Verifier: {verifier}")
    print(f"Code Challenge: {challenge}")

    state = generate_state()
    print(f"State: {state}")

    auth_url = build_auth_url(state, challenge)
    print(f"Auth URL: {auth_url}")

    return_url = input("callback: ")
    grant_code = get_code(return_url)
    print(f"Grant Code: {grant_code}")

    session = await get_session(grant_code, verifier)
    print(session)


if __name__ == "__main__":
    run(get_oauth_token())
