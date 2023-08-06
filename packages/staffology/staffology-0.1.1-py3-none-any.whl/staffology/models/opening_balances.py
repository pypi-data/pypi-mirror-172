from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..models.nic_summary import NicSummary
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="OpeningBalances")


@attr.s(auto_attribs=True)
class OpeningBalances:
    """
    Attributes:
        tax_year (Union[Unset, TaxYear]):
        not_new_starter (Union[Unset, bool]):
        previous_employer_gross (Union[Unset, float]):
        previous_employer_tax (Union[Unset, float]):
        current_employer_gross (Union[Unset, float]):
        current_employer_tax (Union[Unset, float]):
        current_employer_net (Union[Unset, float]):
        student_loan_deductions (Union[Unset, float]):
        postgrad_loan_deductions (Union[Unset, float]):
        empee_pen_contribns_paid (Union[Unset, float]):
        empee_pen_contribns_not_paid (Union[Unset, float]):
        smp (Union[Unset, float]):
        spp (Union[Unset, float]):
        sap (Union[Unset, float]):
        shpp (Union[Unset, float]):
        spbp (Union[Unset, float]):
        real_time_class_1a_ni (Union[Unset, float]):
        termination_payments (Union[Unset, float]):
        maps_miles (Union[Unset, int]):
        benefits_taxed_via_payroll (Union[Unset, float]):
        nic_summaries (Union[Unset, None, List[NicSummary]]):
        employee (Union[Unset, Item]):
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    not_new_starter: Union[Unset, bool] = UNSET
    previous_employer_gross: Union[Unset, float] = UNSET
    previous_employer_tax: Union[Unset, float] = UNSET
    current_employer_gross: Union[Unset, float] = UNSET
    current_employer_tax: Union[Unset, float] = UNSET
    current_employer_net: Union[Unset, float] = UNSET
    student_loan_deductions: Union[Unset, float] = UNSET
    postgrad_loan_deductions: Union[Unset, float] = UNSET
    empee_pen_contribns_paid: Union[Unset, float] = UNSET
    empee_pen_contribns_not_paid: Union[Unset, float] = UNSET
    smp: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET
    real_time_class_1a_ni: Union[Unset, float] = UNSET
    termination_payments: Union[Unset, float] = UNSET
    maps_miles: Union[Unset, int] = UNSET
    benefits_taxed_via_payroll: Union[Unset, float] = UNSET
    nic_summaries: Union[Unset, None, List[NicSummary]] = UNSET
    employee: Union[Unset, Item] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        not_new_starter = self.not_new_starter
        previous_employer_gross = self.previous_employer_gross
        previous_employer_tax = self.previous_employer_tax
        current_employer_gross = self.current_employer_gross
        current_employer_tax = self.current_employer_tax
        current_employer_net = self.current_employer_net
        student_loan_deductions = self.student_loan_deductions
        postgrad_loan_deductions = self.postgrad_loan_deductions
        empee_pen_contribns_paid = self.empee_pen_contribns_paid
        empee_pen_contribns_not_paid = self.empee_pen_contribns_not_paid
        smp = self.smp
        spp = self.spp
        sap = self.sap
        shpp = self.shpp
        spbp = self.spbp
        real_time_class_1a_ni = self.real_time_class_1a_ni
        termination_payments = self.termination_payments
        maps_miles = self.maps_miles
        benefits_taxed_via_payroll = self.benefits_taxed_via_payroll
        nic_summaries: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.nic_summaries, Unset):
            if self.nic_summaries is None:
                nic_summaries = None
            else:
                nic_summaries = []
                for nic_summaries_item_data in self.nic_summaries:
                    nic_summaries_item = nic_summaries_item_data.to_dict()

                    nic_summaries.append(nic_summaries_item)

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if not_new_starter is not UNSET:
            field_dict["notNewStarter"] = not_new_starter
        if previous_employer_gross is not UNSET:
            field_dict["previousEmployerGross"] = previous_employer_gross
        if previous_employer_tax is not UNSET:
            field_dict["previousEmployerTax"] = previous_employer_tax
        if current_employer_gross is not UNSET:
            field_dict["currentEmployerGross"] = current_employer_gross
        if current_employer_tax is not UNSET:
            field_dict["currentEmployerTax"] = current_employer_tax
        if current_employer_net is not UNSET:
            field_dict["currentEmployerNet"] = current_employer_net
        if student_loan_deductions is not UNSET:
            field_dict["studentLoanDeductions"] = student_loan_deductions
        if postgrad_loan_deductions is not UNSET:
            field_dict["postgradLoanDeductions"] = postgrad_loan_deductions
        if empee_pen_contribns_paid is not UNSET:
            field_dict["empeePenContribnsPaid"] = empee_pen_contribns_paid
        if empee_pen_contribns_not_paid is not UNSET:
            field_dict["empeePenContribnsNotPaid"] = empee_pen_contribns_not_paid
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
        if real_time_class_1a_ni is not UNSET:
            field_dict["realTimeClass1ANi"] = real_time_class_1a_ni
        if termination_payments is not UNSET:
            field_dict["terminationPayments"] = termination_payments
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if benefits_taxed_via_payroll is not UNSET:
            field_dict["benefitsTaxedViaPayroll"] = benefits_taxed_via_payroll
        if nic_summaries is not UNSET:
            field_dict["nicSummaries"] = nic_summaries
        if employee is not UNSET:
            field_dict["employee"] = employee

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

        not_new_starter = d.pop("notNewStarter", UNSET)

        previous_employer_gross = d.pop("previousEmployerGross", UNSET)

        previous_employer_tax = d.pop("previousEmployerTax", UNSET)

        current_employer_gross = d.pop("currentEmployerGross", UNSET)

        current_employer_tax = d.pop("currentEmployerTax", UNSET)

        current_employer_net = d.pop("currentEmployerNet", UNSET)

        student_loan_deductions = d.pop("studentLoanDeductions", UNSET)

        postgrad_loan_deductions = d.pop("postgradLoanDeductions", UNSET)

        empee_pen_contribns_paid = d.pop("empeePenContribnsPaid", UNSET)

        empee_pen_contribns_not_paid = d.pop("empeePenContribnsNotPaid", UNSET)

        smp = d.pop("smp", UNSET)

        spp = d.pop("spp", UNSET)

        sap = d.pop("sap", UNSET)

        shpp = d.pop("shpp", UNSET)

        spbp = d.pop("spbp", UNSET)

        real_time_class_1a_ni = d.pop("realTimeClass1ANi", UNSET)

        termination_payments = d.pop("terminationPayments", UNSET)

        maps_miles = d.pop("mapsMiles", UNSET)

        benefits_taxed_via_payroll = d.pop("benefitsTaxedViaPayroll", UNSET)

        nic_summaries = []
        _nic_summaries = d.pop("nicSummaries", UNSET)
        for nic_summaries_item_data in _nic_summaries or []:
            nic_summaries_item = NicSummary.from_dict(nic_summaries_item_data)

            nic_summaries.append(nic_summaries_item)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        opening_balances = cls(
            tax_year=tax_year,
            not_new_starter=not_new_starter,
            previous_employer_gross=previous_employer_gross,
            previous_employer_tax=previous_employer_tax,
            current_employer_gross=current_employer_gross,
            current_employer_tax=current_employer_tax,
            current_employer_net=current_employer_net,
            student_loan_deductions=student_loan_deductions,
            postgrad_loan_deductions=postgrad_loan_deductions,
            empee_pen_contribns_paid=empee_pen_contribns_paid,
            empee_pen_contribns_not_paid=empee_pen_contribns_not_paid,
            smp=smp,
            spp=spp,
            sap=sap,
            shpp=shpp,
            spbp=spbp,
            real_time_class_1a_ni=real_time_class_1a_ni,
            termination_payments=termination_payments,
            maps_miles=maps_miles,
            benefits_taxed_via_payroll=benefits_taxed_via_payroll,
            nic_summaries=nic_summaries,
            employee=employee,
        )

        return opening_balances
