from slack_sdk import WebClient
from typing import Optional
from cccs.vcard import VCard


class SlackExtractor:
    """
    Extractor to fetch all slack users via the slack api.

    Parameters
    ----------
    token : str
        Service token to authenticate against the slack api. The token must have
        the scopes 'users:read' and 'users:read.email' assigned.
    organization : str
        Default organization name that will be assigned to all extraced vcards.

    Authors
    -------
    Sebastian Ullrich <sebastian.ullrich@codecentric.de>
    """

    token = None
    vcards = []

    def __init__(self, token: str):
        self.token = token

    def __fetch_slack_users(self):
        client = WebClient(token=self.token)
        cursor, users = None, []

        while True:
            # Iterate over all slack user.encode("utf-8")s
            response = client.users_list(cursor=cursor, limit=1000, include_locale=True)
            cursor = response.get("response_metadata", {}).get("next_cursor")
            users.extend(response["members"])

            if not cursor:
                break

        return users

   
    def __to_vcard(self, member) -> Optional[VCard]:
        profile = member["profile"]

        first_name = str(profile.get("first_name")).strip()
        last_name = str(profile.get("last_name")).strip()

        email = profile.get("email")
        phone = profile.get("phone")
        image_url = profile.get("image_1024")

        if None in {first_name, last_name, image_url, phone}:
            return None

        return VCard(
            prefix="",
            given_name=first_name,
            family_name=last_name,
            image_url=image_url,
            organization="",
            role="",
            email=email,
            phone=phone,
        )

    def extract(self) -> list[VCard]:
        for user in self.__fetch_slack_users():
            # Filter out disable users, guests and bots
            if user["deleted"] or user["is_bot"] or user["is_restricted"]:
                continue

            vcard = self.__to_vcard(user)
            if vcard:
                self.vcards.append(vcard)

        return self.vcards
