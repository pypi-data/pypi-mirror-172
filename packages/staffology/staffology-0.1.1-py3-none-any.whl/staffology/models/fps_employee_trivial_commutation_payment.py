from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeTrivialCommutationPayment")


@attr.s(auto_attribs=True)
class FpsEmployeeTrivialCommutationPayment:
    """
    Attributes:
        type (Union[Unset, None, str]):
        value (Union[Unset, None, str]):
    """

    type: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        value = d.pop("value", UNSET)

        fps_employee_trivial_commutation_payment = cls(
            type=type,
            value=value,
        )

        return fps_employee_trivial_commutation_payment
