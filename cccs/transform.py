import re
from typing import List
from cccs.vcard import VCard
from phonenumberfmt import format_phone_number


def sanitize(vcard: VCard):
    # Remove brackets containing pronouns
    sanitized_family_name = re.sub(r"\s*\(.*?\)", "", vcard.family_name)
   
    # Sanitize phone numbers, assume that these are german cell phone numbers only
    sanitized_given_name = format_phone_number(vcard.given_name, implied_phone_region="DE")

    return vcard


def transform_all(vcards: List[VCard]):
    sanitized_vcards = []

    for vcard in vcards:
        sanitized_vcards.append(sanitize(vcard))

    return vcards
