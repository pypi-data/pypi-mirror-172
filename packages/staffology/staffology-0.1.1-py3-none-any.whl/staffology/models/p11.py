import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.p11_line import P11Line
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11")


@attr.s(auto_attribs=True)
class P11:
    """A P11 Report summarises payments and deductions made to an employee.
    Our Reports API can return this to you in many formats including as a PDF file
    If you request is as a JSOn object then it is represented using this model.

        Attributes:
            employer_name (Union[Unset, None, str]): [readonly]
            payroll_code (Union[Unset, None, str]): [readonly]
            employer_office_no (Union[Unset, None, str]): [readonly]
            employer_paye_ref (Union[Unset, None, str]): [readonly]
            firstname (Union[Unset, None, str]): [readonly]
            surname (Union[Unset, None, str]): [readonly]
            ni_number (Union[Unset, None, str]): [readonly]
            tax_code (Union[Unset, None, str]): [readonly]
            date_of_birth (Union[Unset, datetime.date]): [readonly]
            join_date (Union[Unset, datetime.date]): [readonly]
            leave_date (Union[Unset, None, datetime.date]): [readonly]
            lines (Union[Unset, None, List[P11Line]]): [readonly]
            report (Union[Unset, Report]):
            tax_year (Union[Unset, TaxYear]):
    """

    employer_name: Union[Unset, None, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    employer_office_no: Union[Unset, None, str] = UNSET
    employer_paye_ref: Union[Unset, None, str] = UNSET
    firstname: Union[Unset, None, str] = UNSET
    surname: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    tax_code: Union[Unset, None, str] = UNSET
    date_of_birth: Union[Unset, datetime.date] = UNSET
    join_date: Union[Unset, datetime.date] = UNSET
    leave_date: Union[Unset, None, datetime.date] = UNSET
    lines: Union[Unset, None, List[P11Line]] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer_name = self.employer_name
        payroll_code = self.payroll_code
        employer_office_no = self.employer_office_no
        employer_paye_ref = self.employer_paye_ref
        firstname = self.firstname
        surname = self.surname
        ni_number = self.ni_number
        tax_code = self.tax_code
        date_of_birth: Union[Unset, str] = UNSET
        if not isinstance(self.date_of_birth, Unset):
            date_of_birth = self.date_of_birth.isoformat()

        join_date: Union[Unset, str] = UNSET
        if not isinstance(self.join_date, Unset):
            join_date = self.join_date.isoformat()

        leave_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.leave_date, Unset):
            leave_date = self.leave_date.isoformat() if self.leave_date else None

        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer_name is not UNSET:
            field_dict["employerName"] = employer_name
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if employer_office_no is not UNSET:
            field_dict["employerOfficeNo"] = employer_office_no
        if employer_paye_ref is not UNSET:
            field_dict["employerPayeRef"] = employer_paye_ref
        if firstname is not UNSET:
            field_dict["firstname"] = firstname
        if surname is not UNSET:
            field_dict["surname"] = surname
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code
        if date_of_birth is not UNSET:
            field_dict["dateOfBirth"] = date_of_birth
        if join_date is not UNSET:
            field_dict["joinDate"] = join_date
        if leave_date is not UNSET:
            field_dict["leaveDate"] = leave_date
        if lines is not UNSET:
            field_dict["lines"] = lines
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_name = d.pop("employerName", UNSET)

        payroll_code = d.pop("payrollCode", UNSET)

        employer_office_no = d.pop("employerOfficeNo", UNSET)

        employer_paye_ref = d.pop("employerPayeRef", UNSET)

        firstname = d.pop("firstname", UNSET)

        surname = d.pop("surname", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        tax_code = d.pop("taxCode", UNSET)

        _date_of_birth = d.pop("dateOfBirth", UNSET)
        date_of_birth: Union[Unset, datetime.date]
        if isinstance(_date_of_birth, Unset):
            date_of_birth = UNSET
        else:
            date_of_birth = isoparse(_date_of_birth).date()

        _join_date = d.pop("joinDate", UNSET)
        join_date: Union[Unset, datetime.date]
        if isinstance(_join_date, Unset):
            join_date = UNSET
        else:
            join_date = isoparse(_join_date).date()

        _leave_date = d.pop("leaveDate", UNSET)
        leave_date: Union[Unset, None, datetime.date]
        if _leave_date is None:
            leave_date = None
        elif isinstance(_leave_date, Unset):
            leave_date = UNSET
        else:
            leave_date = isoparse(_leave_date).date()

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = P11Line.from_dict(lines_item_data)

            lines.append(lines_item)

        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = Report(_report)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        p11 = cls(
            employer_name=employer_name,
            payroll_code=payroll_code,
            employer_office_no=employer_office_no,
            employer_paye_ref=employer_paye_ref,
            firstname=firstname,
            surname=surname,
            ni_number=ni_number,
            tax_code=tax_code,
            date_of_birth=date_of_birth,
            join_date=join_date,
            leave_date=leave_date,
            lines=lines,
            report=report,
            tax_year=tax_year,
        )

        return p11
