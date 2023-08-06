from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cis_return import CisReturn
from ..models.emp_refs import EmpRefs
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Cis300")


@attr.s(auto_attribs=True)
class Cis300:
    """
    Attributes:
        tax_month (Union[Unset, int]):
        employee_count (Union[Unset, int]):
        employment_status_declaration (Union[Unset, bool]):
        verification_declaration (Union[Unset, bool]):
        information_correct_declaration (Union[Unset, bool]):
        inactivity_declaration (Union[Unset, bool]):
        cis_return (Union[Unset, CisReturn]):
        i_rmark (Union[Unset, None, str]):
        xml (Union[Unset, None, str]):
        tax_year (Union[Unset, TaxYear]):
        employer_references (Union[Unset, EmpRefs]):
        gov_talk_submission (Union[Unset, GovTalkSubmission]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    tax_month: Union[Unset, int] = UNSET
    employee_count: Union[Unset, int] = UNSET
    employment_status_declaration: Union[Unset, bool] = UNSET
    verification_declaration: Union[Unset, bool] = UNSET
    information_correct_declaration: Union[Unset, bool] = UNSET
    inactivity_declaration: Union[Unset, bool] = UNSET
    cis_return: Union[Unset, CisReturn] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    xml: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    employer_references: Union[Unset, EmpRefs] = UNSET
    gov_talk_submission: Union[Unset, GovTalkSubmission] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_month = self.tax_month
        employee_count = self.employee_count
        employment_status_declaration = self.employment_status_declaration
        verification_declaration = self.verification_declaration
        information_correct_declaration = self.information_correct_declaration
        inactivity_declaration = self.inactivity_declaration
        cis_return: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cis_return, Unset):
            cis_return = self.cis_return.to_dict()

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
        if tax_month is not UNSET:
            field_dict["taxMonth"] = tax_month
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if employment_status_declaration is not UNSET:
            field_dict["employmentStatusDeclaration"] = employment_status_declaration
        if verification_declaration is not UNSET:
            field_dict["verificationDeclaration"] = verification_declaration
        if information_correct_declaration is not UNSET:
            field_dict[
                "informationCorrectDeclaration"
            ] = information_correct_declaration
        if inactivity_declaration is not UNSET:
            field_dict["inactivityDeclaration"] = inactivity_declaration
        if cis_return is not UNSET:
            field_dict["cisReturn"] = cis_return
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
        tax_month = d.pop("taxMonth", UNSET)

        employee_count = d.pop("employeeCount", UNSET)

        employment_status_declaration = d.pop("employmentStatusDeclaration", UNSET)

        verification_declaration = d.pop("verificationDeclaration", UNSET)

        information_correct_declaration = d.pop("informationCorrectDeclaration", UNSET)

        inactivity_declaration = d.pop("inactivityDeclaration", UNSET)

        _cis_return = d.pop("cisReturn", UNSET)
        cis_return: Union[Unset, CisReturn]
        if isinstance(_cis_return, Unset):
            cis_return = UNSET
        else:
            cis_return = CisReturn.from_dict(_cis_return)

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

        cis_300 = cls(
            tax_month=tax_month,
            employee_count=employee_count,
            employment_status_declaration=employment_status_declaration,
            verification_declaration=verification_declaration,
            information_correct_declaration=information_correct_declaration,
            inactivity_declaration=inactivity_declaration,
            cis_return=cis_return,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return cis_300
