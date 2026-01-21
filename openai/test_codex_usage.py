from asyncio import run
from pathlib import Path
import json
from datetime import datetime, timedelta
from backend_api import OpenAIBackendAPI


def format_time(seconds: int) -> str:
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def display_usage(usage: dict):
    """Display usage data in a readable format"""
    print("\n" + "=" * 60)
    print("OPENAI CODEX USAGE")
    print("=" * 60)

    # Plan type
    plan_type = usage.get("plan_type", "unknown").upper()
    print(f"\nPlan Type: {plan_type}")

    # Rate Limit
    print("\n--- RATE LIMIT ---")
    rate_limit = usage.get("rate_limit", {})
    allowed = "✓ ALLOWED" if rate_limit.get("allowed") else "✗ NOT ALLOWED"
    limit_reached = "✗ LIMIT REACHED" if rate_limit.get("limit_reached") else "✓ Available"
    print(f"Status: {allowed} | {limit_reached}")

    # Primary Window (5 hour usage limit)
    primary = rate_limit.get("primary_window", {})
    if primary:
        print(f"\n5-Hour Usage Limit:")
        print(f"  Used: {primary.get('used_percent', 0)}%")
        print(f"  Resets in: {format_time(primary.get('reset_after_seconds', 0))}")
        reset_at = datetime.fromtimestamp(primary.get('reset_at', 0))
        print(f"  Reset at: {reset_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Secondary Window (Weekly usage limit)
    secondary = rate_limit.get("secondary_window", {})
    if secondary:
        print(f"\nWeekly Usage Limit:")
        print(f"  Used: {secondary.get('used_percent', 0)}%")
        print(f"  Resets in: {format_time(secondary.get('reset_after_seconds', 0))}")
        reset_at = datetime.fromtimestamp(secondary.get('reset_at', 0))
        print(f"  Reset at: {reset_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Code Review Rate Limit
    print("\n--- CODE REVIEW RATE LIMIT ---")
    cr_limit = usage.get("code_review_rate_limit", {})
    cr_allowed = "✓ ALLOWED" if cr_limit.get("allowed") else "✗ NOT ALLOWED"
    cr_limit_reached = "✗ LIMIT REACHED" if cr_limit.get("limit_reached") else "✓ Available"
    print(f"Status: {cr_allowed} | {cr_limit_reached}")

    cr_primary = cr_limit.get("primary_window", {})
    if cr_primary:
        print(f"\nWeekly Code Review Limit:")
        print(f"  Used: {cr_primary.get('used_percent', 0)}%")
        print(f"  Resets in: {format_time(cr_primary.get('reset_after_seconds', 0))}")
        reset_at = datetime.fromtimestamp(cr_primary.get('reset_at', 0))
        print(f"  Reset at: {reset_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Credits
    print("\n--- CREDITS ---")
    credits = usage.get("credits", {})
    has_credits = "✓ YES" if credits.get("has_credits") else "✗ NO"
    unlimited = "✓ YES" if credits.get("unlimited") else "✗ NO"
    print(f"Has Credits: {has_credits}")
    print(f"Unlimited: {unlimited}")
    print(f"Balance: {credits.get('balance', '0')}")

    local_msgs = credits.get("approx_local_messages", [0, 0])
    cloud_msgs = credits.get("approx_cloud_messages", [0, 0])
    print(f"Approx Local Messages: {local_msgs}")
    print(f"Approx Cloud Messages: {cloud_msgs}")

    print("\n" + "=" * 60)


async def test_codex_usage():
    """Test Codex usage API"""
    print("=== Codex Usage Test ===\n")

    # Load access token from local auth.json
    auth_file = Path("auth.json")

    if not auth_file.exists():
        print(f"Error: auth.json not found in current directory")
        return

    with open(auth_file, "r") as f:
        auth_data = json.load(f)

    # Get access token
    token = auth_data.get("access_token")

    if not token:
        print("Error: access_token not found in auth.json")
        return

    print(f"✓ Loaded access token from {auth_file}")

    device_id = input("Enter device ID (press Enter to auto-generate): ").strip()

    if not device_id:
        device_id = None

    api = OpenAIBackendAPI()

    try:
        print("\nFetching Codex usage...")
        usage = await api.get_codex_usage(token=token, device_id=device_id)

        display_usage(usage)

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        await api.close()


if __name__ == "__main__":
    run(test_codex_usage())
