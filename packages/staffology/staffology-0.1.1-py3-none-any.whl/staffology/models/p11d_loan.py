from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DLoan")


@attr.s(auto_attribs=True)
class P11DLoan:
    """
    Attributes:
        joint (Union[Unset, None, str]):
        init_os (Union[Unset, None, str]):
        final_os (Union[Unset, None, str]):
        max_os (Union[Unset, None, str]):
        int_paid (Union[Unset, None, str]):
        date (Union[Unset, None, str]):
        discharge (Union[Unset, None, str]):
        cash_equiv_or_relevant_amt (Union[Unset, None, str]):
    """

    joint: Union[Unset, None, str] = UNSET
    init_os: Union[Unset, None, str] = UNSET
    final_os: Union[Unset, None, str] = UNSET
    max_os: Union[Unset, None, str] = UNSET
    int_paid: Union[Unset, None, str] = UNSET
    date: Union[Unset, None, str] = UNSET
    discharge: Union[Unset, None, str] = UNSET
    cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        joint = self.joint
        init_os = self.init_os
        final_os = self.final_os
        max_os = self.max_os
        int_paid = self.int_paid
        date = self.date
        discharge = self.discharge
        cash_equiv_or_relevant_amt = self.cash_equiv_or_relevant_amt

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if joint is not UNSET:
            field_dict["joint"] = joint
        if init_os is not UNSET:
            field_dict["initOS"] = init_os
        if final_os is not UNSET:
            field_dict["finalOS"] = final_os
        if max_os is not UNSET:
            field_dict["maxOS"] = max_os
        if int_paid is not UNSET:
            field_dict["intPaid"] = int_paid
        if date is not UNSET:
            field_dict["date"] = date
        if discharge is not UNSET:
            field_dict["discharge"] = discharge
        if cash_equiv_or_relevant_amt is not UNSET:
            field_dict["cashEquivOrRelevantAmt"] = cash_equiv_or_relevant_amt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        joint = d.pop("joint", UNSET)

        init_os = d.pop("initOS", UNSET)

        final_os = d.pop("finalOS", UNSET)

        max_os = d.pop("maxOS", UNSET)

        int_paid = d.pop("intPaid", UNSET)

        date = d.pop("date", UNSET)

        discharge = d.pop("discharge", UNSET)

        cash_equiv_or_relevant_amt = d.pop("cashEquivOrRelevantAmt", UNSET)

        p11d_loan = cls(
            joint=joint,
            init_os=init_os,
            final_os=final_os,
            max_os=max_os,
            int_paid=int_paid,
            date=date,
            discharge=discharge,
            cash_equiv_or_relevant_amt=cash_equiv_or_relevant_amt,
        )

        return p11d_loan
