from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_code import PayCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="FullSummaryOfPayReportLine")


@attr.s(auto_attribs=True)
class FullSummaryOfPayReportLine:
    """
    Attributes:
        pay_code (Union[Unset, PayCode]): Each PayLine has a Code. The Code will match the Code property of a PayCode.
            The PayCode that is used determines how the amount is treated with regards to tax, NI and pensions
        value (Union[Unset, float]):
        er_value (Union[Unset, None, float]):
        qty (Union[Unset, None, float]):
        head_count (Union[Unset, int]):
    """

    pay_code: Union[Unset, PayCode] = UNSET
    value: Union[Unset, float] = UNSET
    er_value: Union[Unset, None, float] = UNSET
    qty: Union[Unset, None, float] = UNSET
    head_count: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_code: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_code, Unset):
            pay_code = self.pay_code.to_dict()

        value = self.value
        er_value = self.er_value
        qty = self.qty
        head_count = self.head_count

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if value is not UNSET:
            field_dict["value"] = value
        if er_value is not UNSET:
            field_dict["erValue"] = er_value
        if qty is not UNSET:
            field_dict["qty"] = qty
        if head_count is not UNSET:
            field_dict["headCount"] = head_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _pay_code = d.pop("payCode", UNSET)
        pay_code: Union[Unset, PayCode]
        if isinstance(_pay_code, Unset):
            pay_code = UNSET
        else:
            pay_code = PayCode.from_dict(_pay_code)

        value = d.pop("value", UNSET)

        er_value = d.pop("erValue", UNSET)

        qty = d.pop("qty", UNSET)

        head_count = d.pop("headCount", UNSET)

        full_summary_of_pay_report_line = cls(
            pay_code=pay_code,
            value=value,
            er_value=er_value,
            qty=qty,
            head_count=head_count,
        )

        return full_summary_of_pay_report_line
