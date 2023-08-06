import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.furlough_report_line import FurloughReportLine
from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="FurloughReport")


@attr.s(auto_attribs=True)
class FurloughReport:
    """
    Attributes:
        max_claim_per_employee (Union[Unset, float]):
        percentage_of_ni_and_pension_to_claim (Union[Unset, float]):
        govt_contrib_rate (Union[Unset, float]):
        company_name (Union[Unset, None, str]):
        employer_reference (Union[Unset, None, str]):
        company_crn (Union[Unset, None, str]):
        ct_utr (Union[Unset, None, str]):
        sa_utr (Union[Unset, None, str]):
        claim_period_start_date (Union[Unset, datetime.date]):
        claim_period_end_date (Union[Unset, datetime.date]):
        number_of_employees_being_furloughed (Union[Unset, int]):
        total_claim_amount (Union[Unset, float]):
        total_gross_pay (Union[Unset, float]):
        amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period (Union[Unset, float]):
        amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees (Union[Unset, float]):
        amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees (Union[Unset, float]):
        lines (Union[Unset, None, List[FurloughReportLine]]):
        bank_account_number (Union[Unset, None, str]):
        bank_sort_code (Union[Unset, None, str]):
        bank_account_holders_first_name (Union[Unset, None, str]):
        bank_account_holders_last_name (Union[Unset, None, str]):
        bank_account_holders_address (Union[Unset, None, str]):
        building_society_roll_number (Union[Unset, None, str]):
        company_address (Union[Unset, None, str]):
        contact_name (Union[Unset, None, str]):
        contact_number (Union[Unset, None, str]):
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

    max_claim_per_employee: Union[Unset, float] = UNSET
    percentage_of_ni_and_pension_to_claim: Union[Unset, float] = UNSET
    govt_contrib_rate: Union[Unset, float] = UNSET
    company_name: Union[Unset, None, str] = UNSET
    employer_reference: Union[Unset, None, str] = UNSET
    company_crn: Union[Unset, None, str] = UNSET
    ct_utr: Union[Unset, None, str] = UNSET
    sa_utr: Union[Unset, None, str] = UNSET
    claim_period_start_date: Union[Unset, datetime.date] = UNSET
    claim_period_end_date: Union[Unset, datetime.date] = UNSET
    number_of_employees_being_furloughed: Union[Unset, int] = UNSET
    total_claim_amount: Union[Unset, float] = UNSET
    total_gross_pay: Union[Unset, float] = UNSET
    amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period: Union[
        Unset, float
    ] = UNSET
    amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees: Union[
        Unset, float
    ] = UNSET
    amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees: Union[
        Unset, float
    ] = UNSET
    lines: Union[Unset, None, List[FurloughReportLine]] = UNSET
    bank_account_number: Union[Unset, None, str] = UNSET
    bank_sort_code: Union[Unset, None, str] = UNSET
    bank_account_holders_first_name: Union[Unset, None, str] = UNSET
    bank_account_holders_last_name: Union[Unset, None, str] = UNSET
    bank_account_holders_address: Union[Unset, None, str] = UNSET
    building_society_roll_number: Union[Unset, None, str] = UNSET
    company_address: Union[Unset, None, str] = UNSET
    contact_name: Union[Unset, None, str] = UNSET
    contact_number: Union[Unset, None, str] = UNSET
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
        max_claim_per_employee = self.max_claim_per_employee
        percentage_of_ni_and_pension_to_claim = (
            self.percentage_of_ni_and_pension_to_claim
        )
        govt_contrib_rate = self.govt_contrib_rate
        company_name = self.company_name
        employer_reference = self.employer_reference
        company_crn = self.company_crn
        ct_utr = self.ct_utr
        sa_utr = self.sa_utr
        claim_period_start_date: Union[Unset, str] = UNSET
        if not isinstance(self.claim_period_start_date, Unset):
            claim_period_start_date = self.claim_period_start_date.isoformat()

        claim_period_end_date: Union[Unset, str] = UNSET
        if not isinstance(self.claim_period_end_date, Unset):
            claim_period_end_date = self.claim_period_end_date.isoformat()

        number_of_employees_being_furloughed = self.number_of_employees_being_furloughed
        total_claim_amount = self.total_claim_amount
        total_gross_pay = self.total_gross_pay
        amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period = (
            self.amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period
        )
        amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees = (
            self.amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees
        )
        amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees = (
            self.amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees
        )
        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        bank_account_number = self.bank_account_number
        bank_sort_code = self.bank_sort_code
        bank_account_holders_first_name = self.bank_account_holders_first_name
        bank_account_holders_last_name = self.bank_account_holders_last_name
        bank_account_holders_address = self.bank_account_holders_address
        building_society_roll_number = self.building_society_roll_number
        company_address = self.company_address
        contact_name = self.contact_name
        contact_number = self.contact_number
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
        if max_claim_per_employee is not UNSET:
            field_dict["maxClaimPerEmployee"] = max_claim_per_employee
        if percentage_of_ni_and_pension_to_claim is not UNSET:
            field_dict[
                "percentageOfNIAndPensionToClaim"
            ] = percentage_of_ni_and_pension_to_claim
        if govt_contrib_rate is not UNSET:
            field_dict["govtContribRate"] = govt_contrib_rate
        if company_name is not UNSET:
            field_dict["companyName"] = company_name
        if employer_reference is not UNSET:
            field_dict["employerReference"] = employer_reference
        if company_crn is not UNSET:
            field_dict["companyCrn"] = company_crn
        if ct_utr is not UNSET:
            field_dict["ctUtr"] = ct_utr
        if sa_utr is not UNSET:
            field_dict["saUtr"] = sa_utr
        if claim_period_start_date is not UNSET:
            field_dict["claimPeriodStartDate"] = claim_period_start_date
        if claim_period_end_date is not UNSET:
            field_dict["claimPeriodEndDate"] = claim_period_end_date
        if number_of_employees_being_furloughed is not UNSET:
            field_dict[
                "numberOfEmployeesBeingFurloughed"
            ] = number_of_employees_being_furloughed
        if total_claim_amount is not UNSET:
            field_dict["totalClaimAmount"] = total_claim_amount
        if total_gross_pay is not UNSET:
            field_dict["totalGrossPay"] = total_gross_pay
        if (
            amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period
            is not UNSET
        ):
            field_dict[
                "amountClaimedForGrossPayToEmployeesOnFurloughForThePeriod"
            ] = amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period
        if (
            amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees
            is not UNSET
        ):
            field_dict[
                "amountClaimedForEmployerNICsContributionsForFurloughedEmployees"
            ] = amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees
        if (
            amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees
            is not UNSET
        ):
            field_dict[
                "amountClaimedForEmployersAutoEnrolmentPensionCostsForFurloughedEmployees"
            ] = amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees
        if lines is not UNSET:
            field_dict["lines"] = lines
        if bank_account_number is not UNSET:
            field_dict["bankAccountNumber"] = bank_account_number
        if bank_sort_code is not UNSET:
            field_dict["bankSortCode"] = bank_sort_code
        if bank_account_holders_first_name is not UNSET:
            field_dict["bankAccountHoldersFirstName"] = bank_account_holders_first_name
        if bank_account_holders_last_name is not UNSET:
            field_dict["bankAccountHoldersLastName"] = bank_account_holders_last_name
        if bank_account_holders_address is not UNSET:
            field_dict["bankAccountHoldersAddress"] = bank_account_holders_address
        if building_society_roll_number is not UNSET:
            field_dict["buildingSocietyRollNumber"] = building_society_roll_number
        if company_address is not UNSET:
            field_dict["companyAddress"] = company_address
        if contact_name is not UNSET:
            field_dict["contactName"] = contact_name
        if contact_number is not UNSET:
            field_dict["contactNumber"] = contact_number
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
        max_claim_per_employee = d.pop("maxClaimPerEmployee", UNSET)

        percentage_of_ni_and_pension_to_claim = d.pop(
            "percentageOfNIAndPensionToClaim", UNSET
        )

        govt_contrib_rate = d.pop("govtContribRate", UNSET)

        company_name = d.pop("companyName", UNSET)

        employer_reference = d.pop("employerReference", UNSET)

        company_crn = d.pop("companyCrn", UNSET)

        ct_utr = d.pop("ctUtr", UNSET)

        sa_utr = d.pop("saUtr", UNSET)

        _claim_period_start_date = d.pop("claimPeriodStartDate", UNSET)
        claim_period_start_date: Union[Unset, datetime.date]
        if isinstance(_claim_period_start_date, Unset):
            claim_period_start_date = UNSET
        else:
            claim_period_start_date = isoparse(_claim_period_start_date).date()

        _claim_period_end_date = d.pop("claimPeriodEndDate", UNSET)
        claim_period_end_date: Union[Unset, datetime.date]
        if isinstance(_claim_period_end_date, Unset):
            claim_period_end_date = UNSET
        else:
            claim_period_end_date = isoparse(_claim_period_end_date).date()

        number_of_employees_being_furloughed = d.pop(
            "numberOfEmployeesBeingFurloughed", UNSET
        )

        total_claim_amount = d.pop("totalClaimAmount", UNSET)

        total_gross_pay = d.pop("totalGrossPay", UNSET)

        amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period = d.pop(
            "amountClaimedForGrossPayToEmployeesOnFurloughForThePeriod", UNSET
        )

        amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees = (
            d.pop(
                "amountClaimedForEmployerNICsContributionsForFurloughedEmployees", UNSET
            )
        )

        amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees = d.pop(
            "amountClaimedForEmployersAutoEnrolmentPensionCostsForFurloughedEmployees",
            UNSET,
        )

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = FurloughReportLine.from_dict(lines_item_data)

            lines.append(lines_item)

        bank_account_number = d.pop("bankAccountNumber", UNSET)

        bank_sort_code = d.pop("bankSortCode", UNSET)

        bank_account_holders_first_name = d.pop("bankAccountHoldersFirstName", UNSET)

        bank_account_holders_last_name = d.pop("bankAccountHoldersLastName", UNSET)

        bank_account_holders_address = d.pop("bankAccountHoldersAddress", UNSET)

        building_society_roll_number = d.pop("buildingSocietyRollNumber", UNSET)

        company_address = d.pop("companyAddress", UNSET)

        contact_name = d.pop("contactName", UNSET)

        contact_number = d.pop("contactNumber", UNSET)

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

        furlough_report = cls(
            max_claim_per_employee=max_claim_per_employee,
            percentage_of_ni_and_pension_to_claim=percentage_of_ni_and_pension_to_claim,
            govt_contrib_rate=govt_contrib_rate,
            company_name=company_name,
            employer_reference=employer_reference,
            company_crn=company_crn,
            ct_utr=ct_utr,
            sa_utr=sa_utr,
            claim_period_start_date=claim_period_start_date,
            claim_period_end_date=claim_period_end_date,
            number_of_employees_being_furloughed=number_of_employees_being_furloughed,
            total_claim_amount=total_claim_amount,
            total_gross_pay=total_gross_pay,
            amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period=amount_claimed_for_gross_pay_to_employees_on_furlough_for_the_period,
            amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees=amount_claimed_for_employer_ni_cs_contributions_for_furloughed_employees,
            amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees=amount_claimed_for_employers_auto_enrolment_pension_costs_for_furloughed_employees,
            lines=lines,
            bank_account_number=bank_account_number,
            bank_sort_code=bank_sort_code,
            bank_account_holders_first_name=bank_account_holders_first_name,
            bank_account_holders_last_name=bank_account_holders_last_name,
            bank_account_holders_address=bank_account_holders_address,
            building_society_roll_number=building_society_roll_number,
            company_address=company_address,
            contact_name=contact_name,
            contact_number=contact_number,
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

        return furlough_report
