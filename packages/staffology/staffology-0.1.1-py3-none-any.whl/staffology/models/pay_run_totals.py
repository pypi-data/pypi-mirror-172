from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_run_cost_summary import PayRunCostSummary
from ..models.recoverable_amounts import RecoverableAmounts
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunTotals")


@attr.s(auto_attribs=True)
class PayRunTotals:
    """Used to represent totals for a PayRun or PayRunEntry.
    If a value is 0 then it will not be shown in the JSON.

        Attributes:
            basic_pay (Union[Unset, float]): [readonly] The amount to be paid to this Employee as a result of the PayOptions
                that have been set
            gross (Union[Unset, float]): [readonly] Gross pay
            gross_for_ni (Union[Unset, float]): [readonly] The amount of the Gross that is subject to NI
            gross_not_subject_to_employers_ni (Union[Unset, float]): [readonly] The amount of the Gross that is not subject
                to Employers NI.
                This is the same as GrossForNI where the employees NI Table has an Er contribution
            gross_for_tax (Union[Unset, float]): [readonly] The amount of the Gross that is subject to PAYE
            employer_ni (Union[Unset, float]): [readonly]
            employee_ni (Union[Unset, float]): [readonly]
            employer_ni_off_payroll (Union[Unset, float]): [readonly] The amount included in EmployerNi that is in relation
                to Off-Payroll Workers
            real_time_class_1a_ni (Union[Unset, float]): [readonly]
            tax (Union[Unset, float]): [readonly]
            net_pay (Union[Unset, float]): [readonly] The Net Pay for this Employee
            adjustments (Union[Unset, float]): [readonly] The value of adjustments made to the Net Pay (Non taxable/NIable
                additions/deductions)
            additions (Union[Unset, float]): The value of all additions.  This minus Deductions should equal TakeHomePay
            deductions (Union[Unset, float]): The value of all deductions.  Additions minus This value should equal
                TakeHomePay
            take_home_pay (Union[Unset, float]): [readonly] The amount this Employee takes home
            non_tax_or_nic_pmt (Union[Unset, float]): [readonly] The value of any payments being made to this Employee that
                aren't being subjected to PAYE or NI
            items_subject_to_class_1nic (Union[Unset, float]): [readonly] Items subject to Class 1 NIC but not taxed under
                PAYE regulations excluding pension contributions
            dedns_from_net_pay (Union[Unset, float]): [readonly] The value of any deductions being made to the Net Pay for
                this Employee
            tcp_tcls (Union[Unset, float]): [readonly] Value of payments marked as Trivial Commutation Payment (A - TCLS)
            tcp_pp (Union[Unset, float]): [readonly] Value of payments marked as Trivial Commutation Payment (B - Personal
                Pension)
            tcp_op (Union[Unset, float]): [readonly] Value of payments marked as Trivial Commutation Payment (C -
                Occupational Pension)
            flexi_dd_death (Union[Unset, float]): [readonly] Value of payments marked as flexibly accessing death benefit
                (taxable)
            flexi_dd_death_non_tax (Union[Unset, float]): [readonly] Value of payments marked as flexibly accessing death
                benefit (non taxable)
            flexi_dd_pension (Union[Unset, float]): [readonly] Value of payments marked as flexibly accessing pension
                (taxable)
            flexi_dd_pension_non_tax (Union[Unset, float]): [readonly] Value of payments marked as flexibly accessing
                pension (non taxable)
            smp (Union[Unset, float]): [readonly] Statutory Maternity Pay
            spp (Union[Unset, float]): [readonly] Statutory Paternity Pay
            sap (Union[Unset, float]): [readonly] Statutory Adoption Pay
            shpp (Union[Unset, float]): [readonly] Statutory Shared Parental Pay
            spbp (Union[Unset, float]): [readonly] Statutory Parental Bereavement Pay
            ssp (Union[Unset, float]): [readonly] Statutory Sick  Pay
            student_loan_recovered (Union[Unset, float]): [readonly]
            postgrad_loan_recovered (Union[Unset, float]): [readonly]
            pensionable_earnings (Union[Unset, float]): [readonly] The amount of the Gross that is subject to Pension
                Deductions.
                If the Pension Scheme uses Qualifying Earnings (upper and lower limits) then this value is before those are
                applied
            pensionable_pay (Union[Unset, float]): [readonly] The amount of the Gross that pension calculations are based on
                after taking into account Upper and Lower Limits for the WorkerGroup.
            non_tierable_pay (Union[Unset, float]): [readonly] The value of any pay that shouldn't count towards determining
                a pension tier.
            employee_pension_contribution (Union[Unset, float]): [readonly] The value of the Pension Contribution being made
                by this Employee, excluding any Additional Voluntary Contributions
            employee_pension_contribution_avc (Union[Unset, float]): [readonly] The value of the Pension Contribution being
                made by this Employee as an Additional Voluntary Contribution
            employer_pension_contribution (Union[Unset, float]): [readonly] The value of the Pension Contribution being made
                by the Employer for this Employee
            empee_pen_contribns_not_paid (Union[Unset, float]): [readonly] Value of employee pension contributions that are
                not paid under 'net pay arrangements', including any AVC
            empee_pen_contribns_paid (Union[Unset, float]): [readonly] Value of employee pension contributions paid under
                'net pay arrangements', including any AVC
            attachment_order_deductions (Union[Unset, float]): [readonly] Value of deductions made due to AttachmentOrders
            cis_deduction (Union[Unset, float]): [readonly] Value of any CIS Deduction made
            cis_vat (Union[Unset, float]): [readonly] Value of any VAT paid to CIS Subcontractor
            cis_umbrella_fee (Union[Unset, float]): [readonly] Value of any pre-tax fee charged to the CIS Subcontractor for
                processing the payment
            cis_umbrella_fee_post_tax (Union[Unset, float]): [readonly] Value of any post-tax fee charged to the CIS
                Subcontractor for processing the payment
            pbik (Union[Unset, float]): [readonly] Value of any Payrolled Benefits In Kind
            maps_miles (Union[Unset, int]): [readonly] The number of miles paid for Mileage Allowance Payments
            umbrella_fee (Union[Unset, float]): [readonly] Value of any Umbrella fee charged for processing the payment
            app_levy_deduction (Union[Unset, float]): [readonly] Value of any Apprenticeship Levy fee deducted for
                processing the umbrella payment
            payment_after_leaving (Union[Unset, float]): [readonly] Payment After Leaving
            tax_on_payment_after_leaving (Union[Unset, float]): [readonly] Tax On Payment After Leaving
            nil_paid (Union[Unset, int]): [readonly] The number of employees with NilPaid on the PayRun
            leavers (Union[Unset, int]): [readonly] The number of Leavers on ths PayRun
            starters (Union[Unset, int]): [readonly] The number of Starters on this PayRun
            total_cost (Union[Unset, float]):
            recoverable_amounts (Union[Unset, RecoverableAmounts]):
            cost_summary (Union[Unset, PayRunCostSummary]): Represents the various components that make up the costs of a
                PayRun
    """

    basic_pay: Union[Unset, float] = UNSET
    gross: Union[Unset, float] = UNSET
    gross_for_ni: Union[Unset, float] = UNSET
    gross_not_subject_to_employers_ni: Union[Unset, float] = UNSET
    gross_for_tax: Union[Unset, float] = UNSET
    employer_ni: Union[Unset, float] = UNSET
    employee_ni: Union[Unset, float] = UNSET
    employer_ni_off_payroll: Union[Unset, float] = UNSET
    real_time_class_1a_ni: Union[Unset, float] = UNSET
    tax: Union[Unset, float] = UNSET
    net_pay: Union[Unset, float] = UNSET
    adjustments: Union[Unset, float] = UNSET
    additions: Union[Unset, float] = UNSET
    deductions: Union[Unset, float] = UNSET
    take_home_pay: Union[Unset, float] = UNSET
    non_tax_or_nic_pmt: Union[Unset, float] = UNSET
    items_subject_to_class_1nic: Union[Unset, float] = UNSET
    dedns_from_net_pay: Union[Unset, float] = UNSET
    tcp_tcls: Union[Unset, float] = UNSET
    tcp_pp: Union[Unset, float] = UNSET
    tcp_op: Union[Unset, float] = UNSET
    flexi_dd_death: Union[Unset, float] = UNSET
    flexi_dd_death_non_tax: Union[Unset, float] = UNSET
    flexi_dd_pension: Union[Unset, float] = UNSET
    flexi_dd_pension_non_tax: Union[Unset, float] = UNSET
    smp: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET
    ssp: Union[Unset, float] = UNSET
    student_loan_recovered: Union[Unset, float] = UNSET
    postgrad_loan_recovered: Union[Unset, float] = UNSET
    pensionable_earnings: Union[Unset, float] = UNSET
    pensionable_pay: Union[Unset, float] = UNSET
    non_tierable_pay: Union[Unset, float] = UNSET
    employee_pension_contribution: Union[Unset, float] = UNSET
    employee_pension_contribution_avc: Union[Unset, float] = UNSET
    employer_pension_contribution: Union[Unset, float] = UNSET
    empee_pen_contribns_not_paid: Union[Unset, float] = UNSET
    empee_pen_contribns_paid: Union[Unset, float] = UNSET
    attachment_order_deductions: Union[Unset, float] = UNSET
    cis_deduction: Union[Unset, float] = UNSET
    cis_vat: Union[Unset, float] = UNSET
    cis_umbrella_fee: Union[Unset, float] = UNSET
    cis_umbrella_fee_post_tax: Union[Unset, float] = UNSET
    pbik: Union[Unset, float] = UNSET
    maps_miles: Union[Unset, int] = UNSET
    umbrella_fee: Union[Unset, float] = UNSET
    app_levy_deduction: Union[Unset, float] = UNSET
    payment_after_leaving: Union[Unset, float] = UNSET
    tax_on_payment_after_leaving: Union[Unset, float] = UNSET
    nil_paid: Union[Unset, int] = UNSET
    leavers: Union[Unset, int] = UNSET
    starters: Union[Unset, int] = UNSET
    total_cost: Union[Unset, float] = UNSET
    recoverable_amounts: Union[Unset, RecoverableAmounts] = UNSET
    cost_summary: Union[Unset, PayRunCostSummary] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        basic_pay = self.basic_pay
        gross = self.gross
        gross_for_ni = self.gross_for_ni
        gross_not_subject_to_employers_ni = self.gross_not_subject_to_employers_ni
        gross_for_tax = self.gross_for_tax
        employer_ni = self.employer_ni
        employee_ni = self.employee_ni
        employer_ni_off_payroll = self.employer_ni_off_payroll
        real_time_class_1a_ni = self.real_time_class_1a_ni
        tax = self.tax
        net_pay = self.net_pay
        adjustments = self.adjustments
        additions = self.additions
        deductions = self.deductions
        take_home_pay = self.take_home_pay
        non_tax_or_nic_pmt = self.non_tax_or_nic_pmt
        items_subject_to_class_1nic = self.items_subject_to_class_1nic
        dedns_from_net_pay = self.dedns_from_net_pay
        tcp_tcls = self.tcp_tcls
        tcp_pp = self.tcp_pp
        tcp_op = self.tcp_op
        flexi_dd_death = self.flexi_dd_death
        flexi_dd_death_non_tax = self.flexi_dd_death_non_tax
        flexi_dd_pension = self.flexi_dd_pension
        flexi_dd_pension_non_tax = self.flexi_dd_pension_non_tax
        smp = self.smp
        spp = self.spp
        sap = self.sap
        shpp = self.shpp
        spbp = self.spbp
        ssp = self.ssp
        student_loan_recovered = self.student_loan_recovered
        postgrad_loan_recovered = self.postgrad_loan_recovered
        pensionable_earnings = self.pensionable_earnings
        pensionable_pay = self.pensionable_pay
        non_tierable_pay = self.non_tierable_pay
        employee_pension_contribution = self.employee_pension_contribution
        employee_pension_contribution_avc = self.employee_pension_contribution_avc
        employer_pension_contribution = self.employer_pension_contribution
        empee_pen_contribns_not_paid = self.empee_pen_contribns_not_paid
        empee_pen_contribns_paid = self.empee_pen_contribns_paid
        attachment_order_deductions = self.attachment_order_deductions
        cis_deduction = self.cis_deduction
        cis_vat = self.cis_vat
        cis_umbrella_fee = self.cis_umbrella_fee
        cis_umbrella_fee_post_tax = self.cis_umbrella_fee_post_tax
        pbik = self.pbik
        maps_miles = self.maps_miles
        umbrella_fee = self.umbrella_fee
        app_levy_deduction = self.app_levy_deduction
        payment_after_leaving = self.payment_after_leaving
        tax_on_payment_after_leaving = self.tax_on_payment_after_leaving
        nil_paid = self.nil_paid
        leavers = self.leavers
        starters = self.starters
        total_cost = self.total_cost
        recoverable_amounts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recoverable_amounts, Unset):
            recoverable_amounts = self.recoverable_amounts.to_dict()

        cost_summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cost_summary, Unset):
            cost_summary = self.cost_summary.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if basic_pay is not UNSET:
            field_dict["basicPay"] = basic_pay
        if gross is not UNSET:
            field_dict["gross"] = gross
        if gross_for_ni is not UNSET:
            field_dict["grossForNi"] = gross_for_ni
        if gross_not_subject_to_employers_ni is not UNSET:
            field_dict[
                "grossNotSubjectToEmployersNi"
            ] = gross_not_subject_to_employers_ni
        if gross_for_tax is not UNSET:
            field_dict["grossForTax"] = gross_for_tax
        if employer_ni is not UNSET:
            field_dict["employerNi"] = employer_ni
        if employee_ni is not UNSET:
            field_dict["employeeNi"] = employee_ni
        if employer_ni_off_payroll is not UNSET:
            field_dict["employerNiOffPayroll"] = employer_ni_off_payroll
        if real_time_class_1a_ni is not UNSET:
            field_dict["realTimeClass1ANi"] = real_time_class_1a_ni
        if tax is not UNSET:
            field_dict["tax"] = tax
        if net_pay is not UNSET:
            field_dict["netPay"] = net_pay
        if adjustments is not UNSET:
            field_dict["adjustments"] = adjustments
        if additions is not UNSET:
            field_dict["additions"] = additions
        if deductions is not UNSET:
            field_dict["deductions"] = deductions
        if take_home_pay is not UNSET:
            field_dict["takeHomePay"] = take_home_pay
        if non_tax_or_nic_pmt is not UNSET:
            field_dict["nonTaxOrNICPmt"] = non_tax_or_nic_pmt
        if items_subject_to_class_1nic is not UNSET:
            field_dict["itemsSubjectToClass1NIC"] = items_subject_to_class_1nic
        if dedns_from_net_pay is not UNSET:
            field_dict["dednsFromNetPay"] = dedns_from_net_pay
        if tcp_tcls is not UNSET:
            field_dict["tcp_Tcls"] = tcp_tcls
        if tcp_pp is not UNSET:
            field_dict["tcp_Pp"] = tcp_pp
        if tcp_op is not UNSET:
            field_dict["tcp_Op"] = tcp_op
        if flexi_dd_death is not UNSET:
            field_dict["flexiDd_Death"] = flexi_dd_death
        if flexi_dd_death_non_tax is not UNSET:
            field_dict["flexiDd_Death_NonTax"] = flexi_dd_death_non_tax
        if flexi_dd_pension is not UNSET:
            field_dict["flexiDd_Pension"] = flexi_dd_pension
        if flexi_dd_pension_non_tax is not UNSET:
            field_dict["flexiDd_Pension_NonTax"] = flexi_dd_pension_non_tax
        if smp is not UNSET:
            field_dict["smp"] = smp
        if spp is not UNSET:
            field_dict["spp"] = spp
        if sap is not UNSET:
            field_dict["sap"] = sap
        if shpp is not UNSET:
            field_dict["shpp"] = shpp
        if spbp is not UNSET:
            field_dict["spbp"] = spbp
        if ssp is not UNSET:
            field_dict["ssp"] = ssp
        if student_loan_recovered is not UNSET:
            field_dict["studentLoanRecovered"] = student_loan_recovered
        if postgrad_loan_recovered is not UNSET:
            field_dict["postgradLoanRecovered"] = postgrad_loan_recovered
        if pensionable_earnings is not UNSET:
            field_dict["pensionableEarnings"] = pensionable_earnings
        if pensionable_pay is not UNSET:
            field_dict["pensionablePay"] = pensionable_pay
        if non_tierable_pay is not UNSET:
            field_dict["nonTierablePay"] = non_tierable_pay
        if employee_pension_contribution is not UNSET:
            field_dict["employeePensionContribution"] = employee_pension_contribution
        if employee_pension_contribution_avc is not UNSET:
            field_dict[
                "employeePensionContributionAvc"
            ] = employee_pension_contribution_avc
        if employer_pension_contribution is not UNSET:
            field_dict["employerPensionContribution"] = employer_pension_contribution
        if empee_pen_contribns_not_paid is not UNSET:
            field_dict["empeePenContribnsNotPaid"] = empee_pen_contribns_not_paid
        if empee_pen_contribns_paid is not UNSET:
            field_dict["empeePenContribnsPaid"] = empee_pen_contribns_paid
        if attachment_order_deductions is not UNSET:
            field_dict["attachmentOrderDeductions"] = attachment_order_deductions
        if cis_deduction is not UNSET:
            field_dict["cisDeduction"] = cis_deduction
        if cis_vat is not UNSET:
            field_dict["cisVat"] = cis_vat
        if cis_umbrella_fee is not UNSET:
            field_dict["cisUmbrellaFee"] = cis_umbrella_fee
        if cis_umbrella_fee_post_tax is not UNSET:
            field_dict["cisUmbrellaFeePostTax"] = cis_umbrella_fee_post_tax
        if pbik is not UNSET:
            field_dict["pbik"] = pbik
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if umbrella_fee is not UNSET:
            field_dict["umbrellaFee"] = umbrella_fee
        if app_levy_deduction is not UNSET:
            field_dict["appLevyDeduction"] = app_levy_deduction
        if payment_after_leaving is not UNSET:
            field_dict["paymentAfterLeaving"] = payment_after_leaving
        if tax_on_payment_after_leaving is not UNSET:
            field_dict["taxOnPaymentAfterLeaving"] = tax_on_payment_after_leaving
        if nil_paid is not UNSET:
            field_dict["nilPaid"] = nil_paid
        if leavers is not UNSET:
            field_dict["leavers"] = leavers
        if starters is not UNSET:
            field_dict["starters"] = starters
        if total_cost is not UNSET:
            field_dict["totalCost"] = total_cost
        if recoverable_amounts is not UNSET:
            field_dict["recoverableAmounts"] = recoverable_amounts
        if cost_summary is not UNSET:
            field_dict["costSummary"] = cost_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        basic_pay = d.pop("basicPay", UNSET)

        gross = d.pop("gross", UNSET)

        gross_for_ni = d.pop("grossForNi", UNSET)

        gross_not_subject_to_employers_ni = d.pop("grossNotSubjectToEmployersNi", UNSET)

        gross_for_tax = d.pop("grossForTax", UNSET)

        employer_ni = d.pop("employerNi", UNSET)

        employee_ni = d.pop("employeeNi", UNSET)

        employer_ni_off_payroll = d.pop("employerNiOffPayroll", UNSET)

        real_time_class_1a_ni = d.pop("realTimeClass1ANi", UNSET)

        tax = d.pop("tax", UNSET)

        net_pay = d.pop("netPay", UNSET)

        adjustments = d.pop("adjustments", UNSET)

        additions = d.pop("additions", UNSET)

        deductions = d.pop("deductions", UNSET)

        take_home_pay = d.pop("takeHomePay", UNSET)

        non_tax_or_nic_pmt = d.pop("nonTaxOrNICPmt", UNSET)

        items_subject_to_class_1nic = d.pop("itemsSubjectToClass1NIC", UNSET)

        dedns_from_net_pay = d.pop("dednsFromNetPay", UNSET)

        tcp_tcls = d.pop("tcp_Tcls", UNSET)

        tcp_pp = d.pop("tcp_Pp", UNSET)

        tcp_op = d.pop("tcp_Op", UNSET)

        flexi_dd_death = d.pop("flexiDd_Death", UNSET)

        flexi_dd_death_non_tax = d.pop("flexiDd_Death_NonTax", UNSET)

        flexi_dd_pension = d.pop("flexiDd_Pension", UNSET)

        flexi_dd_pension_non_tax = d.pop("flexiDd_Pension_NonTax", UNSET)

        smp = d.pop("smp", UNSET)

        spp = d.pop("spp", UNSET)

        sap = d.pop("sap", UNSET)

        shpp = d.pop("shpp", UNSET)

        spbp = d.pop("spbp", UNSET)

        ssp = d.pop("ssp", UNSET)

        student_loan_recovered = d.pop("studentLoanRecovered", UNSET)

        postgrad_loan_recovered = d.pop("postgradLoanRecovered", UNSET)

        pensionable_earnings = d.pop("pensionableEarnings", UNSET)

        pensionable_pay = d.pop("pensionablePay", UNSET)

        non_tierable_pay = d.pop("nonTierablePay", UNSET)

        employee_pension_contribution = d.pop("employeePensionContribution", UNSET)

        employee_pension_contribution_avc = d.pop(
            "employeePensionContributionAvc", UNSET
        )

        employer_pension_contribution = d.pop("employerPensionContribution", UNSET)

        empee_pen_contribns_not_paid = d.pop("empeePenContribnsNotPaid", UNSET)

        empee_pen_contribns_paid = d.pop("empeePenContribnsPaid", UNSET)

        attachment_order_deductions = d.pop("attachmentOrderDeductions", UNSET)

        cis_deduction = d.pop("cisDeduction", UNSET)

        cis_vat = d.pop("cisVat", UNSET)

        cis_umbrella_fee = d.pop("cisUmbrellaFee", UNSET)

        cis_umbrella_fee_post_tax = d.pop("cisUmbrellaFeePostTax", UNSET)

        pbik = d.pop("pbik", UNSET)

        maps_miles = d.pop("mapsMiles", UNSET)

        umbrella_fee = d.pop("umbrellaFee", UNSET)

        app_levy_deduction = d.pop("appLevyDeduction", UNSET)

        payment_after_leaving = d.pop("paymentAfterLeaving", UNSET)

        tax_on_payment_after_leaving = d.pop("taxOnPaymentAfterLeaving", UNSET)

        nil_paid = d.pop("nilPaid", UNSET)

        leavers = d.pop("leavers", UNSET)

        starters = d.pop("starters", UNSET)

        total_cost = d.pop("totalCost", UNSET)

        _recoverable_amounts = d.pop("recoverableAmounts", UNSET)
        recoverable_amounts: Union[Unset, RecoverableAmounts]
        if isinstance(_recoverable_amounts, Unset):
            recoverable_amounts = UNSET
        else:
            recoverable_amounts = RecoverableAmounts.from_dict(_recoverable_amounts)

        _cost_summary = d.pop("costSummary", UNSET)
        cost_summary: Union[Unset, PayRunCostSummary]
        if isinstance(_cost_summary, Unset):
            cost_summary = UNSET
        else:
            cost_summary = PayRunCostSummary.from_dict(_cost_summary)

        pay_run_totals = cls(
            basic_pay=basic_pay,
            gross=gross,
            gross_for_ni=gross_for_ni,
            gross_not_subject_to_employers_ni=gross_not_subject_to_employers_ni,
            gross_for_tax=gross_for_tax,
            employer_ni=employer_ni,
            employee_ni=employee_ni,
            employer_ni_off_payroll=employer_ni_off_payroll,
            real_time_class_1a_ni=real_time_class_1a_ni,
            tax=tax,
            net_pay=net_pay,
            adjustments=adjustments,
            additions=additions,
            deductions=deductions,
            take_home_pay=take_home_pay,
            non_tax_or_nic_pmt=non_tax_or_nic_pmt,
            items_subject_to_class_1nic=items_subject_to_class_1nic,
            dedns_from_net_pay=dedns_from_net_pay,
            tcp_tcls=tcp_tcls,
            tcp_pp=tcp_pp,
            tcp_op=tcp_op,
            flexi_dd_death=flexi_dd_death,
            flexi_dd_death_non_tax=flexi_dd_death_non_tax,
            flexi_dd_pension=flexi_dd_pension,
            flexi_dd_pension_non_tax=flexi_dd_pension_non_tax,
            smp=smp,
            spp=spp,
            sap=sap,
            shpp=shpp,
            spbp=spbp,
            ssp=ssp,
            student_loan_recovered=student_loan_recovered,
            postgrad_loan_recovered=postgrad_loan_recovered,
            pensionable_earnings=pensionable_earnings,
            pensionable_pay=pensionable_pay,
            non_tierable_pay=non_tierable_pay,
            employee_pension_contribution=employee_pension_contribution,
            employee_pension_contribution_avc=employee_pension_contribution_avc,
            employer_pension_contribution=employer_pension_contribution,
            empee_pen_contribns_not_paid=empee_pen_contribns_not_paid,
            empee_pen_contribns_paid=empee_pen_contribns_paid,
            attachment_order_deductions=attachment_order_deductions,
            cis_deduction=cis_deduction,
            cis_vat=cis_vat,
            cis_umbrella_fee=cis_umbrella_fee,
            cis_umbrella_fee_post_tax=cis_umbrella_fee_post_tax,
            pbik=pbik,
            maps_miles=maps_miles,
            umbrella_fee=umbrella_fee,
            app_levy_deduction=app_levy_deduction,
            payment_after_leaving=payment_after_leaving,
            tax_on_payment_after_leaving=tax_on_payment_after_leaving,
            nil_paid=nil_paid,
            leavers=leavers,
            starters=starters,
            total_cost=total_cost,
            recoverable_amounts=recoverable_amounts,
            cost_summary=cost_summary,
        )

        return pay_run_totals
