from pathlib import Path
import json
from dataclasses import dataclass


# openai
@dataclass
class OpencodeOpenaiOAuthSession:
    refresh: str
    access: str
    expires: int
    accountId: str


# github-copilot
@dataclass
class OpencodeGithubCopilotSession:
    refresh: str
    access: str
    expires: int = 0


# google
@dataclass
class OpencodeGoogleOAuthSession:
    refresh: str
    access: str
    expires: int = 0


def get_auth_data():
    auth_file = Path.home() / ".local" / "share" / "opencode" / "auth.json"

    with open(auth_file, "r") as f:
        auth_data = json.load(f)

    return auth_data
