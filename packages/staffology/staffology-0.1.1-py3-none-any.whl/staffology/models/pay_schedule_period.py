import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.pay_schedule_period_event import PaySchedulePeriodEvent
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaySchedulePeriod")


@attr.s(auto_attribs=True)
class PaySchedulePeriod:
    """
    Attributes:
        pay_schedule_period_events (Union[Unset, None, List[PaySchedulePeriodEvent]]): [readonly] List of all the events
            in this PaySchedulePeriod
        period (Union[Unset, int]): [readonly] The Period number of the PaySchedulePeriod.
        start_date (Union[Unset, datetime.date]): [readonly] The start date of the PaySchedulePeriod
        end_date (Union[Unset, datetime.date]): [readonly] The end date of the PaySchedulePeriod
        payment_date (Union[Unset, datetime.date]): The payment date of the PaySchedulePeriod.
        unadjusted_payment_date (Union[Unset, datetime.date]): The payment date of the PaySchedulePeriod when not
            accounting for weekends, bank hols or ad-hoc alterations to the pay schedule
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    pay_schedule_period_events: Union[Unset, None, List[PaySchedulePeriodEvent]] = UNSET
    period: Union[Unset, int] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET
    unadjusted_payment_date: Union[Unset, datetime.date] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_schedule_period_events: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pay_schedule_period_events, Unset):
            if self.pay_schedule_period_events is None:
                pay_schedule_period_events = None
            else:
                pay_schedule_period_events = []
                for (
                    pay_schedule_period_events_item_data
                ) in self.pay_schedule_period_events:
                    pay_schedule_period_events_item = (
                        pay_schedule_period_events_item_data.to_dict()
                    )

                    pay_schedule_period_events.append(pay_schedule_period_events_item)

        period = self.period
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()

        unadjusted_payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.unadjusted_payment_date, Unset):
            unadjusted_payment_date = self.unadjusted_payment_date.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_schedule_period_events is not UNSET:
            field_dict["paySchedulePeriodEvents"] = pay_schedule_period_events
        if period is not UNSET:
            field_dict["period"] = period
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if unadjusted_payment_date is not UNSET:
            field_dict["unadjustedPaymentDate"] = unadjusted_payment_date
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_schedule_period_events = []
        _pay_schedule_period_events = d.pop("paySchedulePeriodEvents", UNSET)
        for pay_schedule_period_events_item_data in _pay_schedule_period_events or []:
            pay_schedule_period_events_item = PaySchedulePeriodEvent.from_dict(
                pay_schedule_period_events_item_data
            )

            pay_schedule_period_events.append(pay_schedule_period_events_item)

        period = d.pop("period", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.date]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

        _unadjusted_payment_date = d.pop("unadjustedPaymentDate", UNSET)
        unadjusted_payment_date: Union[Unset, datetime.date]
        if isinstance(_unadjusted_payment_date, Unset):
            unadjusted_payment_date = UNSET
        else:
            unadjusted_payment_date = isoparse(_unadjusted_payment_date).date()

        id = d.pop("id", UNSET)

        pay_schedule_period = cls(
            pay_schedule_period_events=pay_schedule_period_events,
            period=period,
            start_date=start_date,
            end_date=end_date,
            payment_date=payment_date,
            unadjusted_payment_date=unadjusted_payment_date,
            id=id,
        )

        return pay_schedule_period
