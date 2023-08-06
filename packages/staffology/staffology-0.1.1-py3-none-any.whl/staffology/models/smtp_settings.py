from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.smtp_encryption import SmtpEncryption
from ..types import UNSET, Unset

T = TypeVar("T", bound="SmtpSettings")


@attr.s(auto_attribs=True)
class SmtpSettings:
    """
    Attributes:
        smtp_server (Union[Unset, None, str]):
        smtp_port (Union[Unset, int]):
        encryption (Union[Unset, SmtpEncryption]):
        smtp_username (Union[Unset, None, str]):
        smtp_password (Union[Unset, None, str]):
    """

    smtp_server: Union[Unset, None, str] = UNSET
    smtp_port: Union[Unset, int] = UNSET
    encryption: Union[Unset, SmtpEncryption] = UNSET
    smtp_username: Union[Unset, None, str] = UNSET
    smtp_password: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        smtp_server = self.smtp_server
        smtp_port = self.smtp_port
        encryption: Union[Unset, str] = UNSET
        if not isinstance(self.encryption, Unset):
            encryption = self.encryption.value

        smtp_username = self.smtp_username
        smtp_password = self.smtp_password

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if smtp_server is not UNSET:
            field_dict["smtpServer"] = smtp_server
        if smtp_port is not UNSET:
            field_dict["smtpPort"] = smtp_port
        if encryption is not UNSET:
            field_dict["encryption"] = encryption
        if smtp_username is not UNSET:
            field_dict["smtpUsername"] = smtp_username
        if smtp_password is not UNSET:
            field_dict["smtpPassword"] = smtp_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        smtp_server = d.pop("smtpServer", UNSET)

        smtp_port = d.pop("smtpPort", UNSET)

        _encryption = d.pop("encryption", UNSET)
        encryption: Union[Unset, SmtpEncryption]
        if isinstance(_encryption, Unset):
            encryption = UNSET
        else:
            encryption = SmtpEncryption(_encryption)

        smtp_username = d.pop("smtpUsername", UNSET)

        smtp_password = d.pop("smtpPassword", UNSET)

        smtp_settings = cls(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            encryption=encryption,
            smtp_username=smtp_username,
            smtp_password=smtp_password,
        )

        return smtp_settings
