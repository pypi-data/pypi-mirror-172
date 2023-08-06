from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.payroll_value_type import PayrollValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="YtdValue")


@attr.s(auto_attribs=True)
class YtdValue:
    """
    Attributes:
        type (Union[Unset, PayrollValueType]):
        brought_forward (Union[Unset, float]):
        period (Union[Unset, float]):
        value (Union[Unset, float]):
    """

    type: Union[Unset, PayrollValueType] = UNSET
    brought_forward: Union[Unset, float] = UNSET
    period: Union[Unset, float] = UNSET
    value: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        brought_forward = self.brought_forward
        period = self.period
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if brought_forward is not UNSET:
            field_dict["broughtForward"] = brought_forward
        if period is not UNSET:
            field_dict["period"] = period
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PayrollValueType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PayrollValueType(_type)

        brought_forward = d.pop("broughtForward", UNSET)

        period = d.pop("period", UNSET)

        value = d.pop("value", UNSET)

        ytd_value = cls(
            type=type,
            brought_forward=brought_forward,
            period=period,
            value=value,
        )

        return ytd_value
