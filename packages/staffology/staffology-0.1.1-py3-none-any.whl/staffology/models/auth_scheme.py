from enum import Enum


class AuthScheme(str, Enum):
    OAUTH1 = "OAuth1"
    OAUTH2 = "OAuth2"
    BASIC = "Basic"
    APIKEYINHEADER = "ApiKeyInHeader"
    HMAC = "Hmac"
    OAUTH2CC = "OAuth2Cc"
    OAUTH2PASSWORD = "OAuth2Password"

    def __str__(self) -> str:
        return str(self.value)
