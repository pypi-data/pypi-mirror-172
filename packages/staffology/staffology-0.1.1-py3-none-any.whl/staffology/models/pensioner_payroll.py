from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionerPayroll")


@attr.s(auto_attribs=True)
class PensionerPayroll:
    """
    Attributes:
        in_receipt_of_pension (Union[Unset, bool]): If set to true then the FPS will have the OccPenInd flag set to
            'yes'
        bereaved (Union[Unset, bool]): Indicator that Occupational Pension is being paid because they are a recently
            bereaved Spouse/Civil Partner
        amount (Union[Unset, float]): Annual amount of occupational pension
    """

    in_receipt_of_pension: Union[Unset, bool] = UNSET
    bereaved: Union[Unset, bool] = UNSET
    amount: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        in_receipt_of_pension = self.in_receipt_of_pension
        bereaved = self.bereaved
        amount = self.amount

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if in_receipt_of_pension is not UNSET:
            field_dict["inReceiptOfPension"] = in_receipt_of_pension
        if bereaved is not UNSET:
            field_dict["bereaved"] = bereaved
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        in_receipt_of_pension = d.pop("inReceiptOfPension", UNSET)

        bereaved = d.pop("bereaved", UNSET)

        amount = d.pop("amount", UNSET)

        pensioner_payroll = cls(
            in_receipt_of_pension=in_receipt_of_pension,
            bereaved=bereaved,
            amount=amount,
        )

        return pensioner_payroll
