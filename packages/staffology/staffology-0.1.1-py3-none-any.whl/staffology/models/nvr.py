from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.emp_refs import EmpRefs
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.item import Item
from ..models.nvr_request import NvrRequest
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Nvr")


@attr.s(auto_attribs=True)
class Nvr:
    """
    Attributes:
        employees (Union[Unset, None, List[Item]]):
        employee_count (Union[Unset, int]):
        nvr_request (Union[Unset, NvrRequest]):
        i_rmark (Union[Unset, None, str]):
        xml (Union[Unset, None, str]):
        tax_year (Union[Unset, TaxYear]):
        employer_references (Union[Unset, EmpRefs]):
        gov_talk_submission (Union[Unset, GovTalkSubmission]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    employees: Union[Unset, None, List[Item]] = UNSET
    employee_count: Union[Unset, int] = UNSET
    nvr_request: Union[Unset, NvrRequest] = UNSET
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
        nvr_request: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.nvr_request, Unset):
            nvr_request = self.nvr_request.to_dict()

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
        if nvr_request is not UNSET:
            field_dict["nvrRequest"] = nvr_request
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

        _nvr_request = d.pop("nvrRequest", UNSET)
        nvr_request: Union[Unset, NvrRequest]
        if isinstance(_nvr_request, Unset):
            nvr_request = UNSET
        else:
            nvr_request = NvrRequest.from_dict(_nvr_request)

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

        nvr = cls(
            employees=employees,
            employee_count=employee_count,
            nvr_request=nvr_request,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return nvr
