from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.html_email_settings import HtmlEmailSettings
from ..models.smtp_settings import SmtpSettings
from ..types import UNSET, Unset

T = TypeVar("T", bound="MailSettings")


@attr.s(auto_attribs=True)
class MailSettings:
    """Determines the settings used when the Employer sends emails.
    If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal settings will be used;

        Attributes:
            sender_name (str):
            sender_email (str):
            customise_smtp_settings (bool):
            customise_html_email_settings (bool):
            use_system_from_address (Union[Unset, bool]): If set to true then the SenderEmail provided will only be used in
                the
                ReplyTo fields. The system defaults will be used for the From address.
            sender_email_verified (Union[Unset, bool]): [readonly] The SenderEmail must be verified before you can send
                email using that address
            smtp_settings (Union[Unset, SmtpSettings]):
            html_email_settings (Union[Unset, HtmlEmailSettings]):
            id (Union[Unset, str]): [readonly] The unique id of the object
    """

    sender_name: str
    sender_email: str
    customise_smtp_settings: bool
    customise_html_email_settings: bool
    use_system_from_address: Union[Unset, bool] = UNSET
    sender_email_verified: Union[Unset, bool] = UNSET
    smtp_settings: Union[Unset, SmtpSettings] = UNSET
    html_email_settings: Union[Unset, HtmlEmailSettings] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sender_name = self.sender_name
        sender_email = self.sender_email
        customise_smtp_settings = self.customise_smtp_settings
        customise_html_email_settings = self.customise_html_email_settings
        use_system_from_address = self.use_system_from_address
        sender_email_verified = self.sender_email_verified
        smtp_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.smtp_settings, Unset):
            smtp_settings = self.smtp_settings.to_dict()

        html_email_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.html_email_settings, Unset):
            html_email_settings = self.html_email_settings.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "senderName": sender_name,
                "senderEmail": sender_email,
                "customiseSmtpSettings": customise_smtp_settings,
                "customiseHtmlEmailSettings": customise_html_email_settings,
            }
        )
        if use_system_from_address is not UNSET:
            field_dict["useSystemFromAddress"] = use_system_from_address
        if sender_email_verified is not UNSET:
            field_dict["senderEmailVerified"] = sender_email_verified
        if smtp_settings is not UNSET:
            field_dict["smtpSettings"] = smtp_settings
        if html_email_settings is not UNSET:
            field_dict["htmlEmailSettings"] = html_email_settings
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sender_name = d.pop("senderName")

        sender_email = d.pop("senderEmail")

        customise_smtp_settings = d.pop("customiseSmtpSettings")

        customise_html_email_settings = d.pop("customiseHtmlEmailSettings")

        use_system_from_address = d.pop("useSystemFromAddress", UNSET)

        sender_email_verified = d.pop("senderEmailVerified", UNSET)

        _smtp_settings = d.pop("smtpSettings", UNSET)
        smtp_settings: Union[Unset, SmtpSettings]
        if isinstance(_smtp_settings, Unset):
            smtp_settings = UNSET
        else:
            smtp_settings = SmtpSettings.from_dict(_smtp_settings)

        _html_email_settings = d.pop("htmlEmailSettings", UNSET)
        html_email_settings: Union[Unset, HtmlEmailSettings]
        if isinstance(_html_email_settings, Unset):
            html_email_settings = UNSET
        else:
            html_email_settings = HtmlEmailSettings.from_dict(_html_email_settings)

        id = d.pop("id", UNSET)

        mail_settings = cls(
            sender_name=sender_name,
            sender_email=sender_email,
            customise_smtp_settings=customise_smtp_settings,
            customise_html_email_settings=customise_html_email_settings,
            use_system_from_address=use_system_from_address,
            sender_email_verified=sender_email_verified,
            smtp_settings=smtp_settings,
            html_email_settings=html_email_settings,
            id=id,
        )

        return mail_settings
