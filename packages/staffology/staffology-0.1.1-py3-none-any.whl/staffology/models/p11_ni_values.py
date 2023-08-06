from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11NiValues")


@attr.s(auto_attribs=True)
class P11NiValues:
    """Forms a part of the P11 report.

    Attributes:
        table (Union[Unset, None, str]): [readonly]
        period (Union[Unset, float]): [readonly]
        ytd (Union[Unset, float]): [readonly]
    """

    table: Union[Unset, None, str] = UNSET
    period: Union[Unset, float] = UNSET
    ytd: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        table = self.table
        period = self.period
        ytd = self.ytd

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if table is not UNSET:
            field_dict["table"] = table
        if period is not UNSET:
            field_dict["period"] = period
        if ytd is not UNSET:
            field_dict["ytd"] = ytd

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table = d.pop("table", UNSET)

        period = d.pop("period", UNSET)

        ytd = d.pop("ytd", UNSET)

        p11_ni_values = cls(
            table=table,
            period=period,
            ytd=ytd,
        )

        return p11_ni_values
