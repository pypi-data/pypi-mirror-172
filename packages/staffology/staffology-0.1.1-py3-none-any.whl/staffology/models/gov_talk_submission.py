import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.gov_talk_error import GovTalkError
from ..models.submission_status import SubmissionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="GovTalkSubmission")


@attr.s(auto_attribs=True)
class GovTalkSubmission:
    """
    Attributes:
        raw_response (Union[Unset, None, str]):
        message_class (Union[Unset, None, str]):
        poll_interval (Union[Unset, int]):
        last_poll (Union[Unset, None, datetime.datetime]):
        correlation_id (Union[Unset, None, str]):
        url (Union[Unset, None, str]):
        status (Union[Unset, SubmissionStatus]):
        message (Union[Unset, None, str]):
        i_rmark (Union[Unset, None, str]):
        errors_json (Union[Unset, None, str]):
        errors (Union[Unset, None, List[GovTalkError]]):
        submitted_at (Union[Unset, None, datetime.datetime]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    raw_response: Union[Unset, None, str] = UNSET
    message_class: Union[Unset, None, str] = UNSET
    poll_interval: Union[Unset, int] = UNSET
    last_poll: Union[Unset, None, datetime.datetime] = UNSET
    correlation_id: Union[Unset, None, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    status: Union[Unset, SubmissionStatus] = UNSET
    message: Union[Unset, None, str] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    errors_json: Union[Unset, None, str] = UNSET
    errors: Union[Unset, None, List[GovTalkError]] = UNSET
    submitted_at: Union[Unset, None, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        raw_response = self.raw_response
        message_class = self.message_class
        poll_interval = self.poll_interval
        last_poll: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_poll, Unset):
            last_poll = self.last_poll.isoformat() if self.last_poll else None

        correlation_id = self.correlation_id
        url = self.url
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        message = self.message
        i_rmark = self.i_rmark
        errors_json = self.errors_json
        errors: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            if self.errors is None:
                errors = None
            else:
                errors = []
                for errors_item_data in self.errors:
                    errors_item = errors_item_data.to_dict()

                    errors.append(errors_item)

        submitted_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.submitted_at, Unset):
            submitted_at = self.submitted_at.isoformat() if self.submitted_at else None

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if raw_response is not UNSET:
            field_dict["rawResponse"] = raw_response
        if message_class is not UNSET:
            field_dict["messageClass"] = message_class
        if poll_interval is not UNSET:
            field_dict["pollInterval"] = poll_interval
        if last_poll is not UNSET:
            field_dict["lastPoll"] = last_poll
        if correlation_id is not UNSET:
            field_dict["correlationId"] = correlation_id
        if url is not UNSET:
            field_dict["url"] = url
        if status is not UNSET:
            field_dict["status"] = status
        if message is not UNSET:
            field_dict["message"] = message
        if i_rmark is not UNSET:
            field_dict["iRmark"] = i_rmark
        if errors_json is not UNSET:
            field_dict["errorsJson"] = errors_json
        if errors is not UNSET:
            field_dict["errors"] = errors
        if submitted_at is not UNSET:
            field_dict["submittedAt"] = submitted_at
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        raw_response = d.pop("rawResponse", UNSET)

        message_class = d.pop("messageClass", UNSET)

        poll_interval = d.pop("pollInterval", UNSET)

        _last_poll = d.pop("lastPoll", UNSET)
        last_poll: Union[Unset, None, datetime.datetime]
        if _last_poll is None:
            last_poll = None
        elif isinstance(_last_poll, Unset):
            last_poll = UNSET
        else:
            last_poll = isoparse(_last_poll)

        correlation_id = d.pop("correlationId", UNSET)

        url = d.pop("url", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SubmissionStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SubmissionStatus(_status)

        message = d.pop("message", UNSET)

        i_rmark = d.pop("iRmark", UNSET)

        errors_json = d.pop("errorsJson", UNSET)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = GovTalkError.from_dict(errors_item_data)

            errors.append(errors_item)

        _submitted_at = d.pop("submittedAt", UNSET)
        submitted_at: Union[Unset, None, datetime.datetime]
        if _submitted_at is None:
            submitted_at = None
        elif isinstance(_submitted_at, Unset):
            submitted_at = UNSET
        else:
            submitted_at = isoparse(_submitted_at)

        id = d.pop("id", UNSET)

        gov_talk_submission = cls(
            raw_response=raw_response,
            message_class=message_class,
            poll_interval=poll_interval,
            last_poll=last_poll,
            correlation_id=correlation_id,
            url=url,
            status=status,
            message=message,
            i_rmark=i_rmark,
            errors_json=errors_json,
            errors=errors,
            submitted_at=submitted_at,
            id=id,
        )

        return gov_talk_submission
