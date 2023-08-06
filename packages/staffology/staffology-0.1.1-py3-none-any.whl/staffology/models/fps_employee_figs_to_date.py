from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeFigsToDate")


@attr.s(auto_attribs=True)
class FpsEmployeeFigsToDate:
    """
    Attributes:
        taxable_pay (Union[Unset, None, str]):
        total_tax (Union[Unset, None, str]):
        student_loans_td (Union[Unset, None, str]):
        postgrad_loans_td (Union[Unset, None, str]):
        benefits_taxed_via_payroll_ytd (Union[Unset, None, str]):
        empee_pen_contribns_paid_ytd (Union[Unset, None, str]):
        empee_pen_contribns_not_paid_ytd (Union[Unset, None, str]):
        smpytd (Union[Unset, None, str]):
        sppytd (Union[Unset, None, str]):
        sapytd (Union[Unset, None, str]):
        shppytd (Union[Unset, None, str]):
        spbpytd (Union[Unset, None, str]):
        sspytd (Union[Unset, None, str]):
        gross (Union[Unset, None, str]):
        net_pay (Union[Unset, None, str]):
        additions (Union[Unset, None, str]):
        deductions (Union[Unset, None, str]):
        take_home_pay (Union[Unset, None, str]):
        adjustments (Union[Unset, None, str]):
        maps_miles (Union[Unset, None, str]):
        pensionable_earnings (Union[Unset, None, str]):
        pensionable_pay (Union[Unset, None, str]):
        employer_pension_contribution (Union[Unset, None, str]):
        employee_pension_contribution (Union[Unset, None, str]):
        employee_pension_contribution_avc (Union[Unset, None, str]):
        payment_after_leaving (Union[Unset, None, str]):
        tax_on_payment_after_leaving (Union[Unset, None, str]):
        taxable_pay_previous_employment (Union[Unset, None, str]):
        total_tax_previous_employment (Union[Unset, None, str]):
    """

    taxable_pay: Union[Unset, None, str] = UNSET
    total_tax: Union[Unset, None, str] = UNSET
    student_loans_td: Union[Unset, None, str] = UNSET
    postgrad_loans_td: Union[Unset, None, str] = UNSET
    benefits_taxed_via_payroll_ytd: Union[Unset, None, str] = UNSET
    empee_pen_contribns_paid_ytd: Union[Unset, None, str] = UNSET
    empee_pen_contribns_not_paid_ytd: Union[Unset, None, str] = UNSET
    smpytd: Union[Unset, None, str] = UNSET
    sppytd: Union[Unset, None, str] = UNSET
    sapytd: Union[Unset, None, str] = UNSET
    shppytd: Union[Unset, None, str] = UNSET
    spbpytd: Union[Unset, None, str] = UNSET
    sspytd: Union[Unset, None, str] = UNSET
    gross: Union[Unset, None, str] = UNSET
    net_pay: Union[Unset, None, str] = UNSET
    additions: Union[Unset, None, str] = UNSET
    deductions: Union[Unset, None, str] = UNSET
    take_home_pay: Union[Unset, None, str] = UNSET
    adjustments: Union[Unset, None, str] = UNSET
    maps_miles: Union[Unset, None, str] = UNSET
    pensionable_earnings: Union[Unset, None, str] = UNSET
    pensionable_pay: Union[Unset, None, str] = UNSET
    employer_pension_contribution: Union[Unset, None, str] = UNSET
    employee_pension_contribution: Union[Unset, None, str] = UNSET
    employee_pension_contribution_avc: Union[Unset, None, str] = UNSET
    payment_after_leaving: Union[Unset, None, str] = UNSET
    tax_on_payment_after_leaving: Union[Unset, None, str] = UNSET
    taxable_pay_previous_employment: Union[Unset, None, str] = UNSET
    total_tax_previous_employment: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        taxable_pay = self.taxable_pay
        total_tax = self.total_tax
        student_loans_td = self.student_loans_td
        postgrad_loans_td = self.postgrad_loans_td
        benefits_taxed_via_payroll_ytd = self.benefits_taxed_via_payroll_ytd
        empee_pen_contribns_paid_ytd = self.empee_pen_contribns_paid_ytd
        empee_pen_contribns_not_paid_ytd = self.empee_pen_contribns_not_paid_ytd
        smpytd = self.smpytd
        sppytd = self.sppytd
        sapytd = self.sapytd
        shppytd = self.shppytd
        spbpytd = self.spbpytd
        sspytd = self.sspytd
        gross = self.gross
        net_pay = self.net_pay
        additions = self.additions
        deductions = self.deductions
        take_home_pay = self.take_home_pay
        adjustments = self.adjustments
        maps_miles = self.maps_miles
        pensionable_earnings = self.pensionable_earnings
        pensionable_pay = self.pensionable_pay
        employer_pension_contribution = self.employer_pension_contribution
        employee_pension_contribution = self.employee_pension_contribution
        employee_pension_contribution_avc = self.employee_pension_contribution_avc
        payment_after_leaving = self.payment_after_leaving
        tax_on_payment_after_leaving = self.tax_on_payment_after_leaving
        taxable_pay_previous_employment = self.taxable_pay_previous_employment
        total_tax_previous_employment = self.total_tax_previous_employment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if taxable_pay is not UNSET:
            field_dict["taxablePay"] = taxable_pay
        if total_tax is not UNSET:
            field_dict["totalTax"] = total_tax
        if student_loans_td is not UNSET:
            field_dict["studentLoansTD"] = student_loans_td
        if postgrad_loans_td is not UNSET:
            field_dict["postgradLoansTD"] = postgrad_loans_td
        if benefits_taxed_via_payroll_ytd is not UNSET:
            field_dict["benefitsTaxedViaPayrollYTD"] = benefits_taxed_via_payroll_ytd
        if empee_pen_contribns_paid_ytd is not UNSET:
            field_dict["empeePenContribnsPaidYTD"] = empee_pen_contribns_paid_ytd
        if empee_pen_contribns_not_paid_ytd is not UNSET:
            field_dict["empeePenContribnsNotPaidYTD"] = empee_pen_contribns_not_paid_ytd
        if smpytd is not UNSET:
            field_dict["smpytd"] = smpytd
        if sppytd is not UNSET:
            field_dict["sppytd"] = sppytd
        if sapytd is not UNSET:
            field_dict["sapytd"] = sapytd
        if shppytd is not UNSET:
            field_dict["shppytd"] = shppytd
        if spbpytd is not UNSET:
            field_dict["spbpytd"] = spbpytd
        if sspytd is not UNSET:
            field_dict["sspytd"] = sspytd
        if gross is not UNSET:
            field_dict["gross"] = gross
        if net_pay is not UNSET:
            field_dict["netPay"] = net_pay
        if additions is not UNSET:
            field_dict["additions"] = additions
        if deductions is not UNSET:
            field_dict["deductions"] = deductions
        if take_home_pay is not UNSET:
            field_dict["takeHomePay"] = take_home_pay
        if adjustments is not UNSET:
            field_dict["adjustments"] = adjustments
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if pensionable_earnings is not UNSET:
            field_dict["pensionableEarnings"] = pensionable_earnings
        if pensionable_pay is not UNSET:
            field_dict["pensionablePay"] = pensionable_pay
        if employer_pension_contribution is not UNSET:
            field_dict["employerPensionContribution"] = employer_pension_contribution
        if employee_pension_contribution is not UNSET:
            field_dict["employeePensionContribution"] = employee_pension_contribution
        if employee_pension_contribution_avc is not UNSET:
            field_dict[
                "employeePensionContributionAvc"
            ] = employee_pension_contribution_avc
        if payment_after_leaving is not UNSET:
            field_dict["paymentAfterLeaving"] = payment_after_leaving
        if tax_on_payment_after_leaving is not UNSET:
            field_dict["taxOnPaymentAfterLeaving"] = tax_on_payment_after_leaving
        if taxable_pay_previous_employment is not UNSET:
            field_dict["taxablePayPreviousEmployment"] = taxable_pay_previous_employment
        if total_tax_previous_employment is not UNSET:
            field_dict["totalTaxPreviousEmployment"] = total_tax_previous_employment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        taxable_pay = d.pop("taxablePay", UNSET)

        total_tax = d.pop("totalTax", UNSET)

        student_loans_td = d.pop("studentLoansTD", UNSET)

        postgrad_loans_td = d.pop("postgradLoansTD", UNSET)

        benefits_taxed_via_payroll_ytd = d.pop("benefitsTaxedViaPayrollYTD", UNSET)

        empee_pen_contribns_paid_ytd = d.pop("empeePenContribnsPaidYTD", UNSET)

        empee_pen_contribns_not_paid_ytd = d.pop("empeePenContribnsNotPaidYTD", UNSET)

        smpytd = d.pop("smpytd", UNSET)

        sppytd = d.pop("sppytd", UNSET)

        sapytd = d.pop("sapytd", UNSET)

        shppytd = d.pop("shppytd", UNSET)

        spbpytd = d.pop("spbpytd", UNSET)

        sspytd = d.pop("sspytd", UNSET)

        gross = d.pop("gross", UNSET)

        net_pay = d.pop("netPay", UNSET)

        additions = d.pop("additions", UNSET)

        deductions = d.pop("deductions", UNSET)

        take_home_pay = d.pop("takeHomePay", UNSET)

        adjustments = d.pop("adjustments", UNSET)

        maps_miles = d.pop("mapsMiles", UNSET)

        pensionable_earnings = d.pop("pensionableEarnings", UNSET)

        pensionable_pay = d.pop("pensionablePay", UNSET)

        employer_pension_contribution = d.pop("employerPensionContribution", UNSET)

        employee_pension_contribution = d.pop("employeePensionContribution", UNSET)

        employee_pension_contribution_avc = d.pop(
            "employeePensionContributionAvc", UNSET
        )

        payment_after_leaving = d.pop("paymentAfterLeaving", UNSET)

        tax_on_payment_after_leaving = d.pop("taxOnPaymentAfterLeaving", UNSET)

        taxable_pay_previous_employment = d.pop("taxablePayPreviousEmployment", UNSET)

        total_tax_previous_employment = d.pop("totalTaxPreviousEmployment", UNSET)

        fps_employee_figs_to_date = cls(
            taxable_pay=taxable_pay,
            total_tax=total_tax,
            student_loans_td=student_loans_td,
            postgrad_loans_td=postgrad_loans_td,
            benefits_taxed_via_payroll_ytd=benefits_taxed_via_payroll_ytd,
            empee_pen_contribns_paid_ytd=empee_pen_contribns_paid_ytd,
            empee_pen_contribns_not_paid_ytd=empee_pen_contribns_not_paid_ytd,
            smpytd=smpytd,
            sppytd=sppytd,
            sapytd=sapytd,
            shppytd=shppytd,
            spbpytd=spbpytd,
            sspytd=sspytd,
            gross=gross,
            net_pay=net_pay,
            additions=additions,
            deductions=deductions,
            take_home_pay=take_home_pay,
            adjustments=adjustments,
            maps_miles=maps_miles,
            pensionable_earnings=pensionable_earnings,
            pensionable_pay=pensionable_pay,
            employer_pension_contribution=employer_pension_contribution,
            employee_pension_contribution=employee_pension_contribution,
            employee_pension_contribution_avc=employee_pension_contribution_avc,
            payment_after_leaving=payment_after_leaving,
            tax_on_payment_after_leaving=tax_on_payment_after_leaving,
            taxable_pay_previous_employment=taxable_pay_previous_employment,
            total_tax_previous_employment=total_tax_previous_employment,
        )

        return fps_employee_figs_to_date
