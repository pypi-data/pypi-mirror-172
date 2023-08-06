from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.webhook_event import WebhookEvent
from ..models.webhook_payload import WebhookPayload
from ..types import UNSET, Unset

T = TypeVar("T", bound="Webhook")


@attr.s(auto_attribs=True)
class Webhook:
    """
    Attributes:
        url (str): The Url to which the payload should be sent
        webhook_event (Union[Unset, WebhookEvent]):
        active (Union[Unset, bool]): If set to false then this Webhook will not be triggered
        event_count (Union[Unset, int]): The number of times this webhook has been triggered
        last_payload (Union[Unset, WebhookPayload]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    url: str
    webhook_event: Union[Unset, WebhookEvent] = UNSET
    active: Union[Unset, bool] = UNSET
    event_count: Union[Unset, int] = UNSET
    last_payload: Union[Unset, WebhookPayload] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        webhook_event: Union[Unset, str] = UNSET
        if not isinstance(self.webhook_event, Unset):
            webhook_event = self.webhook_event.value

        active = self.active
        event_count = self.event_count
        last_payload: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_payload, Unset):
            last_payload = self.last_payload.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "url": url,
            }
        )
        if webhook_event is not UNSET:
            field_dict["webhookEvent"] = webhook_event
        if active is not UNSET:
            field_dict["active"] = active
        if event_count is not UNSET:
            field_dict["eventCount"] = event_count
        if last_payload is not UNSET:
            field_dict["lastPayload"] = last_payload
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        _webhook_event = d.pop("webhookEvent", UNSET)
        webhook_event: Union[Unset, WebhookEvent]
        if isinstance(_webhook_event, Unset):
            webhook_event = UNSET
        else:
            webhook_event = WebhookEvent(_webhook_event)

        active = d.pop("active", UNSET)

        event_count = d.pop("eventCount", UNSET)

        _last_payload = d.pop("lastPayload", UNSET)
        last_payload: Union[Unset, WebhookPayload]
        if isinstance(_last_payload, Unset):
            last_payload = UNSET
        else:
            last_payload = WebhookPayload.from_dict(_last_payload)

        id = d.pop("id", UNSET)

        webhook = cls(
            url=url,
            webhook_event=webhook_event,
            active=active,
            event_count=event_count,
            last_payload=last_payload,
            id=id,
        )

        return webhook
