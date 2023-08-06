from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.background_task_status import BackgroundTaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalProviderConversation")


@attr.s(auto_attribs=True)
class ExternalProviderConversation:
    """This model is used to provide details of a data exchange with an ExternalDataProvider

    Attributes:
        title (Union[Unset, None, str]):
        content_type (Union[Unset, None, str]):
        url (Union[Unset, None, str]):
        request (Union[Unset, None, str]):
        response (Union[Unset, None, str]):
        status (Union[Unset, BackgroundTaskStatus]):
        status_message (Union[Unset, None, str]):
    """

    title: Union[Unset, None, str] = UNSET
    content_type: Union[Unset, None, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    request: Union[Unset, None, str] = UNSET
    response: Union[Unset, None, str] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_message: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        content_type = self.content_type
        url = self.url
        request = self.request
        response = self.response
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if url is not UNSET:
            field_dict["url"] = url
        if request is not UNSET:
            field_dict["request"] = request
        if response is not UNSET:
            field_dict["response"] = response
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        content_type = d.pop("contentType", UNSET)

        url = d.pop("url", UNSET)

        request = d.pop("request", UNSET)

        response = d.pop("response", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)

        status_message = d.pop("statusMessage", UNSET)

        external_provider_conversation = cls(
            title=title,
            content_type=content_type,
            url=url,
            request=request,
            response=response,
            status=status,
            status_message=status_message,
        )

        return external_provider_conversation
