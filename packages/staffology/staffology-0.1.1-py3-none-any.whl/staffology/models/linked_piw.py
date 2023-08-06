import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.linked_piw_result import LinkedPiwResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkedPiw")


@attr.s(auto_attribs=True)
class LinkedPiw:
    """Linked Period of Incapacity for Work.
    If you record Sick Leave and select Statutory Pay then any other Sick Leave with Statutory Pay
    lasting 4 or more days in the previous 8 weeks will be linked to it

        Attributes:
            result (Union[Unset, LinkedPiwResult]):
            id (Union[Unset, str]): [readonly] The Id of the linked Leave
            average_weekly_earnings (Union[Unset, float]): [readonly] Average weekly earnings from linked Leave
            working_days (Union[Unset, float]): [readonly] The number of working days in the linked Leave.
            total_days (Union[Unset, float]): [readonly] The number of days covered by the linked Leave.
            ssp_first_pay_day (Union[Unset, None, datetime.date]): [readonly] The SspFirstPayDay from the linked Leave, if
                set
            ssp_first_day (Union[Unset, None, datetime.date]): [readonly] The SspFirstDay from the linked Leave, if set
    """

    result: Union[Unset, LinkedPiwResult] = UNSET
    id: Union[Unset, str] = UNSET
    average_weekly_earnings: Union[Unset, float] = UNSET
    working_days: Union[Unset, float] = UNSET
    total_days: Union[Unset, float] = UNSET
    ssp_first_pay_day: Union[Unset, None, datetime.date] = UNSET
    ssp_first_day: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        result: Union[Unset, str] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.value

        id = self.id
        average_weekly_earnings = self.average_weekly_earnings
        working_days = self.working_days
        total_days = self.total_days
        ssp_first_pay_day: Union[Unset, None, str] = UNSET
        if not isinstance(self.ssp_first_pay_day, Unset):
            ssp_first_pay_day = (
                self.ssp_first_pay_day.isoformat() if self.ssp_first_pay_day else None
            )

        ssp_first_day: Union[Unset, None, str] = UNSET
        if not isinstance(self.ssp_first_day, Unset):
            ssp_first_day = (
                self.ssp_first_day.isoformat() if self.ssp_first_day else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if result is not UNSET:
            field_dict["result"] = result
        if id is not UNSET:
            field_dict["id"] = id
        if average_weekly_earnings is not UNSET:
            field_dict["averageWeeklyEarnings"] = average_weekly_earnings
        if working_days is not UNSET:
            field_dict["workingDays"] = working_days
        if total_days is not UNSET:
            field_dict["totalDays"] = total_days
        if ssp_first_pay_day is not UNSET:
            field_dict["sspFirstPayDay"] = ssp_first_pay_day
        if ssp_first_day is not UNSET:
            field_dict["sspFirstDay"] = ssp_first_day

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _result = d.pop("result", UNSET)
        result: Union[Unset, LinkedPiwResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = LinkedPiwResult(_result)

        id = d.pop("id", UNSET)

        average_weekly_earnings = d.pop("averageWeeklyEarnings", UNSET)

        working_days = d.pop("workingDays", UNSET)

        total_days = d.pop("totalDays", UNSET)

        _ssp_first_pay_day = d.pop("sspFirstPayDay", UNSET)
        ssp_first_pay_day: Union[Unset, None, datetime.date]
        if _ssp_first_pay_day is None:
            ssp_first_pay_day = None
        elif isinstance(_ssp_first_pay_day, Unset):
            ssp_first_pay_day = UNSET
        else:
            ssp_first_pay_day = isoparse(_ssp_first_pay_day).date()

        _ssp_first_day = d.pop("sspFirstDay", UNSET)
        ssp_first_day: Union[Unset, None, datetime.date]
        if _ssp_first_day is None:
            ssp_first_day = None
        elif isinstance(_ssp_first_day, Unset):
            ssp_first_day = UNSET
        else:
            ssp_first_day = isoparse(_ssp_first_day).date()

        linked_piw = cls(
            result=result,
            id=id,
            average_weekly_earnings=average_weekly_earnings,
            working_days=working_days,
            total_days=total_days,
            ssp_first_pay_day=ssp_first_pay_day,
            ssp_first_day=ssp_first_day,
        )

        return linked_piw
