import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.pay_run import PayRun
from ..models.recoverable_amounts import RecoverableAmounts
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="CostAnalysisReport")


@attr.s(auto_attribs=True)
class CostAnalysisReport:
    """
    Attributes:
        single_payrun (Union[Unset, PayRun]): This model is right at the very heart of the software.
            There is a PayRun for each period in which people are paid.
        total_pay (Union[Unset, float]):
        pension (Union[Unset, float]):
        aeo_fees (Union[Unset, float]):
        total_cost (Union[Unset, float]):
        employer_nic (Union[Unset, float]):
        net_payroll_cost (Union[Unset, float]):
        male_count (Union[Unset, int]):
        female_count (Union[Unset, int]):
        leaver_count (Union[Unset, int]):
        joiner_count (Union[Unset, int]):
        payment_after_leaving_count (Union[Unset, int]):
        recoverable_amounts (Union[Unset, RecoverableAmounts]):
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

    single_payrun: Union[Unset, PayRun] = UNSET
    total_pay: Union[Unset, float] = UNSET
    pension: Union[Unset, float] = UNSET
    aeo_fees: Union[Unset, float] = UNSET
    total_cost: Union[Unset, float] = UNSET
    employer_nic: Union[Unset, float] = UNSET
    net_payroll_cost: Union[Unset, float] = UNSET
    male_count: Union[Unset, int] = UNSET
    female_count: Union[Unset, int] = UNSET
    leaver_count: Union[Unset, int] = UNSET
    joiner_count: Union[Unset, int] = UNSET
    payment_after_leaving_count: Union[Unset, int] = UNSET
    recoverable_amounts: Union[Unset, RecoverableAmounts] = UNSET
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
        single_payrun: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.single_payrun, Unset):
            single_payrun = self.single_payrun.to_dict()

        total_pay = self.total_pay
        pension = self.pension
        aeo_fees = self.aeo_fees
        total_cost = self.total_cost
        employer_nic = self.employer_nic
        net_payroll_cost = self.net_payroll_cost
        male_count = self.male_count
        female_count = self.female_count
        leaver_count = self.leaver_count
        joiner_count = self.joiner_count
        payment_after_leaving_count = self.payment_after_leaving_count
        recoverable_amounts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recoverable_amounts, Unset):
            recoverable_amounts = self.recoverable_amounts.to_dict()

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
        if single_payrun is not UNSET:
            field_dict["singlePayrun"] = single_payrun
        if total_pay is not UNSET:
            field_dict["totalPay"] = total_pay
        if pension is not UNSET:
            field_dict["pension"] = pension
        if aeo_fees is not UNSET:
            field_dict["aeoFees"] = aeo_fees
        if total_cost is not UNSET:
            field_dict["totalCost"] = total_cost
        if employer_nic is not UNSET:
            field_dict["employerNic"] = employer_nic
        if net_payroll_cost is not UNSET:
            field_dict["netPayrollCost"] = net_payroll_cost
        if male_count is not UNSET:
            field_dict["maleCount"] = male_count
        if female_count is not UNSET:
            field_dict["femaleCount"] = female_count
        if leaver_count is not UNSET:
            field_dict["leaverCount"] = leaver_count
        if joiner_count is not UNSET:
            field_dict["joinerCount"] = joiner_count
        if payment_after_leaving_count is not UNSET:
            field_dict["paymentAfterLeavingCount"] = payment_after_leaving_count
        if recoverable_amounts is not UNSET:
            field_dict["recoverableAmounts"] = recoverable_amounts
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
        _single_payrun = d.pop("singlePayrun", UNSET)
        single_payrun: Union[Unset, PayRun]
        if isinstance(_single_payrun, Unset):
            single_payrun = UNSET
        else:
            single_payrun = PayRun.from_dict(_single_payrun)

        total_pay = d.pop("totalPay", UNSET)

        pension = d.pop("pension", UNSET)

        aeo_fees = d.pop("aeoFees", UNSET)

        total_cost = d.pop("totalCost", UNSET)

        employer_nic = d.pop("employerNic", UNSET)

        net_payroll_cost = d.pop("netPayrollCost", UNSET)

        male_count = d.pop("maleCount", UNSET)

        female_count = d.pop("femaleCount", UNSET)

        leaver_count = d.pop("leaverCount", UNSET)

        joiner_count = d.pop("joinerCount", UNSET)

        payment_after_leaving_count = d.pop("paymentAfterLeavingCount", UNSET)

        _recoverable_amounts = d.pop("recoverableAmounts", UNSET)
        recoverable_amounts: Union[Unset, RecoverableAmounts]
        if isinstance(_recoverable_amounts, Unset):
            recoverable_amounts = UNSET
        else:
            recoverable_amounts = RecoverableAmounts.from_dict(_recoverable_amounts)

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

        cost_analysis_report = cls(
            single_payrun=single_payrun,
            total_pay=total_pay,
            pension=pension,
            aeo_fees=aeo_fees,
            total_cost=total_cost,
            employer_nic=employer_nic,
            net_payroll_cost=net_payroll_cost,
            male_count=male_count,
            female_count=female_count,
            leaver_count=leaver_count,
            joiner_count=joiner_count,
            payment_after_leaving_count=payment_after_leaving_count,
            recoverable_amounts=recoverable_amounts,
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

        return cost_analysis_report
