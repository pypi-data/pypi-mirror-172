import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="HmrcPayment")


@attr.s(auto_attribs=True)
class HmrcPayment:
    """
    Attributes:
        amount (Union[Unset, float]):
        date (Union[Unset, datetime.date]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    amount: Union[Unset, float] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        amount = self.amount
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if date is not UNSET:
            field_dict["date"] = date
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        amount = d.pop("amount", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        id = d.pop("id", UNSET)

        hmrc_payment = cls(
            amount=amount,
            date=date,
            id=id,
        )

        return hmrc_payment
