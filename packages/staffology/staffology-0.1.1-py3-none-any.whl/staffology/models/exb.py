from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.emp_refs import EmpRefs
from ..models.expenses_and_benefits import ExpensesAndBenefits
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Exb")


@attr.s(auto_attribs=True)
class Exb:
    """
    Attributes:
        additions_amount (Union[Unset, float]):
        additions_description (Union[Unset, None, str]):
        deductions_amount (Union[Unset, float]):
        deductions_description (Union[Unset, None, str]):
        employee_count (Union[Unset, int]): [readonly] The number of employees with a P11D
        total_benefits (Union[Unset, float]): [readonly] Total value of benefits, not including any deductions or
            additions
        total_adjusted_benefits (Union[Unset, float]): [readonly] Total value of benefits
        nics_rate (Union[Unset, float]): [readonly] The Class 1A NICS Rate
        nics_payable (Union[Unset, float]): [readonly] NICs Payable
        expenses_and_benefits (Union[Unset, ExpensesAndBenefits]):
        i_rmark (Union[Unset, None, str]):
        xml (Union[Unset, None, str]):
        tax_year (Union[Unset, TaxYear]):
        employer_references (Union[Unset, EmpRefs]):
        gov_talk_submission (Union[Unset, GovTalkSubmission]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    additions_amount: Union[Unset, float] = UNSET
    additions_description: Union[Unset, None, str] = UNSET
    deductions_amount: Union[Unset, float] = UNSET
    deductions_description: Union[Unset, None, str] = UNSET
    employee_count: Union[Unset, int] = UNSET
    total_benefits: Union[Unset, float] = UNSET
    total_adjusted_benefits: Union[Unset, float] = UNSET
    nics_rate: Union[Unset, float] = UNSET
    nics_payable: Union[Unset, float] = UNSET
    expenses_and_benefits: Union[Unset, ExpensesAndBenefits] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    xml: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    employer_references: Union[Unset, EmpRefs] = UNSET
    gov_talk_submission: Union[Unset, GovTalkSubmission] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        additions_amount = self.additions_amount
        additions_description = self.additions_description
        deductions_amount = self.deductions_amount
        deductions_description = self.deductions_description
        employee_count = self.employee_count
        total_benefits = self.total_benefits
        total_adjusted_benefits = self.total_adjusted_benefits
        nics_rate = self.nics_rate
        nics_payable = self.nics_payable
        expenses_and_benefits: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.expenses_and_benefits, Unset):
            expenses_and_benefits = self.expenses_and_benefits.to_dict()

        i_rmark = self.i_rmark
        xml = self.xml
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        employer_references: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer_references, Unset):
            employer_references = self.employer_references.to_dict()

        gov_talk_submission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.gov_talk_submission, Unset):
            gov_talk_submission = self.gov_talk_submission.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if additions_amount is not UNSET:
            field_dict["additionsAmount"] = additions_amount
        if additions_description is not UNSET:
            field_dict["additionsDescription"] = additions_description
        if deductions_amount is not UNSET:
            field_dict["deductionsAmount"] = deductions_amount
        if deductions_description is not UNSET:
            field_dict["deductionsDescription"] = deductions_description
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if total_benefits is not UNSET:
            field_dict["totalBenefits"] = total_benefits
        if total_adjusted_benefits is not UNSET:
            field_dict["totalAdjustedBenefits"] = total_adjusted_benefits
        if nics_rate is not UNSET:
            field_dict["nicsRate"] = nics_rate
        if nics_payable is not UNSET:
            field_dict["nicsPayable"] = nics_payable
        if expenses_and_benefits is not UNSET:
            field_dict["expensesAndBenefits"] = expenses_and_benefits
        if i_rmark is not UNSET:
            field_dict["iRmark"] = i_rmark
        if xml is not UNSET:
            field_dict["xml"] = xml
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if employer_references is not UNSET:
            field_dict["employerReferences"] = employer_references
        if gov_talk_submission is not UNSET:
            field_dict["govTalkSubmission"] = gov_talk_submission
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        additions_amount = d.pop("additionsAmount", UNSET)

        additions_description = d.pop("additionsDescription", UNSET)

        deductions_amount = d.pop("deductionsAmount", UNSET)

        deductions_description = d.pop("deductionsDescription", UNSET)

        employee_count = d.pop("employeeCount", UNSET)

        total_benefits = d.pop("totalBenefits", UNSET)

        total_adjusted_benefits = d.pop("totalAdjustedBenefits", UNSET)

        nics_rate = d.pop("nicsRate", UNSET)

        nics_payable = d.pop("nicsPayable", UNSET)

        _expenses_and_benefits = d.pop("expensesAndBenefits", UNSET)
        expenses_and_benefits: Union[Unset, ExpensesAndBenefits]
        if isinstance(_expenses_and_benefits, Unset):
            expenses_and_benefits = UNSET
        else:
            expenses_and_benefits = ExpensesAndBenefits.from_dict(
                _expenses_and_benefits
            )

        i_rmark = d.pop("iRmark", UNSET)

        xml = d.pop("xml", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _employer_references = d.pop("employerReferences", UNSET)
        employer_references: Union[Unset, EmpRefs]
        if isinstance(_employer_references, Unset):
            employer_references = UNSET
        else:
            employer_references = EmpRefs.from_dict(_employer_references)

        _gov_talk_submission = d.pop("govTalkSubmission", UNSET)
        gov_talk_submission: Union[Unset, GovTalkSubmission]
        if isinstance(_gov_talk_submission, Unset):
            gov_talk_submission = UNSET
        else:
            gov_talk_submission = GovTalkSubmission.from_dict(_gov_talk_submission)

        id = d.pop("id", UNSET)

        exb = cls(
            additions_amount=additions_amount,
            additions_description=additions_description,
            deductions_amount=deductions_amount,
            deductions_description=deductions_description,
            employee_count=employee_count,
            total_benefits=total_benefits,
            total_adjusted_benefits=total_adjusted_benefits,
            nics_rate=nics_rate,
            nics_payable=nics_payable,
            expenses_and_benefits=expenses_and_benefits,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return exb
