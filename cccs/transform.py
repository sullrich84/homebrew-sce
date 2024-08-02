import re
import base64
import requests
import dataclasses
from io import BytesIO
from alive_progress import alive_bar
from phonenumberfmt import format_phone_number
from cccs.vcard import VCard


class VCardTransformer:
    """
    Transforms and sanitized VCard informations.

    Parameters
    ----------
    default_country_code : str
        Country code that will be used to parse and complete phone numbers.

    Authors
    -------
    Sebastian Ullrich <sebastian.ullrich@codecentric.de>
    """

    implied_phone_region = None
    organization = None

    def __init__(self, implied_phone_region: str, organization: str):
        self.implied_phone_region = implied_phone_region
        self.organization = organization

    def __fetch_image_b64(self, image_url: str):
        response = requests.get(image_url)
        response.raise_for_status()

        image_data = BytesIO(response.content)
        base64_encoded_image = base64.b64encode(image_data.read()).decode("utf-8")

        image_type = "JPEG"
        if image_url.endswith(".png"):
            image_type = "PNG"

        return f"TYPE={image_type}:{base64_encoded_image}"

    def __sanitize(self, vcard: VCard) -> VCard:
        # Remove brackets containing pronouns
        sanitized_family_name = re.sub(r"\s*\(.*?\)", "", vcard.family_name)

        # Sanitize phone numbers, assume that these are german cell phone numbers only
        sanitized_phone = format_phone_number(
            vcard.phone, implied_phone_region=self.implied_phone_region
        )

        # Assign default organization if none provided
        sanitized_organization = vcard.organization
        if not sanitized_organization:
            self.organization

        # Store image in file as base64
        sanitized_image = self.__fetch_image_b64(vcard.image_url)

        updated_params = dataclasses.asdict(vcard)
        updated_params.update(
            {
                "family_name": sanitized_family_name,
                "phone": sanitized_phone,
                "organization": sanitized_organization,
                "image_url": sanitized_image,
            }
        )

        return VCard(**updated_params)

    def transform(self, vcards: list[VCard]) -> list[VCard]:
        sanitized_vcards = []
        total = len(vcards)

        with alive_bar(total, dual_line=True, title="Fetching user images") as bar:
            for vcard in vcards:
                bar.text = (
                    f"Fetching user image for {vcard.given_name} {vcard.family_name}..."
                )
                sanitized_vcard = self.__sanitize(vcard)
                sanitized_vcards.append(sanitized_vcard)
                bar()

        return sanitized_vcards
