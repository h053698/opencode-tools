import hashlib
import base64
import secrets
import string
import time
from urllib.parse import urlencode, parse_qs, urlparse
from typing import Tuple
import jwt

OPENAI_OAUTH_URL = "https://auth.openai.com/oauth/authorize"
APP_ID = "app_EMoamEEZ73f0CkXaXp7hrann"


def get_code(url: str) -> str:
    query_string = urlparse(url).query
    return dict(parse_qs(query_string)).get("code")[0]


def convert_expires_in_to_opencode_format(expires_in: int) -> int:
    return int(int(time.time() * 1000) + expires_in or 3600) * 1000


def extract_account_id(id_token: str) -> str:
    claims = jwt.decode(id_token, options={"verify_signature": False})

    if claims.get("chatgpt_account_id"):
        return claims["chatgpt_account_id"]

    auth_section = claims.get("https://api.openai.com/auth")
    if auth_section and auth_section.get("chatgpt_account_id"):
        return auth_section["chatgpt_account_id"]

    orgs = claims.get("organizations")
    if orgs and len(orgs) > 0 and orgs[0].get("id"):
        return orgs[0]["id"]

    return ""


class PKCEGenerator:
    @staticmethod
    def generate_random_string(length: int = 43) -> str:
        chars = string.ascii_letters + string.digits + "-._~"
        return "".join(secrets.choice(chars) for _ in range(length))

    @staticmethod
    def base64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    @classmethod
    def generate_pkce(cls) -> Tuple[str, str]:
        verifier = cls.generate_random_string(43)
        challenge = cls.base64url_encode(
            hashlib.sha256(verifier.encode("utf-8")).digest()
        )
        return verifier, challenge


def generate_state() -> str:
    return PKCEGenerator.base64url_encode(secrets.token_bytes(32))


def build_auth_url(
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
) -> str:
    params = {
        "response_type": "code",
        "client_id": APP_ID,
        "redirect_uri": "http://localhost:1455/auth/callback",
        "scope": "openid profile email offline_access",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "originator": "opencode",
    }
    return f"{OPENAI_OAUTH_URL}?{urlencode(params)}"
