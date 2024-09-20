from dataclasses import dataclass
from datetime import datetime


@dataclass
class VCard:
    """
    Custom vCard 3.0 implementation as used on Mac OSX.

    Authors
    -------
    Sebastian Ullrich <sebastian.ullrich@codecentric.de>
    """
    uid: str
    given_name: str
    family_name: str
    image_url: str
    organization: str
    role: str
    email: str
    phone: str
    rev: str = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    
    title: str = ""
    note: str = ""
    prefix: str | None = None
    image_b64: str | None = None

    def render(self):
        fn = f"{self.given_name} {self.family_name}"
        if self.prefix:
            fn = f"{self.prefix} {fn}"

        return "\n".join(
            [
                f"BEGIN:VCARD",
                f"VERSION:3.0",
                f"N;CHARSET=utf-8:{self.family_name};{self.given_name};;{self.prefix};",
                f"FN;CHARSET=utf-8:{fn}",
                f"UID:{self.uid}",
                f"ORG:{self.organization}",
                f"ROLE:{self.role}",
                f"TITLE:{self.role}",
                f"EMAIL;type=INTERNET;type=WORK;type=pref:{self.email}",
                f"TEL;type=CELL;type=VOICE;type=pref:{self.phone}",
                f"PHOTO;ENCODING=b;{self.image_b64}",
                f"REV:{self.rev}",
                f"NOTE:{self.note}"
                f"",
                f"END:VCARD",
            ]
        )
