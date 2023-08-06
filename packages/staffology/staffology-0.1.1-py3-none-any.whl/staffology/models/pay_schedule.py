import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.pay_run import PayRun
from ..models.pay_schedule_period_events_config import PaySchedulePeriodEventsConfig
from ..models.payment_date_type import PaymentDateType
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaySchedule")


@attr.s(auto_attribs=True)
class PaySchedule:
    """
    Attributes:
        name (Union[Unset, None, str]): A descriptive name for this PaySchedule
        ordinal (Union[Unset, int]): [readonly] Indicates whether this is first, second, third (etc) PaySchedule for
            this PayPeriod.
        tax_year (Union[Unset, TaxYear]):
        pay_period (Union[Unset, PayPeriods]):
        first_period_end_date (Union[Unset, datetime.date]): The last day of the first pay period
        first_payment_date (Union[Unset, datetime.date]): The first payment date
        payment_date_type (Union[Unset, PaymentDateType]):
        period_lengths (Union[Unset, None, List[int]]): Only applicable for PayPeriod of Custom. Defines the length of
            each period
        high_gross_pay (Union[Unset, float]): A gross pay amount considered high for this PaySchedule
        high_net_pay (Union[Unset, float]): A net pay amount considered high for this PaySchedule
        period_events_config (Union[Unset, None, PaySchedulePeriodEventsConfig]): Only applicable if Bureau
            functionality is enabled. Defines the number of days each event occurs before the Payment Date.
        has_open_pay_run_period (Union[Unset, bool]): [readonly] Will be true if the employer currently has an open
            PayRun for this PayPeriod
        last_period_end_date (Union[Unset, None, datetime.date]): [readonly] The end date of the most recent PayRun on
            this schedule
        last_period_number (Union[Unset, None, int]): [readonly] The period number of the most recent PayRun on this
            schedule
        employee_count (Union[Unset, int]): [readonly] The number of employees paid with this PaySchedule
        is_required (Union[Unset, bool]): [readonly] Whether or not this PaySchedule is required for the employer, ie:
            they have employees to be paid on this PaySchedule
        is_configured (Union[Unset, bool]): [readonly] Whether or not this PaySchedule has been configured and is ready
            for use
        is_year_completed (Union[Unset, bool]): [readonly] Returns true if all PayRuns for this PaySchedule in the
            TaxYear have been completed
        year_end_tasks (Union[Unset, None, List[str]]): [readonly] A list of actions that need to be completed for this
            PaySchedule before this TaxYear can be finalised
        pay_runs (Union[Unset, None, List[Item]]): [readonly] Details of PayRuns for this PaySchedule
        current_pay_run (Union[Unset, Item]):
        next_pay_run (Union[Unset, PayRun]): This model is right at the very heart of the software.
            There is a PayRun for each period in which people are paid.
    """

    name: Union[Unset, None, str] = UNSET
    ordinal: Union[Unset, int] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    first_period_end_date: Union[Unset, datetime.date] = UNSET
    first_payment_date: Union[Unset, datetime.date] = UNSET
    payment_date_type: Union[Unset, PaymentDateType] = UNSET
    period_lengths: Union[Unset, None, List[int]] = UNSET
    high_gross_pay: Union[Unset, float] = UNSET
    high_net_pay: Union[Unset, float] = UNSET
    period_events_config: Union[Unset, None, PaySchedulePeriodEventsConfig] = UNSET
    has_open_pay_run_period: Union[Unset, bool] = UNSET
    last_period_end_date: Union[Unset, None, datetime.date] = UNSET
    last_period_number: Union[Unset, None, int] = UNSET
    employee_count: Union[Unset, int] = UNSET
    is_required: Union[Unset, bool] = UNSET
    is_configured: Union[Unset, bool] = UNSET
    is_year_completed: Union[Unset, bool] = UNSET
    year_end_tasks: Union[Unset, None, List[str]] = UNSET
    pay_runs: Union[Unset, None, List[Item]] = UNSET
    current_pay_run: Union[Unset, Item] = UNSET
    next_pay_run: Union[Unset, PayRun] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        ordinal = self.ordinal
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        first_period_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.first_period_end_date, Unset):
            first_period_end_date = self.first_period_end_date.isoformat()

        first_payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.first_payment_date, Unset):
            first_payment_date = self.first_payment_date.isoformat()

        payment_date_type: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date_type, Unset):
            payment_date_type = self.payment_date_type.value

        period_lengths: Union[Unset, None, List[int]] = UNSET
        if not isinstance(self.period_lengths, Unset):
            if self.period_lengths is None:
                period_lengths = None
            else:
                period_lengths = self.period_lengths

        high_gross_pay = self.high_gross_pay
        high_net_pay = self.high_net_pay
        period_events_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.period_events_config, Unset):
            period_events_config = (
                self.period_events_config.to_dict()
                if self.period_events_config
                else None
            )

        has_open_pay_run_period = self.has_open_pay_run_period
        last_period_end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_period_end_date, Unset):
            last_period_end_date = (
                self.last_period_end_date.isoformat()
                if self.last_period_end_date
                else None
            )

        last_period_number = self.last_period_number
        employee_count = self.employee_count
        is_required = self.is_required
        is_configured = self.is_configured
        is_year_completed = self.is_year_completed
        year_end_tasks: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.year_end_tasks, Unset):
            if self.year_end_tasks is None:
                year_end_tasks = None
            else:
                year_end_tasks = self.year_end_tasks

        pay_runs: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pay_runs, Unset):
            if self.pay_runs is None:
                pay_runs = None
            else:
                pay_runs = []
                for pay_runs_item_data in self.pay_runs:
                    pay_runs_item = pay_runs_item_data.to_dict()

                    pay_runs.append(pay_runs_item)

        current_pay_run: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_pay_run, Unset):
            current_pay_run = self.current_pay_run.to_dict()

        next_pay_run: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_pay_run, Unset):
            next_pay_run = self.next_pay_run.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if first_period_end_date is not UNSET:
            field_dict["firstPeriodEndDate"] = first_period_end_date
        if first_payment_date is not UNSET:
            field_dict["firstPaymentDate"] = first_payment_date
        if payment_date_type is not UNSET:
            field_dict["paymentDateType"] = payment_date_type
        if period_lengths is not UNSET:
            field_dict["periodLengths"] = period_lengths
        if high_gross_pay is not UNSET:
            field_dict["highGrossPay"] = high_gross_pay
        if high_net_pay is not UNSET:
            field_dict["highNetPay"] = high_net_pay
        if period_events_config is not UNSET:
            field_dict["periodEventsConfig"] = period_events_config
        if has_open_pay_run_period is not UNSET:
            field_dict["hasOpenPayRunPeriod"] = has_open_pay_run_period
        if last_period_end_date is not UNSET:
            field_dict["lastPeriodEndDate"] = last_period_end_date
        if last_period_number is not UNSET:
            field_dict["lastPeriodNumber"] = last_period_number
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if is_configured is not UNSET:
            field_dict["isConfigured"] = is_configured
        if is_year_completed is not UNSET:
            field_dict["isYearCompleted"] = is_year_completed
        if year_end_tasks is not UNSET:
            field_dict["yearEndTasks"] = year_end_tasks
        if pay_runs is not UNSET:
            field_dict["payRuns"] = pay_runs
        if current_pay_run is not UNSET:
            field_dict["currentPayRun"] = current_pay_run
        if next_pay_run is not UNSET:
            field_dict["nextPayRun"] = next_pay_run

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        ordinal = d.pop("ordinal", UNSET)

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

        _first_period_end_date = d.pop("firstPeriodEndDate", UNSET)
        first_period_end_date: Union[Unset, datetime.date]
        if isinstance(_first_period_end_date, Unset):
            first_period_end_date = UNSET
        else:
            first_period_end_date = isoparse(_first_period_end_date).date()

        _first_payment_date = d.pop("firstPaymentDate", UNSET)
        first_payment_date: Union[Unset, datetime.date]
        if isinstance(_first_payment_date, Unset):
            first_payment_date = UNSET
        else:
            first_payment_date = isoparse(_first_payment_date).date()

        _payment_date_type = d.pop("paymentDateType", UNSET)
        payment_date_type: Union[Unset, PaymentDateType]
        if isinstance(_payment_date_type, Unset):
            payment_date_type = UNSET
        else:
            payment_date_type = PaymentDateType(_payment_date_type)

        period_lengths = cast(List[int], d.pop("periodLengths", UNSET))

        high_gross_pay = d.pop("highGrossPay", UNSET)

        high_net_pay = d.pop("highNetPay", UNSET)

        _period_events_config = d.pop("periodEventsConfig", UNSET)
        period_events_config: Union[Unset, None, PaySchedulePeriodEventsConfig]
        if _period_events_config is None:
            period_events_config = None
        elif isinstance(_period_events_config, Unset):
            period_events_config = UNSET
        else:
            period_events_config = PaySchedulePeriodEventsConfig.from_dict(
                _period_events_config
            )

        has_open_pay_run_period = d.pop("hasOpenPayRunPeriod", UNSET)

        _last_period_end_date = d.pop("lastPeriodEndDate", UNSET)
        last_period_end_date: Union[Unset, None, datetime.date]
        if _last_period_end_date is None:
            last_period_end_date = None
        elif isinstance(_last_period_end_date, Unset):
            last_period_end_date = UNSET
        else:
            last_period_end_date = isoparse(_last_period_end_date).date()

        last_period_number = d.pop("lastPeriodNumber", UNSET)

        employee_count = d.pop("employeeCount", UNSET)

        is_required = d.pop("isRequired", UNSET)

        is_configured = d.pop("isConfigured", UNSET)

        is_year_completed = d.pop("isYearCompleted", UNSET)

        year_end_tasks = cast(List[str], d.pop("yearEndTasks", UNSET))

        pay_runs = []
        _pay_runs = d.pop("payRuns", UNSET)
        for pay_runs_item_data in _pay_runs or []:
            pay_runs_item = Item.from_dict(pay_runs_item_data)

            pay_runs.append(pay_runs_item)

        _current_pay_run = d.pop("currentPayRun", UNSET)
        current_pay_run: Union[Unset, Item]
        if isinstance(_current_pay_run, Unset):
            current_pay_run = UNSET
        else:
            current_pay_run = Item.from_dict(_current_pay_run)

        _next_pay_run = d.pop("nextPayRun", UNSET)
        next_pay_run: Union[Unset, PayRun]
        if isinstance(_next_pay_run, Unset):
            next_pay_run = UNSET
        else:
            next_pay_run = PayRun.from_dict(_next_pay_run)

        pay_schedule = cls(
            name=name,
            ordinal=ordinal,
            tax_year=tax_year,
            pay_period=pay_period,
            first_period_end_date=first_period_end_date,
            first_payment_date=first_payment_date,
            payment_date_type=payment_date_type,
            period_lengths=period_lengths,
            high_gross_pay=high_gross_pay,
            high_net_pay=high_net_pay,
            period_events_config=period_events_config,
            has_open_pay_run_period=has_open_pay_run_period,
            last_period_end_date=last_period_end_date,
            last_period_number=last_period_number,
            employee_count=employee_count,
            is_required=is_required,
            is_configured=is_configured,
            is_year_completed=is_year_completed,
            year_end_tasks=year_end_tasks,
            pay_runs=pay_runs,
            current_pay_run=current_pay_run,
            next_pay_run=next_pay_run,
        )

        return pay_schedule
