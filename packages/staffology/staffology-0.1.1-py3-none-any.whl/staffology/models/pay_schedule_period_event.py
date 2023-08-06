import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.pay_period_event_type import PayPeriodEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaySchedulePeriodEvent")


@attr.s(auto_attribs=True)
class PaySchedulePeriodEvent:
    """An Event within a PaySchedulePeriod. The event could be scheduled x days before PaymentDate.

    Attributes:
        pay_period_event_type (Union[Unset, PayPeriodEventType]): Different events supported for a PaySchedule Period.
            These events happen a pre-configured number of days before the PaymentDate for that PaySchedulePeriod.
        event_date (Union[Unset, datetime.date]): The expected date and time of the event.
        actual_event_date (Union[Unset, None, datetime.date]): The actual date and time when the event was completed.
        is_over_due (Union[Unset, bool]): Returns true if its past the event date.
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    pay_period_event_type: Union[Unset, PayPeriodEventType] = UNSET
    event_date: Union[Unset, datetime.date] = UNSET
    actual_event_date: Union[Unset, None, datetime.date] = UNSET
    is_over_due: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_period_event_type: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period_event_type, Unset):
            pay_period_event_type = self.pay_period_event_type.value

        event_date: Union[Unset, str] = UNSET
        if not isinstance(self.event_date, Unset):
            event_date = self.event_date.isoformat()

        actual_event_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.actual_event_date, Unset):
            actual_event_date = (
                self.actual_event_date.isoformat() if self.actual_event_date else None
            )

        is_over_due = self.is_over_due
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_period_event_type is not UNSET:
            field_dict["payPeriodEventType"] = pay_period_event_type
        if event_date is not UNSET:
            field_dict["eventDate"] = event_date
        if actual_event_date is not UNSET:
            field_dict["actualEventDate"] = actual_event_date
        if is_over_due is not UNSET:
            field_dict["isOverDue"] = is_over_due
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _pay_period_event_type = d.pop("payPeriodEventType", UNSET)
        pay_period_event_type: Union[Unset, PayPeriodEventType]
        if isinstance(_pay_period_event_type, Unset):
            pay_period_event_type = UNSET
        else:
            pay_period_event_type = PayPeriodEventType(_pay_period_event_type)

        _event_date = d.pop("eventDate", UNSET)
        event_date: Union[Unset, datetime.date]
        if isinstance(_event_date, Unset):
            event_date = UNSET
        else:
            event_date = isoparse(_event_date).date()

        _actual_event_date = d.pop("actualEventDate", UNSET)
        actual_event_date: Union[Unset, None, datetime.date]
        if _actual_event_date is None:
            actual_event_date = None
        elif isinstance(_actual_event_date, Unset):
            actual_event_date = UNSET
        else:
            actual_event_date = isoparse(_actual_event_date).date()

        is_over_due = d.pop("isOverDue", UNSET)

        id = d.pop("id", UNSET)

        pay_schedule_period_event = cls(
            pay_period_event_type=pay_period_event_type,
            event_date=event_date,
            actual_event_date=actual_event_date,
            is_over_due=is_over_due,
            id=id,
        )

        return pay_schedule_period_event
