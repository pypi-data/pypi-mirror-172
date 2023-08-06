from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisReportLineValue")


@attr.s(auto_attribs=True)
class AnalysisReportLineValue:
    """
    Attributes:
        qty (Union[Unset, None, float]):
        code (Union[Unset, None, str]):
        value (Union[Unset, float]):
    """

    qty: Union[Unset, None, float] = UNSET
    code: Union[Unset, None, str] = UNSET
    value: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        qty = self.qty
        code = self.code
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if qty is not UNSET:
            field_dict["qty"] = qty
        if code is not UNSET:
            field_dict["code"] = code
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        qty = d.pop("qty", UNSET)

        code = d.pop("code", UNSET)

        value = d.pop("value", UNSET)

        analysis_report_line_value = cls(
            qty=qty,
            code=code,
            value=value,
        )

        return analysis_report_line_value
