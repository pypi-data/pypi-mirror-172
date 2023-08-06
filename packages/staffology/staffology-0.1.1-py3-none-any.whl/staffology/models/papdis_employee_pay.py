from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeePay")


@attr.s(auto_attribs=True)
class PapdisEmployeePay:
    """
    Attributes:
        pensionable_earnings_amount (Union[Unset, float]): [readonly]
        total_gross_qualifying_earnings_amount (Union[Unset, float]): [readonly]
    """

    pensionable_earnings_amount: Union[Unset, float] = UNSET
    total_gross_qualifying_earnings_amount: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pensionable_earnings_amount = self.pensionable_earnings_amount
        total_gross_qualifying_earnings_amount = (
            self.total_gross_qualifying_earnings_amount
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pensionable_earnings_amount is not UNSET:
            field_dict["pensionableEarningsAmount"] = pensionable_earnings_amount
        if total_gross_qualifying_earnings_amount is not UNSET:
            field_dict[
                "totalGrossQualifyingEarningsAmount"
            ] = total_gross_qualifying_earnings_amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pensionable_earnings_amount = d.pop("pensionableEarningsAmount", UNSET)

        total_gross_qualifying_earnings_amount = d.pop(
            "totalGrossQualifyingEarningsAmount", UNSET
        )

        papdis_employee_pay = cls(
            pensionable_earnings_amount=pensionable_earnings_amount,
            total_gross_qualifying_earnings_amount=total_gross_qualifying_earnings_amount,
        )

        return papdis_employee_pay
