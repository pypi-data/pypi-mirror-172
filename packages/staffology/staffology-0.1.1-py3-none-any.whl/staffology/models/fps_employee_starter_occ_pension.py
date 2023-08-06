from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeStarterOccPension")


@attr.s(auto_attribs=True)
class FpsEmployeeStarterOccPension:
    """
    Attributes:
        bereaved (Union[Unset, None, str]):
        amount (Union[Unset, None, str]):
    """

    bereaved: Union[Unset, None, str] = UNSET
    amount: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bereaved = self.bereaved
        amount = self.amount

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bereaved is not UNSET:
            field_dict["bereaved"] = bereaved
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bereaved = d.pop("bereaved", UNSET)

        amount = d.pop("amount", UNSET)

        fps_employee_starter_occ_pension = cls(
            bereaved=bereaved,
            amount=amount,
        )

        return fps_employee_starter_occ_pension
