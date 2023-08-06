import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_status import BackgroundTaskStatus
from ..models.pay_periods import PayPeriods
from ..models.pay_run_summary_line import PayRunSummaryLine
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunJournal")


@attr.s(auto_attribs=True)
class PayRunJournal:
    """
    Attributes:
        lines (Union[Unset, None, List[PayRunSummaryLine]]):
        date (Union[Unset, datetime.date]): [readonly] The PaymentDate from the PayRun
        title (Union[Unset, None, str]): [readonly] The status of the task for posting this journal to an
            ExternalDataProvider
        status (Union[Unset, BackgroundTaskStatus]):
        status_message (Union[Unset, None, str]): [readonly] A message to elaborate on the Status
        link (Union[Unset, None, str]): [readonly] If available, a link to the journal in the ExternalDataProvider
        tax_year (Union[Unset, TaxYear]):
        pay_period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]): [readonly]
        period (Union[Unset, int]): [readonly]
    """

    lines: Union[Unset, None, List[PayRunSummaryLine]] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    title: Union[Unset, None, str] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    link: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET

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

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        title = self.title
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message
        link = self.link
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if lines is not UNSET:
            field_dict["lines"] = lines
        if date is not UNSET:
            field_dict["date"] = date
        if title is not UNSET:
            field_dict["title"] = title
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if link is not UNSET:
            field_dict["link"] = link
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = PayRunSummaryLine.from_dict(lines_item_data)

            lines.append(lines_item)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        title = d.pop("title", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)

        status_message = d.pop("statusMessage", UNSET)

        link = d.pop("link", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

        pay_run_journal = cls(
            lines=lines,
            date=date,
            title=title,
            status=status,
            status_message=status_message,
            link=link,
            tax_year=tax_year,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
        )

        return pay_run_journal
