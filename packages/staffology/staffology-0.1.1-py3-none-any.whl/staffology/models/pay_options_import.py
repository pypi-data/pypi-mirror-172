from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.pay_basis import PayBasis
from ..models.pay_line import PayLine
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayOptionsImport")


@attr.s(auto_attribs=True)
class PayOptionsImport:
    """This object is used to import payment information for a payrun entry

    Attributes:
        employer_identifier (Union[Unset, None, str]): Optional. But if one entry has it then all must.
            Allows you to import to multiple employers by specifying the Employers AlternativeIdentifier
        payroll_code (Union[Unset, None, str]): The payroll code of the employee to update
        pay_amount (Union[Unset, float]): The amount the Employee is regularly paid each period
        basis (Union[Unset, PayBasis]):
        pay_code (Union[Unset, None, str]): If you want to override the PayCode used for the Basic Pay then set the code
            here, otherwise leave this blank and the default will be used.
        pay_amount_multiplier (Union[Unset, float]): This property is irrelevant if the basis is Monthly.
            But if the basis is Daily or Hourly then this property sets how many days/hours the employee should be paid for
            in the period.
        note (Union[Unset, None, str]): Any note that you'd like to appear on the payslip
        tags (Union[Unset, None, List[str]]):
        lines (Union[Unset, None, List[PayLine]]):
    """

    employer_identifier: Union[Unset, None, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    pay_amount: Union[Unset, float] = UNSET
    basis: Union[Unset, PayBasis] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    pay_amount_multiplier: Union[Unset, float] = UNSET
    note: Union[Unset, None, str] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    lines: Union[Unset, None, List[PayLine]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer_identifier = self.employer_identifier
        payroll_code = self.payroll_code
        pay_amount = self.pay_amount
        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        pay_code = self.pay_code
        pay_amount_multiplier = self.pay_amount_multiplier
        note = self.note
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer_identifier is not UNSET:
            field_dict["employerIdentifier"] = employer_identifier
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if pay_amount is not UNSET:
            field_dict["payAmount"] = pay_amount
        if basis is not UNSET:
            field_dict["basis"] = basis
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if pay_amount_multiplier is not UNSET:
            field_dict["payAmountMultiplier"] = pay_amount_multiplier
        if note is not UNSET:
            field_dict["note"] = note
        if tags is not UNSET:
            field_dict["tags"] = tags
        if lines is not UNSET:
            field_dict["lines"] = lines

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_identifier = d.pop("employerIdentifier", UNSET)

        payroll_code = d.pop("payrollCode", UNSET)

        pay_amount = d.pop("payAmount", UNSET)

        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, PayBasis]
        if isinstance(_basis, Unset):
            basis = UNSET
        else:
            basis = PayBasis(_basis)

        pay_code = d.pop("payCode", UNSET)

        pay_amount_multiplier = d.pop("payAmountMultiplier", UNSET)

        note = d.pop("note", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = PayLine.from_dict(lines_item_data)

            lines.append(lines_item)

        pay_options_import = cls(
            employer_identifier=employer_identifier,
            payroll_code=payroll_code,
            pay_amount=pay_amount,
            basis=basis,
            pay_code=pay_code,
            pay_amount_multiplier=pay_amount_multiplier,
            note=note,
            tags=tags,
            lines=lines,
        )

        return pay_options_import
