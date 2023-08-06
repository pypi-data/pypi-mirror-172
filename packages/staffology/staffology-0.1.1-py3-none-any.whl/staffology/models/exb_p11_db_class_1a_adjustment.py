from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11DbClass1AAdjustment")


@attr.s(auto_attribs=True)
class ExbP11DbClass1AAdjustment:
    """
    Attributes:
        description (Union[Unset, None, str]):
        adjustment (Union[Unset, None, str]):
    """

    description: Union[Unset, None, str] = UNSET
    adjustment: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        adjustment = self.adjustment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if adjustment is not UNSET:
            field_dict["adjustment"] = adjustment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        adjustment = d.pop("adjustment", UNSET)

        exb_p11_db_class_1a_adjustment = cls(
            description=description,
            adjustment=adjustment,
        )

        return exb_p11_db_class_1a_adjustment
