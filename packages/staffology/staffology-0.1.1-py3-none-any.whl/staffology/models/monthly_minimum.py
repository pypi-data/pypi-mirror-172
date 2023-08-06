import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MonthlyMinimum")


@attr.s(auto_attribs=True)
class MonthlyMinimum:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        amount (Union[Unset, float]):
        start_date (Union[Unset, None, datetime.date]):
        end_date (Union[Unset, None, datetime.date]):
        bill_past_end_date (Union[Unset, bool]): If set to true then this user should still be billed even after the End
            Date
    """

    enabled: Union[Unset, bool] = UNSET
    amount: Union[Unset, float] = UNSET
    start_date: Union[Unset, None, datetime.date] = UNSET
    end_date: Union[Unset, None, datetime.date] = UNSET
    bill_past_end_date: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        amount = self.amount
        start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat() if self.start_date else None

        end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat() if self.end_date else None

        bill_past_end_date = self.bill_past_end_date

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if amount is not UNSET:
            field_dict["amount"] = amount
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if bill_past_end_date is not UNSET:
            field_dict["billPastEndDate"] = bill_past_end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        amount = d.pop("amount", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, None, datetime.date]
        if _start_date is None:
            start_date = None
        elif isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, None, datetime.date]
        if _end_date is None:
            end_date = None
        elif isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()

        bill_past_end_date = d.pop("billPastEndDate", UNSET)

        monthly_minimum = cls(
            enabled=enabled,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            bill_past_end_date=bill_past_end_date,
        )

        return monthly_minimum
