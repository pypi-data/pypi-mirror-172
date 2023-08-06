from enum import Enum


class RightToWorkDocumentType(str, Enum):
    OTHER = "Other"
    VISA = "Visa"
    PASSPORT = "Passport"
    BIRTHCERTIFICATE = "BirthCertificate"
    IDENTITYCARD = "IdentityCard"
    SHARECODE = "ShareCode"

    def __str__(self) -> str:
        return str(self.value)
