from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.exb_p11_db_class_1a_adjustments import ExbP11DbClass1AAdjustments
from ..models.exb_p11_db_class_1a_total_benefit import ExbP11DbClass1ATotalBenefit
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11DbClass1A")


@attr.s(auto_attribs=True)
class ExbP11DbClass1A:
    """
    Attributes:
        ni_cs_rate (Union[Unset, None, str]):
        total_benefit (Union[Unset, ExbP11DbClass1ATotalBenefit]):
        adjustments (Union[Unset, ExbP11DbClass1AAdjustments]):
        ni_cpayable (Union[Unset, None, str]):
    """

    ni_cs_rate: Union[Unset, None, str] = UNSET
    total_benefit: Union[Unset, ExbP11DbClass1ATotalBenefit] = UNSET
    adjustments: Union[Unset, ExbP11DbClass1AAdjustments] = UNSET
    ni_cpayable: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ni_cs_rate = self.ni_cs_rate
        total_benefit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.total_benefit, Unset):
            total_benefit = self.total_benefit.to_dict()

        adjustments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.adjustments, Unset):
            adjustments = self.adjustments.to_dict()

        ni_cpayable = self.ni_cpayable

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ni_cs_rate is not UNSET:
            field_dict["niCsRate"] = ni_cs_rate
        if total_benefit is not UNSET:
            field_dict["totalBenefit"] = total_benefit
        if adjustments is not UNSET:
            field_dict["adjustments"] = adjustments
        if ni_cpayable is not UNSET:
            field_dict["niCpayable"] = ni_cpayable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ni_cs_rate = d.pop("niCsRate", UNSET)

        _total_benefit = d.pop("totalBenefit", UNSET)
        total_benefit: Union[Unset, ExbP11DbClass1ATotalBenefit]
        if isinstance(_total_benefit, Unset):
            total_benefit = UNSET
        else:
            total_benefit = ExbP11DbClass1ATotalBenefit.from_dict(_total_benefit)

        _adjustments = d.pop("adjustments", UNSET)
        adjustments: Union[Unset, ExbP11DbClass1AAdjustments]
        if isinstance(_adjustments, Unset):
            adjustments = UNSET
        else:
            adjustments = ExbP11DbClass1AAdjustments.from_dict(_adjustments)

        ni_cpayable = d.pop("niCpayable", UNSET)

        exb_p11_db_class_1a = cls(
            ni_cs_rate=ni_cs_rate,
            total_benefit=total_benefit,
            adjustments=adjustments,
            ni_cpayable=ni_cpayable,
        )

        return exb_p11_db_class_1a
