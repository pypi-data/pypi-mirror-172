from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.employee_ytd_values import EmployeeYtdValues
from ..models.pay_run import PayRun
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="YtdReport")


@attr.s(auto_attribs=True)
class YtdReport:
    """
    Attributes:
        payrun (Union[Unset, PayRun]): This model is right at the very heart of the software.
            There is a PayRun for each period in which people are paid.
        lines (Union[Unset, None, List[EmployeeYtdValues]]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
    """

    payrun: Union[Unset, PayRun] = UNSET
    lines: Union[Unset, None, List[EmployeeYtdValues]] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payrun: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payrun, Unset):
            payrun = self.payrun.to_dict()

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
        if payrun is not UNSET:
            field_dict["payrun"] = payrun
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
        _payrun = d.pop("payrun", UNSET)
        payrun: Union[Unset, PayRun]
        if isinstance(_payrun, Unset):
            payrun = UNSET
        else:
            payrun = PayRun.from_dict(_payrun)

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = EmployeeYtdValues.from_dict(lines_item_data)

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

        ytd_report = cls(
            payrun=payrun,
            lines=lines,
            report=report,
            tax_year=tax_year,
        )

        return ytd_report
