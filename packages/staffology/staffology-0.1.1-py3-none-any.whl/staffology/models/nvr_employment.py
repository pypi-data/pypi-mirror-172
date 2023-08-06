from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NvrEmployment")


@attr.s(auto_attribs=True)
class NvrEmployment:
    """
    Attributes:
        pay_id (Union[Unset, None, str]):
    """

    pay_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_id = self.pay_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_id is not UNSET:
            field_dict["payId"] = pay_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_id = d.pop("payId", UNSET)

        nvr_employment = cls(
            pay_id=pay_id,
        )

        return nvr_employment
