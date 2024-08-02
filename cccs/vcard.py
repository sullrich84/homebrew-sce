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

        fn = f"{self.given_name} {self.family_name}"
        if (self.prefix):
            fn = f"{self.prefix} {fn}"

        return "\n".join(
            [
                f"BEGIN:VCARD",
                f"VERSION:3.0",
                f"N;CHARSET=utf-8:{self.family_name};{self.given_name};;{self.prefix};",
                f"FN;CHARSET=utf-8:{fn}",
                f"ORG:{self.organization}",
                f"ROLE:{self.role}",
                f"EMAIL;type=INTERNET;type=WORK;type=pref:{self.email}",
                f"TEL;type=CELL;type=VOICE;type=pref:{self.phone}",
                f"PHOTO;ENCODING=b;{self.image_url}",
                f"REV:{self.rev}",
                f"END:VCARD",
            ]
        )
