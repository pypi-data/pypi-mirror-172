import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_status import BackgroundTaskStatus
from ..models.email_attachment import EmailAttachment
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerEmail")


@attr.s(auto_attribs=True)
class EmployerEmail:
    """
    Attributes:
        to_name (str):
        to_email (str):
        subject (str):
        status_message (Union[Unset, None, str]):
        button_text (Union[Unset, None, str]):
        button_link (Union[Unset, None, str]):
        body_preview (Union[Unset, None, str]):
        body (Union[Unset, None, str]):
        after_btn_body (Union[Unset, None, str]):
        status (Union[Unset, BackgroundTaskStatus]):
        status_date (Union[Unset, datetime.datetime]):
        status_message (Union[Unset, None, str]):
        send_attempts (Union[Unset, int]):
        web_app_base_url (Union[Unset, None, str]):
        attachments (Union[Unset, None, List[EmailAttachment]]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    to_name: str
    to_email: str
    subject: str
    status_message: Union[Unset, None, str] = UNSET
    button_text: Union[Unset, None, str] = UNSET
    button_link: Union[Unset, None, str] = UNSET
    body_preview: Union[Unset, None, str] = UNSET
    body: Union[Unset, None, str] = UNSET
    after_btn_body: Union[Unset, None, str] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_date: Union[Unset, datetime.datetime] = UNSET
    send_attempts: Union[Unset, int] = UNSET
    web_app_base_url: Union[Unset, None, str] = UNSET
    attachments: Union[Unset, None, List[EmailAttachment]] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        to_name = self.to_name
        to_email = self.to_email
        subject = self.subject
        status_message = self.status_message
        button_text = self.button_text
        button_link = self.button_link
        body_preview = self.body_preview
        body = self.body
        after_btn_body = self.after_btn_body
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_date: Union[Unset, str] = UNSET
        if not isinstance(self.status_date, Unset):
            status_date = self.status_date.isoformat()

        status_message = self.status_message
        send_attempts = self.send_attempts
        web_app_base_url = self.web_app_base_url
        attachments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            if self.attachments is None:
                attachments = None
            else:
                attachments = []
                for attachments_item_data in self.attachments:
                    attachments_item = attachments_item_data.to_dict()

                    attachments.append(attachments_item)

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "toName": to_name,
                "toEmail": to_email,
                "subject": subject,
            }
        )
        if status_message is not UNSET:
            field_dict["_statusMessage"] = status_message
        if button_text is not UNSET:
            field_dict["buttonText"] = button_text
        if button_link is not UNSET:
            field_dict["buttonLink"] = button_link
        if body_preview is not UNSET:
            field_dict["bodyPreview"] = body_preview
        if body is not UNSET:
            field_dict["body"] = body
        if after_btn_body is not UNSET:
            field_dict["afterBtnBody"] = after_btn_body
        if status is not UNSET:
            field_dict["status"] = status
        if status_date is not UNSET:
            field_dict["statusDate"] = status_date
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if send_attempts is not UNSET:
            field_dict["sendAttempts"] = send_attempts
        if web_app_base_url is not UNSET:
            field_dict["webAppBaseUrl"] = web_app_base_url
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        to_name = d.pop("toName")

        to_email = d.pop("toEmail")

        subject = d.pop("subject")

        status_message = d.pop("_statusMessage", UNSET)

        button_text = d.pop("buttonText", UNSET)

        button_link = d.pop("buttonLink", UNSET)

        body_preview = d.pop("bodyPreview", UNSET)

        body = d.pop("body", UNSET)

        after_btn_body = d.pop("afterBtnBody", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)

        _status_date = d.pop("statusDate", UNSET)
        status_date: Union[Unset, datetime.datetime]
        if isinstance(_status_date, Unset):
            status_date = UNSET
        else:
            status_date = isoparse(_status_date)

        status_message = d.pop("statusMessage", UNSET)

        send_attempts = d.pop("sendAttempts", UNSET)

        web_app_base_url = d.pop("webAppBaseUrl", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = EmailAttachment.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        id = d.pop("id", UNSET)

        employer_email = cls(
            to_name=to_name,
            to_email=to_email,
            subject=subject,
            status_message=status_message,
            button_text=button_text,
            button_link=button_link,
            body_preview=body_preview,
            body=body,
            after_btn_body=after_btn_body,
            status=status,
            status_date=status_date,
            send_attempts=send_attempts,
            web_app_base_url=web_app_base_url,
            attachments=attachments,
            id=id,
        )

        return employer_email
