from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..models.rti_employee_name import RtiEmployeeName
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisStatement")


@attr.s(auto_attribs=True)
class CisStatement:
    """CIS Payment and Deduction Statement (CISOL1)

    Attributes:
        tax_year (Union[Unset, TaxYear]):
        tax_month (Union[Unset, int]): [readonly]
        contractor_name (Union[Unset, None, str]): [readonly]
        contractor_address (Union[Unset, Address]):
        contractor_office_number (Union[Unset, None, str]): [readonly]
        contractor_paye_reference (Union[Unset, None, str]): [readonly]
        subcontractor_name (Union[Unset, RtiEmployeeName]):
        sub_contractor_utr (Union[Unset, None, str]): [readonly]
        verification_number (Union[Unset, None, str]): [readonly]
        gross_amount_paid (Union[Unset, float]): [readonly] Gross Amount Paid (Excl VAT)
        cost_of_materials (Union[Unset, float]): [readonly]
        amount_liable_to_deduction (Union[Unset, float]): [readonly]
        amount_deducted (Union[Unset, float]): [readonly]
        amount_payable (Union[Unset, float]): [readonly]
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    tax_month: Union[Unset, int] = UNSET
    contractor_name: Union[Unset, None, str] = UNSET
    contractor_address: Union[Unset, Address] = UNSET
    contractor_office_number: Union[Unset, None, str] = UNSET
    contractor_paye_reference: Union[Unset, None, str] = UNSET
    subcontractor_name: Union[Unset, RtiEmployeeName] = UNSET
    sub_contractor_utr: Union[Unset, None, str] = UNSET
    verification_number: Union[Unset, None, str] = UNSET
    gross_amount_paid: Union[Unset, float] = UNSET
    cost_of_materials: Union[Unset, float] = UNSET
    amount_liable_to_deduction: Union[Unset, float] = UNSET
    amount_deducted: Union[Unset, float] = UNSET
    amount_payable: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        tax_month = self.tax_month
        contractor_name = self.contractor_name
        contractor_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contractor_address, Unset):
            contractor_address = self.contractor_address.to_dict()

        contractor_office_number = self.contractor_office_number
        contractor_paye_reference = self.contractor_paye_reference
        subcontractor_name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.subcontractor_name, Unset):
            subcontractor_name = self.subcontractor_name.to_dict()

        sub_contractor_utr = self.sub_contractor_utr
        verification_number = self.verification_number
        gross_amount_paid = self.gross_amount_paid
        cost_of_materials = self.cost_of_materials
        amount_liable_to_deduction = self.amount_liable_to_deduction
        amount_deducted = self.amount_deducted
        amount_payable = self.amount_payable

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if tax_month is not UNSET:
            field_dict["taxMonth"] = tax_month
        if contractor_name is not UNSET:
            field_dict["contractorName"] = contractor_name
        if contractor_address is not UNSET:
            field_dict["contractorAddress"] = contractor_address
        if contractor_office_number is not UNSET:
            field_dict["contractorOfficeNumber"] = contractor_office_number
        if contractor_paye_reference is not UNSET:
            field_dict["contractorPayeReference"] = contractor_paye_reference
        if subcontractor_name is not UNSET:
            field_dict["subcontractorName"] = subcontractor_name
        if sub_contractor_utr is not UNSET:
            field_dict["subContractorUtr"] = sub_contractor_utr
        if verification_number is not UNSET:
            field_dict["verificationNumber"] = verification_number
        if gross_amount_paid is not UNSET:
            field_dict["grossAmountPaid"] = gross_amount_paid
        if cost_of_materials is not UNSET:
            field_dict["costOfMaterials"] = cost_of_materials
        if amount_liable_to_deduction is not UNSET:
            field_dict["amountLiableToDeduction"] = amount_liable_to_deduction
        if amount_deducted is not UNSET:
            field_dict["amountDeducted"] = amount_deducted
        if amount_payable is not UNSET:
            field_dict["amountPayable"] = amount_payable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        tax_month = d.pop("taxMonth", UNSET)

        contractor_name = d.pop("contractorName", UNSET)

        _contractor_address = d.pop("contractorAddress", UNSET)
        contractor_address: Union[Unset, Address]
        if isinstance(_contractor_address, Unset):
            contractor_address = UNSET
        else:
            contractor_address = Address.from_dict(_contractor_address)

        contractor_office_number = d.pop("contractorOfficeNumber", UNSET)

        contractor_paye_reference = d.pop("contractorPayeReference", UNSET)

        _subcontractor_name = d.pop("subcontractorName", UNSET)
        subcontractor_name: Union[Unset, RtiEmployeeName]
        if isinstance(_subcontractor_name, Unset):
            subcontractor_name = UNSET
        else:
            subcontractor_name = RtiEmployeeName.from_dict(_subcontractor_name)

        sub_contractor_utr = d.pop("subContractorUtr", UNSET)

        verification_number = d.pop("verificationNumber", UNSET)

        gross_amount_paid = d.pop("grossAmountPaid", UNSET)

        cost_of_materials = d.pop("costOfMaterials", UNSET)

        amount_liable_to_deduction = d.pop("amountLiableToDeduction", UNSET)

        amount_deducted = d.pop("amountDeducted", UNSET)

        amount_payable = d.pop("amountPayable", UNSET)

        cis_statement = cls(
            tax_year=tax_year,
            tax_month=tax_month,
            contractor_name=contractor_name,
            contractor_address=contractor_address,
            contractor_office_number=contractor_office_number,
            contractor_paye_reference=contractor_paye_reference,
            subcontractor_name=subcontractor_name,
            sub_contractor_utr=sub_contractor_utr,
            verification_number=verification_number,
            gross_amount_paid=gross_amount_paid,
            cost_of_materials=cost_of_materials,
            amount_liable_to_deduction=amount_liable_to_deduction,
            amount_deducted=amount_deducted,
            amount_payable=amount_payable,
        )

        return cis_statement
