from enum import Enum


class SmtpEncryption(str, Enum):
    AUTO = "Auto"
    SSL = "Ssl"
    TLS = "Tls"

    def __str__(self) -> str:
        return str(self.value)
