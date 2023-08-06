from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaxCodeChange")


@attr.s(auto_attribs=True)
class TaxCodeChange:
    """Part of the TaxYearConfig that our engine uses to perform the Year End routine.
    It is used internally when our engine performs the Year End routine.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            suffix (Union[Unset, None, str]): [readonly] The suffix of the Tax Code that needs to be incremented for this
                Tax Year
            increment (Union[Unset, int]): [readonly] The amount by which to increment Tax Codes with the given suffix
    """

    suffix: Union[Unset, None, str] = UNSET
    increment: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        suffix = self.suffix
        increment = self.increment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if increment is not UNSET:
            field_dict["increment"] = increment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        suffix = d.pop("suffix", UNSET)

        increment = d.pop("increment", UNSET)

        tax_code_change = cls(
            suffix=suffix,
            increment=increment,
        )

        return tax_code_change
