import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LeaverDetails")


@attr.s(auto_attribs=True)
class LeaverDetails:
    """
    Attributes:
        has_left (Union[Unset, bool]):
        leave_date (Union[Unset, None, datetime.date]):
        is_deceased (Union[Unset, bool]):
        payment_after_leaving (Union[Unset, bool]):
        p_45_sent (Union[Unset, bool]):
    """

    has_left: Union[Unset, bool] = UNSET
    leave_date: Union[Unset, None, datetime.date] = UNSET
    is_deceased: Union[Unset, bool] = UNSET
    payment_after_leaving: Union[Unset, bool] = UNSET
    p_45_sent: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        has_left = self.has_left
        leave_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.leave_date, Unset):
            leave_date = self.leave_date.isoformat() if self.leave_date else None

        is_deceased = self.is_deceased
        payment_after_leaving = self.payment_after_leaving
        p_45_sent = self.p_45_sent

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if has_left is not UNSET:
            field_dict["hasLeft"] = has_left
        if leave_date is not UNSET:
            field_dict["leaveDate"] = leave_date
        if is_deceased is not UNSET:
            field_dict["isDeceased"] = is_deceased
        if payment_after_leaving is not UNSET:
            field_dict["paymentAfterLeaving"] = payment_after_leaving
        if p_45_sent is not UNSET:
            field_dict["p45Sent"] = p_45_sent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        has_left = d.pop("hasLeft", UNSET)

        _leave_date = d.pop("leaveDate", UNSET)
        leave_date: Union[Unset, None, datetime.date]
        if _leave_date is None:
            leave_date = None
        elif isinstance(_leave_date, Unset):
            leave_date = UNSET
        else:
            leave_date = isoparse(_leave_date).date()

        is_deceased = d.pop("isDeceased", UNSET)

        payment_after_leaving = d.pop("paymentAfterLeaving", UNSET)

        p_45_sent = d.pop("p45Sent", UNSET)

        leaver_details = cls(
            has_left=has_left,
            leave_date=leave_date,
            is_deceased=is_deceased,
            payment_after_leaving=payment_after_leaving,
            p_45_sent=p_45_sent,
        )

        return leaver_details
