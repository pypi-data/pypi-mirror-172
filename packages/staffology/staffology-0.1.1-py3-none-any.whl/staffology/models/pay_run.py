import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.pay_run_state import PayRunState
from ..models.pay_run_totals import PayRunTotals
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRun")


@attr.s(auto_attribs=True)
class PayRun:
    """This model is right at the very heart of the software.
    There is a PayRun for each period in which people are paid.

        Attributes:
            tax_year (Union[Unset, TaxYear]):
            tax_month (Union[Unset, int]): [readonly] The Tax Month that the Payment Date falls in
            pay_period (Union[Unset, PayPeriods]):
            ordinal (Union[Unset, int]): [readonly] Indicates whether this uses first, second, third (etc.) PaySchedule for
                this PayPeriod.
            period (Union[Unset, int]): [readonly] The period (i.e, Tax Week or Tax Month) that this PayRun is for.
            start_date (Union[Unset, datetime.date]): [readonly] The start date of the period this PayRun covers
            end_date (Union[Unset, datetime.date]): [readonly] The end date of the period this PayRun covers
            payment_date (Union[Unset, datetime.date]): [readonly] The intended date that Employees will be paid, although
                this can be changed on a per PayRunEntry basis
            employee_count (Union[Unset, int]): [readonly] The number of Employees included in this PayRun (including any
                CIS Subcontractors)
            sub_contractor_count (Union[Unset, int]): [readonly] The number of CIS Subcontractors included in this PayRun
            totals (Union[Unset, PayRunTotals]): Used to represent totals for a PayRun or PayRunEntry.
                If a value is 0 then it will not be shown in the JSON.
            state (Union[Unset, PayRunState]): The state of the payrun. You would set this value when updating a payrun to
                finalise or re-open it.
                Other states are used with Bureau functionality which isn't currently generally available.
            is_closed (Union[Unset, bool]): [readonly] Set to True if the PayRun is Finalised and changes can no longer be
                made
            date_closed (Union[Unset, None, datetime.datetime]):
            auto_pilot_close_date (Union[Unset, None, datetime.date]): [readonly] If AutoPilot is enabled in the
                AutomationSettings for the Employer then this property will tell you when
                the payrun will be automatically closed
            entries (Union[Unset, None, List[Item]]): [readonly] The PayRunEntries that make up this PayRun.
                This is populate automatically when you start a PayRun.
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    tax_month: Union[Unset, int] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET
    employee_count: Union[Unset, int] = UNSET
    sub_contractor_count: Union[Unset, int] = UNSET
    totals: Union[Unset, PayRunTotals] = UNSET
    state: Union[Unset, PayRunState] = UNSET
    is_closed: Union[Unset, bool] = UNSET
    date_closed: Union[Unset, None, datetime.datetime] = UNSET
    auto_pilot_close_date: Union[Unset, None, datetime.date] = UNSET
    entries: Union[Unset, None, List[Item]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        tax_month = self.tax_month
        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()

        employee_count = self.employee_count
        sub_contractor_count = self.sub_contractor_count
        totals: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals, Unset):
            totals = self.totals.to_dict()

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        is_closed = self.is_closed
        date_closed: Union[Unset, None, str] = UNSET
        if not isinstance(self.date_closed, Unset):
            date_closed = self.date_closed.isoformat() if self.date_closed else None

        auto_pilot_close_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.auto_pilot_close_date, Unset):
            auto_pilot_close_date = (
                self.auto_pilot_close_date.isoformat()
                if self.auto_pilot_close_date
                else None
            )

        entries: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            if self.entries is None:
                entries = None
            else:
                entries = []
                for entries_item_data in self.entries:
                    entries_item = entries_item_data.to_dict()

                    entries.append(entries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if tax_month is not UNSET:
            field_dict["taxMonth"] = tax_month
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if sub_contractor_count is not UNSET:
            field_dict["subContractorCount"] = sub_contractor_count
        if totals is not UNSET:
            field_dict["totals"] = totals
        if state is not UNSET:
            field_dict["state"] = state
        if is_closed is not UNSET:
            field_dict["isClosed"] = is_closed
        if date_closed is not UNSET:
            field_dict["dateClosed"] = date_closed
        if auto_pilot_close_date is not UNSET:
            field_dict["autoPilotCloseDate"] = auto_pilot_close_date
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        tax_month = d.pop("taxMonth", UNSET)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

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

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

        employee_count = d.pop("employeeCount", UNSET)

        sub_contractor_count = d.pop("subContractorCount", UNSET)

        _totals = d.pop("totals", UNSET)
        totals: Union[Unset, PayRunTotals]
        if isinstance(_totals, Unset):
            totals = UNSET
        else:
            totals = PayRunTotals.from_dict(_totals)

        _state = d.pop("state", UNSET)
        state: Union[Unset, PayRunState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = PayRunState(_state)

        is_closed = d.pop("isClosed", UNSET)

        _date_closed = d.pop("dateClosed", UNSET)
        date_closed: Union[Unset, None, datetime.datetime]
        if _date_closed is None:
            date_closed = None
        elif isinstance(_date_closed, Unset):
            date_closed = UNSET
        else:
            date_closed = isoparse(_date_closed)

        _auto_pilot_close_date = d.pop("autoPilotCloseDate", UNSET)
        auto_pilot_close_date: Union[Unset, None, datetime.date]
        if _auto_pilot_close_date is None:
            auto_pilot_close_date = None
        elif isinstance(_auto_pilot_close_date, Unset):
            auto_pilot_close_date = UNSET
        else:
            auto_pilot_close_date = isoparse(_auto_pilot_close_date).date()

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = Item.from_dict(entries_item_data)

            entries.append(entries_item)

        pay_run = cls(
            tax_year=tax_year,
            tax_month=tax_month,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
            start_date=start_date,
            end_date=end_date,
            payment_date=payment_date,
            employee_count=employee_count,
            sub_contractor_count=sub_contractor_count,
            totals=totals,
            state=state,
            is_closed=is_closed,
            date_closed=date_closed,
            auto_pilot_close_date=auto_pilot_close_date,
            entries=entries,
        )

        return pay_run
