import json
from pathlib import Path

from openai.get_oauth_token import OpenAICodexSession
from openai.utils import convert_expires_in_to_opencode_format, extract_account_id
from utils import get_auth_data, OpencodeOpenaiOAuthSession

from dataclasses import asdict


async def switch_openai_session(session: OpenAICodexSession):
    auth_data = get_auth_data()

    auth_file = Path.home() / ".local" / "share" / "opencode" / "auth.json"

    if not "openai" in auth_data:
        auth_data["openai"] = {}

    auth_data["openai"] = {"type": "oauth"}.update(
        asdict(
            OpencodeOpenaiOAuthSession(
                refresh=session.refresh_token,
                access=session.access_token,
                expires=convert_expires_in_to_opencode_format(session.expires_in),
                accountId=extract_account_id(session.id_token),
            )
        )
    )

    with open(auth_file, "w") as f:
        json.dump(auth_data, f, indent=2)
