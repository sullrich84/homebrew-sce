import subprocess
from slack_sdk import WebClient


def fetch_slack_token():
    result = subprocess.run(
        ["op", "item", "get", "Slack Service Token", "--fields", "password"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def extract_slack_users(token: str):
    client = WebClient(token=token)
    print(f"Using token: {token}")

    cursor = None
    users = []

    while True:
        # Iterate over all slack users
        response = client.users_list(cursor=cursor, limit=1000, include_locale=True)
        cursor = response.get("response_metadata", {}).get("next_cursor")

        if not cursor:
            break

        for member in response["members"]:
            # Filter out disable users, guests and bots
            if member["deleted"] or member["is_bot"] or member["is_restricted"]:
                continue

            user = parse_slack_member(member)
            if user:
                users.append(user)

    return users


def parse_slack_member(member):
    profile = member["profile"]

    first_name = str(profile.get("first_name")).strip()
    last_name = str(profile.get("last_name")).strip()

    email = profile.get("email")
    image = profile.get("image_original")
    phone = profile.get("phone")

    if None in {first_name, last_name, image, phone}:
        return None

    return {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "image": image,
    }


def extract_all():
    token = fetch_slack_token()
    slack_users = extract_slack_users(token=token)

    return [*slack_users]
