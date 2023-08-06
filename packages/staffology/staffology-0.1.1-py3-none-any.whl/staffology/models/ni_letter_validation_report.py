import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.ni_letter_validation_report_line import NiLetterValidationReportLine
from ..models.pay_periods import PayPeriods
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="NiLetterValidationReport")


@attr.s(auto_attribs=True)
class NiLetterValidationReport:
    """
    Attributes:
        based_on_payrun (Union[Unset, bool]): If false, then any payrun related information (Tax year, etc) should be
            ignored.
        error_lines (Union[Unset, None, List[NiLetterValidationReportLine]]):
        payment_date (Union[Unset, None, datetime.date]):
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

    based_on_payrun: Union[Unset, bool] = UNSET
    error_lines: Union[Unset, None, List[NiLetterValidationReportLine]] = UNSET
    payment_date: Union[Unset, None, datetime.date] = UNSET
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
        based_on_payrun = self.based_on_payrun
        error_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.error_lines, Unset):
            if self.error_lines is None:
                error_lines = None
            else:
                error_lines = []
                for error_lines_item_data in self.error_lines:
                    error_lines_item = error_lines_item_data.to_dict()

                    error_lines.append(error_lines_item)

        payment_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat() if self.payment_date else None

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
        if based_on_payrun is not UNSET:
            field_dict["basedOnPayrun"] = based_on_payrun
        if error_lines is not UNSET:
            field_dict["errorLines"] = error_lines
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
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
        based_on_payrun = d.pop("basedOnPayrun", UNSET)

        error_lines = []
        _error_lines = d.pop("errorLines", UNSET)
        for error_lines_item_data in _error_lines or []:
            error_lines_item = NiLetterValidationReportLine.from_dict(
                error_lines_item_data
            )

            error_lines.append(error_lines_item)

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, None, datetime.date]
        if _payment_date is None:
            payment_date = None
        elif isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

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

        ni_letter_validation_report = cls(
            based_on_payrun=based_on_payrun,
            error_lines=error_lines,
            payment_date=payment_date,
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

        return ni_letter_validation_report
