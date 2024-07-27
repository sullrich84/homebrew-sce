from dataclasses import dataclass
from datetime import datetime

@dataclass
class VCard:
    prefix: str
    given_name: str
    family_name: str
    image_url: str
    organization: str
    role: str
    email: str
    phone: str
    rev: str = datetime.now().strftime("%Y%m%dT%H%M%SZ")

    def render(self):
        return [
            f"BEGIN:VCARD",
            f"VERSION:4.0",
            f"N:{self.family_name};{self.given_name};;{self.prefix};",
            f"FN:{self.prefix} {self.given_name} {self.family_name}",
            f"ORG:{self.organization}",
            f"ROLE:{self.role}",
            f"PHOTO;MEDIATYPE=image/jpeg:{self.image_url}",
            f"TEL;TYPE=work,voice;VALUE=uri:tel:{self.phone}",
            f"EMAIL:{self.email}",
            f"REV:{self.rev}",
            f"END:VCARD",
        ]
