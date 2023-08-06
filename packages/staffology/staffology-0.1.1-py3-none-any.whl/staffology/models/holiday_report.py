from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.holiday_report_line import HolidayReportLine
from ..models.item import Item
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="HolidayReport")


@attr.s(auto_attribs=True)
class HolidayReport:
    """
    Attributes:
        accruals_report (Union[Unset, bool]):
        employer (Union[Unset, Item]):
        lines (Union[Unset, None, List[HolidayReportLine]]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
    """

    accruals_report: Union[Unset, bool] = UNSET
    employer: Union[Unset, Item] = UNSET
    lines: Union[Unset, None, List[HolidayReportLine]] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        accruals_report = self.accruals_report
        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

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
        if accruals_report is not UNSET:
            field_dict["accrualsReport"] = accruals_report
        if employer is not UNSET:
            field_dict["employer"] = employer
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
        accruals_report = d.pop("accrualsReport", UNSET)

        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, Item]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = Item.from_dict(_employer)

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = HolidayReportLine.from_dict(lines_item_data)

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

        holiday_report = cls(
            accruals_report=accruals_report,
            employer=employer,
            lines=lines,
            report=report,
            tax_year=tax_year,
        )

        return holiday_report
