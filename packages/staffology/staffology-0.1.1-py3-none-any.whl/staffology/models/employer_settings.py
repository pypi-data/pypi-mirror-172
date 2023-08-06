from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerSettings")


@attr.s(auto_attribs=True)
class EmployerSettings:
    """Miscellaneous settings related to the employer that don't naturally belong in other models

    Attributes:
        allow_negative_pay (Union[Unset, bool]):
    """

    allow_negative_pay: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        allow_negative_pay = self.allow_negative_pay

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if allow_negative_pay is not UNSET:
            field_dict["allowNegativePay"] = allow_negative_pay

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allow_negative_pay = d.pop("allowNegativePay", UNSET)

        employer_settings = cls(
            allow_negative_pay=allow_negative_pay,
        )

        return employer_settings
