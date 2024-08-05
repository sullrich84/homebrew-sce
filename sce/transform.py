import re
import base64
import requests
import dataclasses
from io import BytesIO
from string import Template
from alive_progress import alive_bar
from phonenumberfmt import format_phone_number
from sce.vcard import VCard


class VCardTransformer:
    """
    Transforms and sanitizes vCard information.

    Parameters
    ----------
    default_country_code : str
        Country code that will be used to parse and complete phone numbers.
    organization : str
        Default organization name that will be assigned to all extraced vCards.
    email_schema : str | None
        Schema that will be used to 'assume' the users email address. This Schema
        will be used when email addresses are not available.

    Authors
    -------
    Sebastian Ullrich <sebastian.ullrich@codecentric.de>
    """

    implied_phone_region = None
    organization = None
    email_schema = None

    def __init__(
        self,
        implied_phone_region: str,
        organization: str,
        email_schema: str | None = None,
    ):
        self.implied_phone_region = implied_phone_region
        self.organization = organization
        self.email_schema = email_schema

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
            phone_number=vcard.phone,
            implied_phone_region=self.implied_phone_region,
        )

        # Assign default organization if none provided
        sanitized_organization = vcard.organization
        if not sanitized_organization:
            sanitized_organization = self.organization

        # Imply email when no email is returned and schema is available
        sanitized_email = vcard.email
        if not sanitized_email and self.email_schema:
            template = Template(self.email_schema)
            sanitized_email = template.substitute(
                given_name=vcard.given_name,
                family_name=sanitized_family_name,
            ).lower()

        # Store image in file as base64
        image_b64 = self.__fetch_image_b64(vcard.image_url)

        updated_params = dataclasses.asdict(vcard)
        updated_params.update(
            {
                "family_name": sanitized_family_name,
                "email": sanitized_email,
                "phone": sanitized_phone,
                "organization": sanitized_organization,
                "image_b64": image_b64,
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
