from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11DbClass1ATotalBenefit")


@attr.s(auto_attribs=True)
class ExbP11DbClass1ATotalBenefit:
    """
    Attributes:
        adjustment_required (Union[Unset, None, str]):
        value (Union[Unset, None, str]):
    """

    adjustment_required: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        adjustment_required = self.adjustment_required
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if adjustment_required is not UNSET:
            field_dict["adjustmentRequired"] = adjustment_required
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        adjustment_required = d.pop("adjustmentRequired", UNSET)

        value = d.pop("value", UNSET)

        exb_p11_db_class_1a_total_benefit = cls(
            adjustment_required=adjustment_required,
            value=value,
        )

        return exb_p11_db_class_1a_total_benefit
