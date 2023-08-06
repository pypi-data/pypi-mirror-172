from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaxBracket")


@attr.s(auto_attribs=True)
class TaxBracket:
    """
    Attributes:
        from_ (Union[Unset, float]): [readonly] The starting point for applying this tax rate
        to (Union[Unset, float]): [readonly] The end point for applying this tax rate
        multiplier (Union[Unset, float]): [readonly] The tax rate to apply
    """

    from_: Union[Unset, float] = UNSET
    to: Union[Unset, float] = UNSET
    multiplier: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_
        to = self.to
        multiplier = self.multiplier

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if multiplier is not UNSET:
            field_dict["multiplier"] = multiplier

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = d.pop("from", UNSET)

        to = d.pop("to", UNSET)

        multiplier = d.pop("multiplier", UNSET)

        tax_bracket = cls(
            from_=from_,
            to=to,
            multiplier=multiplier,
        )

        return tax_bracket
