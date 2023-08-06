import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.full_summary_of_pay_report_line import FullSummaryOfPayReportLine
from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="FullSummaryOfPayReport")


@attr.s(auto_attribs=True)
class FullSummaryOfPayReport:
    """
    Attributes:
        lines (Union[Unset, None, List[FullSummaryOfPayReportLine]]):
        deduction_lines (Union[Unset, None, List[FullSummaryOfPayReportLine]]):
        employer (Union[Unset, Item]):
        pay_period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]):
        period (Union[Unset, int]):
        period_to (Union[Unset, int]):
        start_period_name (Union[Unset, None, str]):
        end_period_name (Union[Unset, None, str]):
        start_date (Union[Unset, datetime.date]):
        end_date (Union[Unset, datetime.date]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
    """

    lines: Union[Unset, None, List[FullSummaryOfPayReportLine]] = UNSET
    deduction_lines: Union[Unset, None, List[FullSummaryOfPayReportLine]] = UNSET
    employer: Union[Unset, Item] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET
    period_to: Union[Unset, int] = UNSET
    start_period_name: Union[Unset, None, str] = UNSET
    end_period_name: Union[Unset, None, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        deduction_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.deduction_lines, Unset):
            if self.deduction_lines is None:
                deduction_lines = None
            else:
                deduction_lines = []
                for deduction_lines_item_data in self.deduction_lines:
                    deduction_lines_item = deduction_lines_item_data.to_dict()

                    deduction_lines.append(deduction_lines_item)

        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period
        period_to = self.period_to
        start_period_name = self.start_period_name
        end_period_name = self.end_period_name
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if lines is not UNSET:
            field_dict["lines"] = lines
        if deduction_lines is not UNSET:
            field_dict["deductionLines"] = deduction_lines
        if employer is not UNSET:
            field_dict["employer"] = employer
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period
        if period_to is not UNSET:
            field_dict["periodTo"] = period_to
        if start_period_name is not UNSET:
            field_dict["startPeriodName"] = start_period_name
        if end_period_name is not UNSET:
            field_dict["endPeriodName"] = end_period_name
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = FullSummaryOfPayReportLine.from_dict(lines_item_data)

            lines.append(lines_item)

        deduction_lines = []
        _deduction_lines = d.pop("deductionLines", UNSET)
        for deduction_lines_item_data in _deduction_lines or []:
            deduction_lines_item = FullSummaryOfPayReportLine.from_dict(
                deduction_lines_item_data
            )

            deduction_lines.append(deduction_lines_item)

        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, Item]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = Item.from_dict(_employer)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

        period_to = d.pop("periodTo", UNSET)

        start_period_name = d.pop("startPeriodName", UNSET)

        end_period_name = d.pop("endPeriodName", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.date]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()

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

        full_summary_of_pay_report = cls(
            lines=lines,
            deduction_lines=deduction_lines,
            employer=employer,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
            period_to=period_to,
            start_period_name=start_period_name,
            end_period_name=end_period_name,
            start_date=start_date,
            end_date=end_date,
            report=report,
            tax_year=tax_year,
        )

        return full_summary_of_pay_report
