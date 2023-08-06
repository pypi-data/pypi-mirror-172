import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.hmrc_payment import HmrcPayment
from ..models.item import Item
from ..models.pay_run import PayRun
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="HmrcLiability")


@attr.s(auto_attribs=True)
class HmrcLiability:
    """
    Attributes:
        title (Union[Unset, None, str]): [readonly] A descriptive name for the Period
        tax_year (Union[Unset, TaxYear]):
        period_ending (Union[Unset, datetime.date]): [readonly]
        period_complete (Union[Unset, bool]): [readonly] Indicates whether or not all PayRuns for this period have been
            completed
        recoverable_amounts_eps_created (Union[Unset, bool]): [readonly] If there are recoverable amount present (ie,
            SMP) and the Period is complete then this field Indicates
            whether or not an EPS has been created up to the final tax month of this period to declare
            the recoverable amounts
        apprenticeship_levy_eps_created (Union[Unset, bool]): [readonly] If there is an Apprenticeship LEvy amount
            present and the Period is complete then this field Indicates
            whether or not an EPS has been created up to the final tax month of this period to declare
            the amount
        pay_runs (Union[Unset, None, List[PayRun]]):
        tax (Union[Unset, float]): [readonly] Amount due to HMRC for PAYE in period
        cis_deductions (Union[Unset, float]): [readonly] Amount due to HMRC for CIS Deductions made in period
        postgrad_loan_deductions (Union[Unset, float]): [readonly] Amount due to HMRC for Postgrad Loan Deductions made
            in period
        student_loan_deductions (Union[Unset, float]): [readonly] Amount due to HMRC for Student Loan Deductions made in
            period
        employee_nic (Union[Unset, float]): [readonly] Amount due to HMRC for Employee NIC Contributions withheld in
            period
        employer_nic (Union[Unset, float]): [readonly] Amount due to HMRC for Employer NIC Contributions due on payments
            in period
        real_time_class_1a_nic (Union[Unset, float]): [readonly] Amount due to HMRC for Employer NIC Contributions due
            on payments in period
        smp (Union[Unset, float]): [readonly] SMP recovered from payments in period
        smp_nic (Union[Unset, float]): [readonly] SMP NIC Compensation for period
        spp (Union[Unset, float]): [readonly] SPP recovered from payments in period
        spp_nic (Union[Unset, float]): [readonly] SPP Nic Compensation for period
        sap (Union[Unset, float]): [readonly] SAP recovered from payments in period
        sap_nic (Union[Unset, float]): [readonly] SAP Nic Compensation for period
        shpp (Union[Unset, float]): [readonly] ShPP recovered from payments in period
        shpp_nic (Union[Unset, float]): [readonly] ShPP Nic Compensation for period
        spbp (Union[Unset, float]): [readonly] SPBP recovered from payments in period
        spbp_nic (Union[Unset, float]): [readonly] SPBP Nic Compensation for period
        eligible_for_employment_allowance (Union[Unset, bool]): [readonly] Indicates whether the Employer settings say
            the Employer is eligible for Employment Allowance
        employment_allowance_claim (Union[Unset, float]): Amount to claim with respect to the Employment Allowance
        employment_allowance_claim_auto (Union[Unset, bool]): If set to true, we'll automatically claim the maximum
            allowed.
            If set to false then you can enter your own value.
            If EligibleForEmploymentAllowance is false then the EmploymentAllowanceClaim will
            always be overwritten with a zero value regardless of this property
        liable_for_apprenticeship_levy (Union[Unset, bool]): [readonly] Indicates whether the Employer settings say the
            Employer is liable for the Apprenticeship Levy
        apprenticeship_levy (Union[Unset, float]): Amount due with respect to the Apprenticeship Levy
        apprenticeship_levy_auto (Union[Unset, bool]): If set to true, we'll automatically calculate your liability
            If set to false then you can enter your own value.
            If LiableForApprenticeshipLevy is false then the ApprenticeshipLevy will
            always be overwritten with a zero value regardless of this property
        liability_arising_in_period (Union[Unset, float]): [readonly] Total Liability (before any deductions) arising in
            this Period
        due_in_previous_periods (Union[Unset, float]): [readonly] Amount due to HMRC in previous periods for this Tax
            Year
        paid_in_previous_periods (Union[Unset, float]): [readonly] Amount paid to HMRC in previous periods for this Tax
            Year
        employment_allowance_claim_in_previous_periods (Union[Unset, float]): [readonly] The amount of Employment
            Allowance claimed in previous periods for this Tax Year
        received_from_hmrc_to_refund_tax (Union[Unset, float]): Any amount received from HMRC to refund Tax in Period
        received_from_hmrc_to_pay_statutory_pay (Union[Unset, float]): Any amount received from HMRC to pay Statutory
            Pay Period
        cis_deductions_suffered (Union[Unset, float]): CIS Deductions Suffered in Period
        adjustment (Union[Unset, float]): Any manual adjustment for Period
        net_liability_for_period (Union[Unset, float]): [readonly] Net Liability (including any deductions/additions)
            arising in this Period
        total_paid (Union[Unset, float]): [readonly] The total value of all payments in this period
        payments (Union[Unset, None, List[HmrcPayment]]):
        fps_list (Union[Unset, None, List[Item]]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    period_ending: Union[Unset, datetime.date] = UNSET
    period_complete: Union[Unset, bool] = UNSET
    recoverable_amounts_eps_created: Union[Unset, bool] = UNSET
    apprenticeship_levy_eps_created: Union[Unset, bool] = UNSET
    pay_runs: Union[Unset, None, List[PayRun]] = UNSET
    tax: Union[Unset, float] = UNSET
    cis_deductions: Union[Unset, float] = UNSET
    postgrad_loan_deductions: Union[Unset, float] = UNSET
    student_loan_deductions: Union[Unset, float] = UNSET
    employee_nic: Union[Unset, float] = UNSET
    employer_nic: Union[Unset, float] = UNSET
    real_time_class_1a_nic: Union[Unset, float] = UNSET
    smp: Union[Unset, float] = UNSET
    smp_nic: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    spp_nic: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    sap_nic: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    shpp_nic: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET
    spbp_nic: Union[Unset, float] = UNSET
    eligible_for_employment_allowance: Union[Unset, bool] = UNSET
    employment_allowance_claim: Union[Unset, float] = UNSET
    employment_allowance_claim_auto: Union[Unset, bool] = UNSET
    liable_for_apprenticeship_levy: Union[Unset, bool] = UNSET
    apprenticeship_levy: Union[Unset, float] = UNSET
    apprenticeship_levy_auto: Union[Unset, bool] = UNSET
    liability_arising_in_period: Union[Unset, float] = UNSET
    due_in_previous_periods: Union[Unset, float] = UNSET
    paid_in_previous_periods: Union[Unset, float] = UNSET
    employment_allowance_claim_in_previous_periods: Union[Unset, float] = UNSET
    received_from_hmrc_to_refund_tax: Union[Unset, float] = UNSET
    received_from_hmrc_to_pay_statutory_pay: Union[Unset, float] = UNSET
    cis_deductions_suffered: Union[Unset, float] = UNSET
    adjustment: Union[Unset, float] = UNSET
    net_liability_for_period: Union[Unset, float] = UNSET
    total_paid: Union[Unset, float] = UNSET
    payments: Union[Unset, None, List[HmrcPayment]] = UNSET
    fps_list: Union[Unset, None, List[Item]] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        period_ending: Union[Unset, str] = UNSET
        if not isinstance(self.period_ending, Unset):
            period_ending = self.period_ending.isoformat()

        period_complete = self.period_complete
        recoverable_amounts_eps_created = self.recoverable_amounts_eps_created
        apprenticeship_levy_eps_created = self.apprenticeship_levy_eps_created
        pay_runs: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pay_runs, Unset):
            if self.pay_runs is None:
                pay_runs = None
            else:
                pay_runs = []
                for pay_runs_item_data in self.pay_runs:
                    pay_runs_item = pay_runs_item_data.to_dict()

                    pay_runs.append(pay_runs_item)

        tax = self.tax
        cis_deductions = self.cis_deductions
        postgrad_loan_deductions = self.postgrad_loan_deductions
        student_loan_deductions = self.student_loan_deductions
        employee_nic = self.employee_nic
        employer_nic = self.employer_nic
        real_time_class_1a_nic = self.real_time_class_1a_nic
        smp = self.smp
        smp_nic = self.smp_nic
        spp = self.spp
        spp_nic = self.spp_nic
        sap = self.sap
        sap_nic = self.sap_nic
        shpp = self.shpp
        shpp_nic = self.shpp_nic
        spbp = self.spbp
        spbp_nic = self.spbp_nic
        eligible_for_employment_allowance = self.eligible_for_employment_allowance
        employment_allowance_claim = self.employment_allowance_claim
        employment_allowance_claim_auto = self.employment_allowance_claim_auto
        liable_for_apprenticeship_levy = self.liable_for_apprenticeship_levy
        apprenticeship_levy = self.apprenticeship_levy
        apprenticeship_levy_auto = self.apprenticeship_levy_auto
        liability_arising_in_period = self.liability_arising_in_period
        due_in_previous_periods = self.due_in_previous_periods
        paid_in_previous_periods = self.paid_in_previous_periods
        employment_allowance_claim_in_previous_periods = (
            self.employment_allowance_claim_in_previous_periods
        )
        received_from_hmrc_to_refund_tax = self.received_from_hmrc_to_refund_tax
        received_from_hmrc_to_pay_statutory_pay = (
            self.received_from_hmrc_to_pay_statutory_pay
        )
        cis_deductions_suffered = self.cis_deductions_suffered
        adjustment = self.adjustment
        net_liability_for_period = self.net_liability_for_period
        total_paid = self.total_paid
        payments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.payments, Unset):
            if self.payments is None:
                payments = None
            else:
                payments = []
                for payments_item_data in self.payments:
                    payments_item = payments_item_data.to_dict()

                    payments.append(payments_item)

        fps_list: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.fps_list, Unset):
            if self.fps_list is None:
                fps_list = None
            else:
                fps_list = []
                for fps_list_item_data in self.fps_list:
                    fps_list_item = fps_list_item_data.to_dict()

                    fps_list.append(fps_list_item)

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if period_ending is not UNSET:
            field_dict["periodEnding"] = period_ending
        if period_complete is not UNSET:
            field_dict["periodComplete"] = period_complete
        if recoverable_amounts_eps_created is not UNSET:
            field_dict["recoverableAmountsEpsCreated"] = recoverable_amounts_eps_created
        if apprenticeship_levy_eps_created is not UNSET:
            field_dict["apprenticeshipLevyEpsCreated"] = apprenticeship_levy_eps_created
        if pay_runs is not UNSET:
            field_dict["payRuns"] = pay_runs
        if tax is not UNSET:
            field_dict["tax"] = tax
        if cis_deductions is not UNSET:
            field_dict["cisDeductions"] = cis_deductions
        if postgrad_loan_deductions is not UNSET:
            field_dict["postgradLoanDeductions"] = postgrad_loan_deductions
        if student_loan_deductions is not UNSET:
            field_dict["studentLoanDeductions"] = student_loan_deductions
        if employee_nic is not UNSET:
            field_dict["employeeNic"] = employee_nic
        if employer_nic is not UNSET:
            field_dict["employerNic"] = employer_nic
        if real_time_class_1a_nic is not UNSET:
            field_dict["realTimeClass1ANic"] = real_time_class_1a_nic
        if smp is not UNSET:
            field_dict["smp"] = smp
        if smp_nic is not UNSET:
            field_dict["smpNic"] = smp_nic
        if spp is not UNSET:
            field_dict["spp"] = spp
        if spp_nic is not UNSET:
            field_dict["sppNic"] = spp_nic
        if sap is not UNSET:
            field_dict["sap"] = sap
        if sap_nic is not UNSET:
            field_dict["sapNic"] = sap_nic
        if shpp is not UNSET:
            field_dict["shpp"] = shpp
        if shpp_nic is not UNSET:
            field_dict["shppNic"] = shpp_nic
        if spbp is not UNSET:
            field_dict["spbp"] = spbp
        if spbp_nic is not UNSET:
            field_dict["spbpNic"] = spbp_nic
        if eligible_for_employment_allowance is not UNSET:
            field_dict[
                "eligibleForEmploymentAllowance"
            ] = eligible_for_employment_allowance
        if employment_allowance_claim is not UNSET:
            field_dict["employmentAllowanceClaim"] = employment_allowance_claim
        if employment_allowance_claim_auto is not UNSET:
            field_dict["employmentAllowanceClaimAuto"] = employment_allowance_claim_auto
        if liable_for_apprenticeship_levy is not UNSET:
            field_dict["liableForApprenticeshipLevy"] = liable_for_apprenticeship_levy
        if apprenticeship_levy is not UNSET:
            field_dict["apprenticeshipLevy"] = apprenticeship_levy
        if apprenticeship_levy_auto is not UNSET:
            field_dict["apprenticeshipLevyAuto"] = apprenticeship_levy_auto
        if liability_arising_in_period is not UNSET:
            field_dict["liabilityArisingInPeriod"] = liability_arising_in_period
        if due_in_previous_periods is not UNSET:
            field_dict["dueInPreviousPeriods"] = due_in_previous_periods
        if paid_in_previous_periods is not UNSET:
            field_dict["paidInPreviousPeriods"] = paid_in_previous_periods
        if employment_allowance_claim_in_previous_periods is not UNSET:
            field_dict[
                "employmentAllowanceClaimInPreviousPeriods"
            ] = employment_allowance_claim_in_previous_periods
        if received_from_hmrc_to_refund_tax is not UNSET:
            field_dict["receivedFromHMRCToRefundTax"] = received_from_hmrc_to_refund_tax
        if received_from_hmrc_to_pay_statutory_pay is not UNSET:
            field_dict[
                "receivedFromHMRCToPayStatutoryPay"
            ] = received_from_hmrc_to_pay_statutory_pay
        if cis_deductions_suffered is not UNSET:
            field_dict["cisDeductionsSuffered"] = cis_deductions_suffered
        if adjustment is not UNSET:
            field_dict["adjustment"] = adjustment
        if net_liability_for_period is not UNSET:
            field_dict["netLiabilityForPeriod"] = net_liability_for_period
        if total_paid is not UNSET:
            field_dict["totalPaid"] = total_paid
        if payments is not UNSET:
            field_dict["payments"] = payments
        if fps_list is not UNSET:
            field_dict["fpsList"] = fps_list
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _period_ending = d.pop("periodEnding", UNSET)
        period_ending: Union[Unset, datetime.date]
        if isinstance(_period_ending, Unset):
            period_ending = UNSET
        else:
            period_ending = isoparse(_period_ending).date()

        period_complete = d.pop("periodComplete", UNSET)

        recoverable_amounts_eps_created = d.pop("recoverableAmountsEpsCreated", UNSET)

        apprenticeship_levy_eps_created = d.pop("apprenticeshipLevyEpsCreated", UNSET)

        pay_runs = []
        _pay_runs = d.pop("payRuns", UNSET)
        for pay_runs_item_data in _pay_runs or []:
            pay_runs_item = PayRun.from_dict(pay_runs_item_data)

            pay_runs.append(pay_runs_item)

        tax = d.pop("tax", UNSET)

        cis_deductions = d.pop("cisDeductions", UNSET)

        postgrad_loan_deductions = d.pop("postgradLoanDeductions", UNSET)

        student_loan_deductions = d.pop("studentLoanDeductions", UNSET)

        employee_nic = d.pop("employeeNic", UNSET)

        employer_nic = d.pop("employerNic", UNSET)

        real_time_class_1a_nic = d.pop("realTimeClass1ANic", UNSET)

        smp = d.pop("smp", UNSET)

        smp_nic = d.pop("smpNic", UNSET)

        spp = d.pop("spp", UNSET)

        spp_nic = d.pop("sppNic", UNSET)

        sap = d.pop("sap", UNSET)

        sap_nic = d.pop("sapNic", UNSET)

        shpp = d.pop("shpp", UNSET)

        shpp_nic = d.pop("shppNic", UNSET)

        spbp = d.pop("spbp", UNSET)

        spbp_nic = d.pop("spbpNic", UNSET)

        eligible_for_employment_allowance = d.pop(
            "eligibleForEmploymentAllowance", UNSET
        )

        employment_allowance_claim = d.pop("employmentAllowanceClaim", UNSET)

        employment_allowance_claim_auto = d.pop("employmentAllowanceClaimAuto", UNSET)

        liable_for_apprenticeship_levy = d.pop("liableForApprenticeshipLevy", UNSET)

        apprenticeship_levy = d.pop("apprenticeshipLevy", UNSET)

        apprenticeship_levy_auto = d.pop("apprenticeshipLevyAuto", UNSET)

        liability_arising_in_period = d.pop("liabilityArisingInPeriod", UNSET)

        due_in_previous_periods = d.pop("dueInPreviousPeriods", UNSET)

        paid_in_previous_periods = d.pop("paidInPreviousPeriods", UNSET)

        employment_allowance_claim_in_previous_periods = d.pop(
            "employmentAllowanceClaimInPreviousPeriods", UNSET
        )

        received_from_hmrc_to_refund_tax = d.pop("receivedFromHMRCToRefundTax", UNSET)

        received_from_hmrc_to_pay_statutory_pay = d.pop(
            "receivedFromHMRCToPayStatutoryPay", UNSET
        )

        cis_deductions_suffered = d.pop("cisDeductionsSuffered", UNSET)

        adjustment = d.pop("adjustment", UNSET)

        net_liability_for_period = d.pop("netLiabilityForPeriod", UNSET)

        total_paid = d.pop("totalPaid", UNSET)

        payments = []
        _payments = d.pop("payments", UNSET)
        for payments_item_data in _payments or []:
            payments_item = HmrcPayment.from_dict(payments_item_data)

            payments.append(payments_item)

        fps_list = []
        _fps_list = d.pop("fpsList", UNSET)
        for fps_list_item_data in _fps_list or []:
            fps_list_item = Item.from_dict(fps_list_item_data)

            fps_list.append(fps_list_item)

        id = d.pop("id", UNSET)

        hmrc_liability = cls(
            title=title,
            tax_year=tax_year,
            period_ending=period_ending,
            period_complete=period_complete,
            recoverable_amounts_eps_created=recoverable_amounts_eps_created,
            apprenticeship_levy_eps_created=apprenticeship_levy_eps_created,
            pay_runs=pay_runs,
            tax=tax,
            cis_deductions=cis_deductions,
            postgrad_loan_deductions=postgrad_loan_deductions,
            student_loan_deductions=student_loan_deductions,
            employee_nic=employee_nic,
            employer_nic=employer_nic,
            real_time_class_1a_nic=real_time_class_1a_nic,
            smp=smp,
            smp_nic=smp_nic,
            spp=spp,
            spp_nic=spp_nic,
            sap=sap,
            sap_nic=sap_nic,
            shpp=shpp,
            shpp_nic=shpp_nic,
            spbp=spbp,
            spbp_nic=spbp_nic,
            eligible_for_employment_allowance=eligible_for_employment_allowance,
            employment_allowance_claim=employment_allowance_claim,
            employment_allowance_claim_auto=employment_allowance_claim_auto,
            liable_for_apprenticeship_levy=liable_for_apprenticeship_levy,
            apprenticeship_levy=apprenticeship_levy,
            apprenticeship_levy_auto=apprenticeship_levy_auto,
            liability_arising_in_period=liability_arising_in_period,
            due_in_previous_periods=due_in_previous_periods,
            paid_in_previous_periods=paid_in_previous_periods,
            employment_allowance_claim_in_previous_periods=employment_allowance_claim_in_previous_periods,
            received_from_hmrc_to_refund_tax=received_from_hmrc_to_refund_tax,
            received_from_hmrc_to_pay_statutory_pay=received_from_hmrc_to_pay_statutory_pay,
            cis_deductions_suffered=cis_deductions_suffered,
            adjustment=adjustment,
            net_liability_for_period=net_liability_for_period,
            total_paid=total_paid,
            payments=payments,
            fps_list=fps_list,
            id=id,
        )

        return hmrc_liability
