from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.fps_benefit import FpsBenefit
from ..models.fps_employee_flexible_drawdown import FpsEmployeeFlexibleDrawdown
from ..models.fps_employee_tax_code import FpsEmployeeTaxCode
from ..models.fps_employee_trivial_commutation_payment import (
    FpsEmployeeTrivialCommutationPayment,
)
from ..models.student_loan_recovered import StudentLoanRecovered
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeePayment")


@attr.s(auto_attribs=True)
class FpsEmployeePayment:
    """
    Attributes:
        bacs_hash_code (Union[Unset, None, str]):
        pay_freq (Union[Unset, None, str]):
        pmt_date (Union[Unset, None, str]):
        late_reason (Union[Unset, None, str]):
        week_no (Union[Unset, None, str]):
        month_no (Union[Unset, None, str]):
        periods_covered (Union[Unset, int]):
        aggregated_earnings (Union[Unset, None, str]):
        pmt_after_leaving (Union[Unset, None, str]):
        hours_worked (Union[Unset, None, str]):
        tax_code (Union[Unset, FpsEmployeeTaxCode]):
        taxable_pay (Union[Unset, None, str]):
        non_tax_or_nic_pmt (Union[Unset, None, str]):
        dedns_from_net_pay (Union[Unset, None, str]):
        pay_after_stat_dedns (Union[Unset, None, str]):
        benefits_taxed_via_payroll (Union[Unset, None, str]):
        class_1ani_cs_ytd (Union[Unset, None, str]):
        benefits (Union[Unset, FpsBenefit]):
        empee_pen_contribns_paid (Union[Unset, None, str]):
        items_subject_to_class_1nic (Union[Unset, None, str]):
        empee_pen_contribns_not_paid (Union[Unset, None, str]):
        student_loan_recovered (Union[Unset, StudentLoanRecovered]):
        postgrad_loan_recovered (Union[Unset, None, str]):
        tax_deducted_or_refunded (Union[Unset, None, str]):
        on_strike (Union[Unset, None, str]):
        unpaid_absence (Union[Unset, None, str]):
        smpytd (Union[Unset, None, str]):
        sppytd (Union[Unset, None, str]):
        sapytd (Union[Unset, None, str]):
        sh_ppytd (Union[Unset, None, str]):
        spbpytd (Union[Unset, None, str]):
        trivial_commutation_payment (Union[Unset, None, List[FpsEmployeeTrivialCommutationPayment]]):
        flexible_drawdown (Union[Unset, FpsEmployeeFlexibleDrawdown]):
    """

    bacs_hash_code: Union[Unset, None, str] = UNSET
    pay_freq: Union[Unset, None, str] = UNSET
    pmt_date: Union[Unset, None, str] = UNSET
    late_reason: Union[Unset, None, str] = UNSET
    week_no: Union[Unset, None, str] = UNSET
    month_no: Union[Unset, None, str] = UNSET
    periods_covered: Union[Unset, int] = UNSET
    aggregated_earnings: Union[Unset, None, str] = UNSET
    pmt_after_leaving: Union[Unset, None, str] = UNSET
    hours_worked: Union[Unset, None, str] = UNSET
    tax_code: Union[Unset, FpsEmployeeTaxCode] = UNSET
    taxable_pay: Union[Unset, None, str] = UNSET
    non_tax_or_nic_pmt: Union[Unset, None, str] = UNSET
    dedns_from_net_pay: Union[Unset, None, str] = UNSET
    pay_after_stat_dedns: Union[Unset, None, str] = UNSET
    benefits_taxed_via_payroll: Union[Unset, None, str] = UNSET
    class_1ani_cs_ytd: Union[Unset, None, str] = UNSET
    benefits: Union[Unset, FpsBenefit] = UNSET
    empee_pen_contribns_paid: Union[Unset, None, str] = UNSET
    items_subject_to_class_1nic: Union[Unset, None, str] = UNSET
    empee_pen_contribns_not_paid: Union[Unset, None, str] = UNSET
    student_loan_recovered: Union[Unset, StudentLoanRecovered] = UNSET
    postgrad_loan_recovered: Union[Unset, None, str] = UNSET
    tax_deducted_or_refunded: Union[Unset, None, str] = UNSET
    on_strike: Union[Unset, None, str] = UNSET
    unpaid_absence: Union[Unset, None, str] = UNSET
    smpytd: Union[Unset, None, str] = UNSET
    sppytd: Union[Unset, None, str] = UNSET
    sapytd: Union[Unset, None, str] = UNSET
    sh_ppytd: Union[Unset, None, str] = UNSET
    spbpytd: Union[Unset, None, str] = UNSET
    trivial_commutation_payment: Union[
        Unset, None, List[FpsEmployeeTrivialCommutationPayment]
    ] = UNSET
    flexible_drawdown: Union[Unset, FpsEmployeeFlexibleDrawdown] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bacs_hash_code = self.bacs_hash_code
        pay_freq = self.pay_freq
        pmt_date = self.pmt_date
        late_reason = self.late_reason
        week_no = self.week_no
        month_no = self.month_no
        periods_covered = self.periods_covered
        aggregated_earnings = self.aggregated_earnings
        pmt_after_leaving = self.pmt_after_leaving
        hours_worked = self.hours_worked
        tax_code: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tax_code, Unset):
            tax_code = self.tax_code.to_dict()

        taxable_pay = self.taxable_pay
        non_tax_or_nic_pmt = self.non_tax_or_nic_pmt
        dedns_from_net_pay = self.dedns_from_net_pay
        pay_after_stat_dedns = self.pay_after_stat_dedns
        benefits_taxed_via_payroll = self.benefits_taxed_via_payroll
        class_1ani_cs_ytd = self.class_1ani_cs_ytd
        benefits: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.benefits, Unset):
            benefits = self.benefits.to_dict()

        empee_pen_contribns_paid = self.empee_pen_contribns_paid
        items_subject_to_class_1nic = self.items_subject_to_class_1nic
        empee_pen_contribns_not_paid = self.empee_pen_contribns_not_paid
        student_loan_recovered: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.student_loan_recovered, Unset):
            student_loan_recovered = self.student_loan_recovered.to_dict()

        postgrad_loan_recovered = self.postgrad_loan_recovered
        tax_deducted_or_refunded = self.tax_deducted_or_refunded
        on_strike = self.on_strike
        unpaid_absence = self.unpaid_absence
        smpytd = self.smpytd
        sppytd = self.sppytd
        sapytd = self.sapytd
        sh_ppytd = self.sh_ppytd
        spbpytd = self.spbpytd
        trivial_commutation_payment: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trivial_commutation_payment, Unset):
            if self.trivial_commutation_payment is None:
                trivial_commutation_payment = None
            else:
                trivial_commutation_payment = []
                for (
                    trivial_commutation_payment_item_data
                ) in self.trivial_commutation_payment:
                    trivial_commutation_payment_item = (
                        trivial_commutation_payment_item_data.to_dict()
                    )

                    trivial_commutation_payment.append(trivial_commutation_payment_item)

        flexible_drawdown: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flexible_drawdown, Unset):
            flexible_drawdown = self.flexible_drawdown.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bacs_hash_code is not UNSET:
            field_dict["bacsHashCode"] = bacs_hash_code
        if pay_freq is not UNSET:
            field_dict["payFreq"] = pay_freq
        if pmt_date is not UNSET:
            field_dict["pmtDate"] = pmt_date
        if late_reason is not UNSET:
            field_dict["lateReason"] = late_reason
        if week_no is not UNSET:
            field_dict["weekNo"] = week_no
        if month_no is not UNSET:
            field_dict["monthNo"] = month_no
        if periods_covered is not UNSET:
            field_dict["periodsCovered"] = periods_covered
        if aggregated_earnings is not UNSET:
            field_dict["aggregatedEarnings"] = aggregated_earnings
        if pmt_after_leaving is not UNSET:
            field_dict["pmtAfterLeaving"] = pmt_after_leaving
        if hours_worked is not UNSET:
            field_dict["hoursWorked"] = hours_worked
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code
        if taxable_pay is not UNSET:
            field_dict["taxablePay"] = taxable_pay
        if non_tax_or_nic_pmt is not UNSET:
            field_dict["nonTaxOrNICPmt"] = non_tax_or_nic_pmt
        if dedns_from_net_pay is not UNSET:
            field_dict["dednsFromNetPay"] = dedns_from_net_pay
        if pay_after_stat_dedns is not UNSET:
            field_dict["payAfterStatDedns"] = pay_after_stat_dedns
        if benefits_taxed_via_payroll is not UNSET:
            field_dict["benefitsTaxedViaPayroll"] = benefits_taxed_via_payroll
        if class_1ani_cs_ytd is not UNSET:
            field_dict["class1ANICsYTD"] = class_1ani_cs_ytd
        if benefits is not UNSET:
            field_dict["benefits"] = benefits
        if empee_pen_contribns_paid is not UNSET:
            field_dict["empeePenContribnsPaid"] = empee_pen_contribns_paid
        if items_subject_to_class_1nic is not UNSET:
            field_dict["itemsSubjectToClass1NIC"] = items_subject_to_class_1nic
        if empee_pen_contribns_not_paid is not UNSET:
            field_dict["empeePenContribnsNotPaid"] = empee_pen_contribns_not_paid
        if student_loan_recovered is not UNSET:
            field_dict["studentLoanRecovered"] = student_loan_recovered
        if postgrad_loan_recovered is not UNSET:
            field_dict["postgradLoanRecovered"] = postgrad_loan_recovered
        if tax_deducted_or_refunded is not UNSET:
            field_dict["taxDeductedOrRefunded"] = tax_deducted_or_refunded
        if on_strike is not UNSET:
            field_dict["onStrike"] = on_strike
        if unpaid_absence is not UNSET:
            field_dict["unpaidAbsence"] = unpaid_absence
        if smpytd is not UNSET:
            field_dict["smpytd"] = smpytd
        if sppytd is not UNSET:
            field_dict["sppytd"] = sppytd
        if sapytd is not UNSET:
            field_dict["sapytd"] = sapytd
        if sh_ppytd is not UNSET:
            field_dict["shPPYTD"] = sh_ppytd
        if spbpytd is not UNSET:
            field_dict["spbpytd"] = spbpytd
        if trivial_commutation_payment is not UNSET:
            field_dict["trivialCommutationPayment"] = trivial_commutation_payment
        if flexible_drawdown is not UNSET:
            field_dict["flexibleDrawdown"] = flexible_drawdown

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bacs_hash_code = d.pop("bacsHashCode", UNSET)

        pay_freq = d.pop("payFreq", UNSET)

        pmt_date = d.pop("pmtDate", UNSET)

        late_reason = d.pop("lateReason", UNSET)

        week_no = d.pop("weekNo", UNSET)

        month_no = d.pop("monthNo", UNSET)

        periods_covered = d.pop("periodsCovered", UNSET)

        aggregated_earnings = d.pop("aggregatedEarnings", UNSET)

        pmt_after_leaving = d.pop("pmtAfterLeaving", UNSET)

        hours_worked = d.pop("hoursWorked", UNSET)

        _tax_code = d.pop("taxCode", UNSET)
        tax_code: Union[Unset, FpsEmployeeTaxCode]
        if isinstance(_tax_code, Unset):
            tax_code = UNSET
        else:
            tax_code = FpsEmployeeTaxCode.from_dict(_tax_code)

        taxable_pay = d.pop("taxablePay", UNSET)

        non_tax_or_nic_pmt = d.pop("nonTaxOrNICPmt", UNSET)

        dedns_from_net_pay = d.pop("dednsFromNetPay", UNSET)

        pay_after_stat_dedns = d.pop("payAfterStatDedns", UNSET)

        benefits_taxed_via_payroll = d.pop("benefitsTaxedViaPayroll", UNSET)

        class_1ani_cs_ytd = d.pop("class1ANICsYTD", UNSET)

        _benefits = d.pop("benefits", UNSET)
        benefits: Union[Unset, FpsBenefit]
        if isinstance(_benefits, Unset):
            benefits = UNSET
        else:
            benefits = FpsBenefit.from_dict(_benefits)

        empee_pen_contribns_paid = d.pop("empeePenContribnsPaid", UNSET)

        items_subject_to_class_1nic = d.pop("itemsSubjectToClass1NIC", UNSET)

        empee_pen_contribns_not_paid = d.pop("empeePenContribnsNotPaid", UNSET)

        _student_loan_recovered = d.pop("studentLoanRecovered", UNSET)
        student_loan_recovered: Union[Unset, StudentLoanRecovered]
        if isinstance(_student_loan_recovered, Unset):
            student_loan_recovered = UNSET
        else:
            student_loan_recovered = StudentLoanRecovered.from_dict(
                _student_loan_recovered
            )

        postgrad_loan_recovered = d.pop("postgradLoanRecovered", UNSET)

        tax_deducted_or_refunded = d.pop("taxDeductedOrRefunded", UNSET)

        on_strike = d.pop("onStrike", UNSET)

        unpaid_absence = d.pop("unpaidAbsence", UNSET)

        smpytd = d.pop("smpytd", UNSET)

        sppytd = d.pop("sppytd", UNSET)

        sapytd = d.pop("sapytd", UNSET)

        sh_ppytd = d.pop("shPPYTD", UNSET)

        spbpytd = d.pop("spbpytd", UNSET)

        trivial_commutation_payment = []
        _trivial_commutation_payment = d.pop("trivialCommutationPayment", UNSET)
        for trivial_commutation_payment_item_data in _trivial_commutation_payment or []:
            trivial_commutation_payment_item = (
                FpsEmployeeTrivialCommutationPayment.from_dict(
                    trivial_commutation_payment_item_data
                )
            )

            trivial_commutation_payment.append(trivial_commutation_payment_item)

        _flexible_drawdown = d.pop("flexibleDrawdown", UNSET)
        flexible_drawdown: Union[Unset, FpsEmployeeFlexibleDrawdown]
        if isinstance(_flexible_drawdown, Unset):
            flexible_drawdown = UNSET
        else:
            flexible_drawdown = FpsEmployeeFlexibleDrawdown.from_dict(
                _flexible_drawdown
            )

        fps_employee_payment = cls(
            bacs_hash_code=bacs_hash_code,
            pay_freq=pay_freq,
            pmt_date=pmt_date,
            late_reason=late_reason,
            week_no=week_no,
            month_no=month_no,
            periods_covered=periods_covered,
            aggregated_earnings=aggregated_earnings,
            pmt_after_leaving=pmt_after_leaving,
            hours_worked=hours_worked,
            tax_code=tax_code,
            taxable_pay=taxable_pay,
            non_tax_or_nic_pmt=non_tax_or_nic_pmt,
            dedns_from_net_pay=dedns_from_net_pay,
            pay_after_stat_dedns=pay_after_stat_dedns,
            benefits_taxed_via_payroll=benefits_taxed_via_payroll,
            class_1ani_cs_ytd=class_1ani_cs_ytd,
            benefits=benefits,
            empee_pen_contribns_paid=empee_pen_contribns_paid,
            items_subject_to_class_1nic=items_subject_to_class_1nic,
            empee_pen_contribns_not_paid=empee_pen_contribns_not_paid,
            student_loan_recovered=student_loan_recovered,
            postgrad_loan_recovered=postgrad_loan_recovered,
            tax_deducted_or_refunded=tax_deducted_or_refunded,
            on_strike=on_strike,
            unpaid_absence=unpaid_absence,
            smpytd=smpytd,
            sppytd=sppytd,
            sapytd=sapytd,
            sh_ppytd=sh_ppytd,
            spbpytd=spbpytd,
            trivial_commutation_payment=trivial_commutation_payment,
            flexible_drawdown=flexible_drawdown,
        )

        return fps_employee_payment
