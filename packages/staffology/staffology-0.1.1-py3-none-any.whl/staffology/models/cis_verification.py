from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cis_request import CisRequest
from ..models.cis_sub_contractor import CisSubContractor
from ..models.emp_refs import EmpRefs
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.item import Item
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisVerification")


@attr.s(auto_attribs=True)
class CisVerification:
    """If an Employee is marked as a CIS Subcontractor then this model is included ad a child of CisDetails and is used to
    represent the Verification details of the Subcontractor

        Attributes:
            employees (Union[Unset, None, List[Item]]):
            employee_count (Union[Unset, int]):
            cis_request (Union[Unset, CisRequest]):
            responses (Union[Unset, None, List[CisSubContractor]]):
            i_rmark (Union[Unset, None, str]):
            xml (Union[Unset, None, str]):
            tax_year (Union[Unset, TaxYear]):
            employer_references (Union[Unset, EmpRefs]):
            gov_talk_submission (Union[Unset, GovTalkSubmission]):
            id (Union[Unset, str]): [readonly] The unique id of the object
    """

    employees: Union[Unset, None, List[Item]] = UNSET
    employee_count: Union[Unset, int] = UNSET
    cis_request: Union[Unset, CisRequest] = UNSET
    responses: Union[Unset, None, List[CisSubContractor]] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    xml: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    employer_references: Union[Unset, EmpRefs] = UNSET
    gov_talk_submission: Union[Unset, GovTalkSubmission] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employees: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employees, Unset):
            if self.employees is None:
                employees = None
            else:
                employees = []
                for employees_item_data in self.employees:
                    employees_item = employees_item_data.to_dict()

                    employees.append(employees_item)

        employee_count = self.employee_count
        cis_request: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cis_request, Unset):
            cis_request = self.cis_request.to_dict()

        responses: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.responses, Unset):
            if self.responses is None:
                responses = None
            else:
                responses = []
                for responses_item_data in self.responses:
                    responses_item = responses_item_data.to_dict()

                    responses.append(responses_item)

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
        if employees is not UNSET:
            field_dict["employees"] = employees
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if cis_request is not UNSET:
            field_dict["cisRequest"] = cis_request
        if responses is not UNSET:
            field_dict["responses"] = responses
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
        employees = []
        _employees = d.pop("employees", UNSET)
        for employees_item_data in _employees or []:
            employees_item = Item.from_dict(employees_item_data)

            employees.append(employees_item)

        employee_count = d.pop("employeeCount", UNSET)

        _cis_request = d.pop("cisRequest", UNSET)
        cis_request: Union[Unset, CisRequest]
        if isinstance(_cis_request, Unset):
            cis_request = UNSET
        else:
            cis_request = CisRequest.from_dict(_cis_request)

        responses = []
        _responses = d.pop("responses", UNSET)
        for responses_item_data in _responses or []:
            responses_item = CisSubContractor.from_dict(responses_item_data)

            responses.append(responses_item)

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

        cis_verification = cls(
            employees=employees,
            employee_count=employee_count,
            cis_request=cis_request,
            responses=responses,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return cis_verification
