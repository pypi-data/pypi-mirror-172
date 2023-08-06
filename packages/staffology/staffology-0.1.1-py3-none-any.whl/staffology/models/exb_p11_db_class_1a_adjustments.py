from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.exb_p11_db_class_1a_adjustment import ExbP11DbClass1AAdjustment
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11DbClass1AAdjustments")


@attr.s(auto_attribs=True)
class ExbP11DbClass1AAdjustments:
    """
    Attributes:
        total_benefit (Union[Unset, None, str]):
        amount_due (Union[Unset, ExbP11DbClass1AAdjustment]):
        amount_not_due (Union[Unset, ExbP11DbClass1AAdjustment]):
        total (Union[Unset, None, str]):
        payable (Union[Unset, None, str]):
    """

    total_benefit: Union[Unset, None, str] = UNSET
    amount_due: Union[Unset, ExbP11DbClass1AAdjustment] = UNSET
    amount_not_due: Union[Unset, ExbP11DbClass1AAdjustment] = UNSET
    total: Union[Unset, None, str] = UNSET
    payable: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        total_benefit = self.total_benefit
        amount_due: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.amount_due, Unset):
            amount_due = self.amount_due.to_dict()

        amount_not_due: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.amount_not_due, Unset):
            amount_not_due = self.amount_not_due.to_dict()

        total = self.total
        payable = self.payable

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if total_benefit is not UNSET:
            field_dict["totalBenefit"] = total_benefit
        if amount_due is not UNSET:
            field_dict["amountDue"] = amount_due
        if amount_not_due is not UNSET:
            field_dict["amountNotDue"] = amount_not_due
        if total is not UNSET:
            field_dict["total"] = total
        if payable is not UNSET:
            field_dict["payable"] = payable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_benefit = d.pop("totalBenefit", UNSET)

        _amount_due = d.pop("amountDue", UNSET)
        amount_due: Union[Unset, ExbP11DbClass1AAdjustment]
        if isinstance(_amount_due, Unset):
            amount_due = UNSET
        else:
            amount_due = ExbP11DbClass1AAdjustment.from_dict(_amount_due)

        _amount_not_due = d.pop("amountNotDue", UNSET)
        amount_not_due: Union[Unset, ExbP11DbClass1AAdjustment]
        if isinstance(_amount_not_due, Unset):
            amount_not_due = UNSET
        else:
            amount_not_due = ExbP11DbClass1AAdjustment.from_dict(_amount_not_due)

        total = d.pop("total", UNSET)

        payable = d.pop("payable", UNSET)

        exb_p11_db_class_1a_adjustments = cls(
            total_benefit=total_benefit,
            amount_due=amount_due,
            amount_not_due=amount_not_due,
            total=total,
            payable=payable,
        )

        return exb_p11_db_class_1a_adjustments
