import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.p11_detailed_ni_values import P11DetailedNiValues
from ..models.p11_ni_and_stat_payments_line import P11NiAndStatPaymentsLine
from ..models.p11_ni_and_stat_payments_totals_line import P11NiAndStatPaymentsTotalsLine
from ..models.p11_paye_line import P11PayeLine
from ..models.p11_paye_summary import P11PayeSummary
from ..models.p11_paye_totals_line import P11PayeTotalsLine
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11Detailed")


@attr.s(auto_attribs=True)
class P11Detailed:
    """A more comprehensive P11 Report.
    Our Reports API can return this to you in several formats including as a PDF file
    If you request a JSON object then it is represented using this model.

        Attributes:
            employer_name (Union[Unset, None, str]): [readonly]
            payroll_code (Union[Unset, None, str]): [readonly]
            employer_office_no (Union[Unset, None, str]): [readonly]
            employer_paye_ref (Union[Unset, None, str]): [readonly]
            firstname (Union[Unset, None, str]): [readonly]
            middlename (Union[Unset, None, str]): [readonly]
            surname (Union[Unset, None, str]): [readonly]
            ni_number (Union[Unset, None, str]): [readonly]
            tax_code (Union[Unset, None, str]): [readonly]
            date_of_birth (Union[Unset, datetime.date]): [readonly]
            join_date (Union[Unset, datetime.date]): [readonly]
            leave_date (Union[Unset, None, datetime.date]): [readonly]
            is_director (Union[Unset, bool]): [readonly]
            ni_and_stat_payments_lines (Union[Unset, None, List[P11NiAndStatPaymentsLine]]): [readonly]
            totals_line (Union[Unset, P11NiAndStatPaymentsTotalsLine]): Summary line for the NI Contributions and Statutory
                Payments table in the P11 Detailed report
            ni_summary (Union[Unset, None, List[P11DetailedNiValues]]): [readonly]
            paye_lines (Union[Unset, None, List[P11PayeLine]]): [readonly]
            paye_totals_line (Union[Unset, P11PayeTotalsLine]): Summary line for the Paye Income Tax table in the P11
                Detailed report
            paye_summary (Union[Unset, P11PayeSummary]): Forms the PAYE summary in the P11 Detailed report
            report (Union[Unset, Report]):
            tax_year (Union[Unset, TaxYear]):
    """

    employer_name: Union[Unset, None, str] = UNSET
    payroll_code: Union[Unset, None, str] = UNSET
    employer_office_no: Union[Unset, None, str] = UNSET
    employer_paye_ref: Union[Unset, None, str] = UNSET
    firstname: Union[Unset, None, str] = UNSET
    middlename: Union[Unset, None, str] = UNSET
    surname: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    tax_code: Union[Unset, None, str] = UNSET
    date_of_birth: Union[Unset, datetime.date] = UNSET
    join_date: Union[Unset, datetime.date] = UNSET
    leave_date: Union[Unset, None, datetime.date] = UNSET
    is_director: Union[Unset, bool] = UNSET
    ni_and_stat_payments_lines: Union[
        Unset, None, List[P11NiAndStatPaymentsLine]
    ] = UNSET
    totals_line: Union[Unset, P11NiAndStatPaymentsTotalsLine] = UNSET
    ni_summary: Union[Unset, None, List[P11DetailedNiValues]] = UNSET
    paye_lines: Union[Unset, None, List[P11PayeLine]] = UNSET
    paye_totals_line: Union[Unset, P11PayeTotalsLine] = UNSET
    paye_summary: Union[Unset, P11PayeSummary] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer_name = self.employer_name
        payroll_code = self.payroll_code
        employer_office_no = self.employer_office_no
        employer_paye_ref = self.employer_paye_ref
        firstname = self.firstname
        middlename = self.middlename
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

        is_director = self.is_director
        ni_and_stat_payments_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ni_and_stat_payments_lines, Unset):
            if self.ni_and_stat_payments_lines is None:
                ni_and_stat_payments_lines = None
            else:
                ni_and_stat_payments_lines = []
                for (
                    ni_and_stat_payments_lines_item_data
                ) in self.ni_and_stat_payments_lines:
                    ni_and_stat_payments_lines_item = (
                        ni_and_stat_payments_lines_item_data.to_dict()
                    )

                    ni_and_stat_payments_lines.append(ni_and_stat_payments_lines_item)

        totals_line: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals_line, Unset):
            totals_line = self.totals_line.to_dict()

        ni_summary: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ni_summary, Unset):
            if self.ni_summary is None:
                ni_summary = None
            else:
                ni_summary = []
                for ni_summary_item_data in self.ni_summary:
                    ni_summary_item = ni_summary_item_data.to_dict()

                    ni_summary.append(ni_summary_item)

        paye_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.paye_lines, Unset):
            if self.paye_lines is None:
                paye_lines = None
            else:
                paye_lines = []
                for paye_lines_item_data in self.paye_lines:
                    paye_lines_item = paye_lines_item_data.to_dict()

                    paye_lines.append(paye_lines_item)

        paye_totals_line: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.paye_totals_line, Unset):
            paye_totals_line = self.paye_totals_line.to_dict()

        paye_summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.paye_summary, Unset):
            paye_summary = self.paye_summary.to_dict()

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
        if middlename is not UNSET:
            field_dict["middlename"] = middlename
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
        if is_director is not UNSET:
            field_dict["isDirector"] = is_director
        if ni_and_stat_payments_lines is not UNSET:
            field_dict["niAndStatPaymentsLines"] = ni_and_stat_payments_lines
        if totals_line is not UNSET:
            field_dict["totalsLine"] = totals_line
        if ni_summary is not UNSET:
            field_dict["niSummary"] = ni_summary
        if paye_lines is not UNSET:
            field_dict["payeLines"] = paye_lines
        if paye_totals_line is not UNSET:
            field_dict["payeTotalsLine"] = paye_totals_line
        if paye_summary is not UNSET:
            field_dict["payeSummary"] = paye_summary
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

        middlename = d.pop("middlename", UNSET)

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

        is_director = d.pop("isDirector", UNSET)

        ni_and_stat_payments_lines = []
        _ni_and_stat_payments_lines = d.pop("niAndStatPaymentsLines", UNSET)
        for ni_and_stat_payments_lines_item_data in _ni_and_stat_payments_lines or []:
            ni_and_stat_payments_lines_item = P11NiAndStatPaymentsLine.from_dict(
                ni_and_stat_payments_lines_item_data
            )

            ni_and_stat_payments_lines.append(ni_and_stat_payments_lines_item)

        _totals_line = d.pop("totalsLine", UNSET)
        totals_line: Union[Unset, P11NiAndStatPaymentsTotalsLine]
        if isinstance(_totals_line, Unset):
            totals_line = UNSET
        else:
            totals_line = P11NiAndStatPaymentsTotalsLine.from_dict(_totals_line)

        ni_summary = []
        _ni_summary = d.pop("niSummary", UNSET)
        for ni_summary_item_data in _ni_summary or []:
            ni_summary_item = P11DetailedNiValues.from_dict(ni_summary_item_data)

            ni_summary.append(ni_summary_item)

        paye_lines = []
        _paye_lines = d.pop("payeLines", UNSET)
        for paye_lines_item_data in _paye_lines or []:
            paye_lines_item = P11PayeLine.from_dict(paye_lines_item_data)

            paye_lines.append(paye_lines_item)

        _paye_totals_line = d.pop("payeTotalsLine", UNSET)
        paye_totals_line: Union[Unset, P11PayeTotalsLine]
        if isinstance(_paye_totals_line, Unset):
            paye_totals_line = UNSET
        else:
            paye_totals_line = P11PayeTotalsLine.from_dict(_paye_totals_line)

        _paye_summary = d.pop("payeSummary", UNSET)
        paye_summary: Union[Unset, P11PayeSummary]
        if isinstance(_paye_summary, Unset):
            paye_summary = UNSET
        else:
            paye_summary = P11PayeSummary.from_dict(_paye_summary)

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

        p11_detailed = cls(
            employer_name=employer_name,
            payroll_code=payroll_code,
            employer_office_no=employer_office_no,
            employer_paye_ref=employer_paye_ref,
            firstname=firstname,
            middlename=middlename,
            surname=surname,
            ni_number=ni_number,
            tax_code=tax_code,
            date_of_birth=date_of_birth,
            join_date=join_date,
            leave_date=leave_date,
            is_director=is_director,
            ni_and_stat_payments_lines=ni_and_stat_payments_lines,
            totals_line=totals_line,
            ni_summary=ni_summary,
            paye_lines=paye_lines,
            paye_totals_line=paye_totals_line,
            paye_summary=paye_summary,
            report=report,
            tax_year=tax_year,
        )

        return p11_detailed
