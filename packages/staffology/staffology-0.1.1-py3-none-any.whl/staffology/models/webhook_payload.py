import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_status import BackgroundTaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookPayload")


@attr.s(auto_attribs=True)
class WebhookPayload:
    """
    Attributes:
        url (str): [readonly] The Url that payload will be sent to
        name (Union[Unset, None, str]): [readonly] A descriptive name for this payload
        attempts (Union[Unset, int]): [readonly]  The number of attempts that have been made to deliver this payload
        status_code (Union[Unset, int]): [readonly] The status code received from the Url
        task_status (Union[Unset, BackgroundTaskStatus]):
        status_message (Union[Unset, None, str]): [readonly]  A message to accompany the status
        created (Union[Unset, datetime.date]): [readonly]  The date and time this payload was created
        payload (Union[Unset, Any]): [readonly] the JSON payload that will be sent to the URl
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    url: str
    name: Union[Unset, None, str] = UNSET
    attempts: Union[Unset, int] = UNSET
    status_code: Union[Unset, int] = UNSET
    task_status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    created: Union[Unset, datetime.date] = UNSET
    payload: Union[Unset, Any] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        name = self.name
        attempts = self.attempts
        status_code = self.status_code
        task_status: Union[Unset, str] = UNSET
        if not isinstance(self.task_status, Unset):
            task_status = self.task_status.value

        status_message = self.status_message
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        payload = self.payload
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "url": url,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if attempts is not UNSET:
            field_dict["attempts"] = attempts
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if task_status is not UNSET:
            field_dict["taskStatus"] = task_status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if created is not UNSET:
            field_dict["created"] = created
        if payload is not UNSET:
            field_dict["payload"] = payload
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        name = d.pop("name", UNSET)

        attempts = d.pop("attempts", UNSET)

        status_code = d.pop("statusCode", UNSET)

        _task_status = d.pop("taskStatus", UNSET)
        task_status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_task_status, Unset):
            task_status = UNSET
        else:
            task_status = BackgroundTaskStatus(_task_status)

        status_message = d.pop("statusMessage", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.date]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created).date()

        payload = d.pop("payload", UNSET)

        id = d.pop("id", UNSET)

        webhook_payload = cls(
            url=url,
            name=name,
            attempts=attempts,
            status_code=status_code,
            task_status=task_status,
            status_message=status_message,
            created=created,
            payload=payload,
            id=id,
        )

        return webhook_payload
