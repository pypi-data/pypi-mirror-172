import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.dps_data_type import DpsDataType
from ..models.item import Item
from ..models.student_loan import StudentLoan
from ..types import UNSET, Unset

T = TypeVar("T", bound="DpsNotice")


@attr.s(auto_attribs=True)
class DpsNotice:
    """
    Attributes:
        issue_date (Union[Unset, datetime.date]):
        effective_date (Union[Unset, datetime.date]):
        tax_year (Union[Unset, int]):
        sequence_number (Union[Unset, int]):
        type (Union[Unset, DpsDataType]):
        form_type (Union[Unset, None, str]):
        forename (Union[Unset, None, str]):
        surname (Union[Unset, None, str]):
        ni_no (Union[Unset, None, str]):
        works_number (Union[Unset, None, str]):
        tax_code (Union[Unset, None, str]):
        week_1_month_1 (Union[Unset, None, bool]):
        previous_tax (Union[Unset, None, float]):
        previous_pay (Union[Unset, None, float]):
        plan_type (Union[Unset, StudentLoan]):
        applied_on (Union[Unset, None, datetime.date]):
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    issue_date: Union[Unset, datetime.date] = UNSET
    effective_date: Union[Unset, datetime.date] = UNSET
    tax_year: Union[Unset, int] = UNSET
    sequence_number: Union[Unset, int] = UNSET
    type: Union[Unset, DpsDataType] = UNSET
    form_type: Union[Unset, None, str] = UNSET
    forename: Union[Unset, None, str] = UNSET
    surname: Union[Unset, None, str] = UNSET
    ni_no: Union[Unset, None, str] = UNSET
    works_number: Union[Unset, None, str] = UNSET
    tax_code: Union[Unset, None, str] = UNSET
    week_1_month_1: Union[Unset, None, bool] = UNSET
    previous_tax: Union[Unset, None, float] = UNSET
    previous_pay: Union[Unset, None, float] = UNSET
    plan_type: Union[Unset, StudentLoan] = UNSET
    applied_on: Union[Unset, None, datetime.date] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_date: Union[Unset, str] = UNSET
        if not isinstance(self.issue_date, Unset):
            issue_date = self.issue_date.isoformat()

        effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        tax_year = self.tax_year
        sequence_number = self.sequence_number
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        form_type = self.form_type
        forename = self.forename
        surname = self.surname
        ni_no = self.ni_no
        works_number = self.works_number
        tax_code = self.tax_code
        week_1_month_1 = self.week_1_month_1
        previous_tax = self.previous_tax
        previous_pay = self.previous_pay
        plan_type: Union[Unset, str] = UNSET
        if not isinstance(self.plan_type, Unset):
            plan_type = self.plan_type.value

        applied_on: Union[Unset, None, str] = UNSET
        if not isinstance(self.applied_on, Unset):
            applied_on = self.applied_on.isoformat() if self.applied_on else None

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_date is not UNSET:
            field_dict["issueDate"] = issue_date
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if sequence_number is not UNSET:
            field_dict["sequenceNumber"] = sequence_number
        if type is not UNSET:
            field_dict["type"] = type
        if form_type is not UNSET:
            field_dict["formType"] = form_type
        if forename is not UNSET:
            field_dict["forename"] = forename
        if surname is not UNSET:
            field_dict["surname"] = surname
        if ni_no is not UNSET:
            field_dict["niNo"] = ni_no
        if works_number is not UNSET:
            field_dict["worksNumber"] = works_number
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code
        if week_1_month_1 is not UNSET:
            field_dict["week1Month1"] = week_1_month_1
        if previous_tax is not UNSET:
            field_dict["previousTax"] = previous_tax
        if previous_pay is not UNSET:
            field_dict["previousPay"] = previous_pay
        if plan_type is not UNSET:
            field_dict["planType"] = plan_type
        if applied_on is not UNSET:
            field_dict["appliedOn"] = applied_on
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _issue_date = d.pop("issueDate", UNSET)
        issue_date: Union[Unset, datetime.date]
        if isinstance(_issue_date, Unset):
            issue_date = UNSET
        else:
            issue_date = isoparse(_issue_date).date()

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: Union[Unset, datetime.date]
        if isinstance(_effective_date, Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date).date()

        tax_year = d.pop("taxYear", UNSET)

        sequence_number = d.pop("sequenceNumber", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, DpsDataType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DpsDataType(_type)

        form_type = d.pop("formType", UNSET)

        forename = d.pop("forename", UNSET)

        surname = d.pop("surname", UNSET)

        ni_no = d.pop("niNo", UNSET)

        works_number = d.pop("worksNumber", UNSET)

        tax_code = d.pop("taxCode", UNSET)

        week_1_month_1 = d.pop("week1Month1", UNSET)

        previous_tax = d.pop("previousTax", UNSET)

        previous_pay = d.pop("previousPay", UNSET)

        _plan_type = d.pop("planType", UNSET)
        plan_type: Union[Unset, StudentLoan]
        if isinstance(_plan_type, Unset):
            plan_type = UNSET
        else:
            plan_type = StudentLoan(_plan_type)

        _applied_on = d.pop("appliedOn", UNSET)
        applied_on: Union[Unset, None, datetime.date]
        if _applied_on is None:
            applied_on = None
        elif isinstance(_applied_on, Unset):
            applied_on = UNSET
        else:
            applied_on = isoparse(_applied_on).date()

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        dps_notice = cls(
            issue_date=issue_date,
            effective_date=effective_date,
            tax_year=tax_year,
            sequence_number=sequence_number,
            type=type,
            form_type=form_type,
            forename=forename,
            surname=surname,
            ni_no=ni_no,
            works_number=works_number,
            tax_code=tax_code,
            week_1_month_1=week_1_month_1,
            previous_tax=previous_tax,
            previous_pay=previous_pay,
            plan_type=plan_type,
            applied_on=applied_on,
            employee=employee,
            id=id,
        )

        return dps_notice
