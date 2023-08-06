from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FixedCode")


@attr.s(auto_attribs=True)
class FixedCode:
    """Part of the TaxYearConfig that our engine uses to enable calculation of Tax and NI.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            code (Union[Unset, None, str]): [readonly]
            rate (Union[Unset, float]): [readonly]
    """

    code: Union[Unset, None, str] = UNSET
    rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        rate = self.rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if rate is not UNSET:
            field_dict["rate"] = rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        rate = d.pop("rate", UNSET)

        fixed_code = cls(
            code=code,
            rate=rate,
        )

        return fixed_code
