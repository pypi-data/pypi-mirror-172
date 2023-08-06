from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.fps_employee_figs_to_date import FpsEmployeeFigsToDate
from ..models.fps_employee_n_iletters_and_values import FpsEmployeeNIlettersAndValues
from ..models.fps_employee_payment import FpsEmployeePayment
from ..models.fps_employee_starter import FpsEmployeeStarter
from ..models.fps_employer_pay_id_changed import FpsEmployerPayIdChanged
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployment")


@attr.s(auto_attribs=True)
class FpsEmployment:
    """
    Attributes:
        employee_current_ni_letter (Union[Unset, None, str]):
        off_payroll_worker (Union[Unset, None, str]):
        occ_pen_ind (Union[Unset, None, str]):
        directors_nic (Union[Unset, None, str]):
        tax_wk_of_appt_of_director (Union[Unset, None, str]):
        starter (Union[Unset, FpsEmployeeStarter]):
        pay_id (Union[Unset, None, str]):
        pay_id_chgd (Union[Unset, FpsEmployerPayIdChanged]):
        payment_to_a_non_individual (Union[Unset, None, str]):
        irr_emp (Union[Unset, None, str]):
        leaving_date (Union[Unset, None, str]):
        figures_to_date (Union[Unset, FpsEmployeeFigsToDate]):
        payment (Union[Unset, FpsEmployeePayment]):
        n_iletters_and_values (Union[Unset, None, List[FpsEmployeeNIlettersAndValues]]):
    """

    employee_current_ni_letter: Union[Unset, None, str] = UNSET
    off_payroll_worker: Union[Unset, None, str] = UNSET
    occ_pen_ind: Union[Unset, None, str] = UNSET
    directors_nic: Union[Unset, None, str] = UNSET
    tax_wk_of_appt_of_director: Union[Unset, None, str] = UNSET
    starter: Union[Unset, FpsEmployeeStarter] = UNSET
    pay_id: Union[Unset, None, str] = UNSET
    pay_id_chgd: Union[Unset, FpsEmployerPayIdChanged] = UNSET
    payment_to_a_non_individual: Union[Unset, None, str] = UNSET
    irr_emp: Union[Unset, None, str] = UNSET
    leaving_date: Union[Unset, None, str] = UNSET
    figures_to_date: Union[Unset, FpsEmployeeFigsToDate] = UNSET
    payment: Union[Unset, FpsEmployeePayment] = UNSET
    n_iletters_and_values: Union[
        Unset, None, List[FpsEmployeeNIlettersAndValues]
    ] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_current_ni_letter = self.employee_current_ni_letter
        off_payroll_worker = self.off_payroll_worker
        occ_pen_ind = self.occ_pen_ind
        directors_nic = self.directors_nic
        tax_wk_of_appt_of_director = self.tax_wk_of_appt_of_director
        starter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.starter, Unset):
            starter = self.starter.to_dict()

        pay_id = self.pay_id
        pay_id_chgd: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_id_chgd, Unset):
            pay_id_chgd = self.pay_id_chgd.to_dict()

        payment_to_a_non_individual = self.payment_to_a_non_individual
        irr_emp = self.irr_emp
        leaving_date = self.leaving_date
        figures_to_date: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.figures_to_date, Unset):
            figures_to_date = self.figures_to_date.to_dict()

        payment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payment, Unset):
            payment = self.payment.to_dict()

        n_iletters_and_values: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.n_iletters_and_values, Unset):
            if self.n_iletters_and_values is None:
                n_iletters_and_values = None
            else:
                n_iletters_and_values = []
                for n_iletters_and_values_item_data in self.n_iletters_and_values:
                    n_iletters_and_values_item = (
                        n_iletters_and_values_item_data.to_dict()
                    )

                    n_iletters_and_values.append(n_iletters_and_values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_current_ni_letter is not UNSET:
            field_dict["employeeCurrentNiLetter"] = employee_current_ni_letter
        if off_payroll_worker is not UNSET:
            field_dict["offPayrollWorker"] = off_payroll_worker
        if occ_pen_ind is not UNSET:
            field_dict["occPenInd"] = occ_pen_ind
        if directors_nic is not UNSET:
            field_dict["directorsNIC"] = directors_nic
        if tax_wk_of_appt_of_director is not UNSET:
            field_dict["taxWkOfApptOfDirector"] = tax_wk_of_appt_of_director
        if starter is not UNSET:
            field_dict["starter"] = starter
        if pay_id is not UNSET:
            field_dict["payId"] = pay_id
        if pay_id_chgd is not UNSET:
            field_dict["payIdChgd"] = pay_id_chgd
        if payment_to_a_non_individual is not UNSET:
            field_dict["paymentToANonIndividual"] = payment_to_a_non_individual
        if irr_emp is not UNSET:
            field_dict["irrEmp"] = irr_emp
        if leaving_date is not UNSET:
            field_dict["leavingDate"] = leaving_date
        if figures_to_date is not UNSET:
            field_dict["figuresToDate"] = figures_to_date
        if payment is not UNSET:
            field_dict["payment"] = payment
        if n_iletters_and_values is not UNSET:
            field_dict["nIlettersAndValues"] = n_iletters_and_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_current_ni_letter = d.pop("employeeCurrentNiLetter", UNSET)

        off_payroll_worker = d.pop("offPayrollWorker", UNSET)

        occ_pen_ind = d.pop("occPenInd", UNSET)

        directors_nic = d.pop("directorsNIC", UNSET)

        tax_wk_of_appt_of_director = d.pop("taxWkOfApptOfDirector", UNSET)

        _starter = d.pop("starter", UNSET)
        starter: Union[Unset, FpsEmployeeStarter]
        if isinstance(_starter, Unset):
            starter = UNSET
        else:
            starter = FpsEmployeeStarter.from_dict(_starter)

        pay_id = d.pop("payId", UNSET)

        _pay_id_chgd = d.pop("payIdChgd", UNSET)
        pay_id_chgd: Union[Unset, FpsEmployerPayIdChanged]
        if isinstance(_pay_id_chgd, Unset):
            pay_id_chgd = UNSET
        else:
            pay_id_chgd = FpsEmployerPayIdChanged.from_dict(_pay_id_chgd)

        payment_to_a_non_individual = d.pop("paymentToANonIndividual", UNSET)

        irr_emp = d.pop("irrEmp", UNSET)

        leaving_date = d.pop("leavingDate", UNSET)

        _figures_to_date = d.pop("figuresToDate", UNSET)
        figures_to_date: Union[Unset, FpsEmployeeFigsToDate]
        if isinstance(_figures_to_date, Unset):
            figures_to_date = UNSET
        else:
            figures_to_date = FpsEmployeeFigsToDate.from_dict(_figures_to_date)

        _payment = d.pop("payment", UNSET)
        payment: Union[Unset, FpsEmployeePayment]
        if isinstance(_payment, Unset):
            payment = UNSET
        else:
            payment = FpsEmployeePayment.from_dict(_payment)

        n_iletters_and_values = []
        _n_iletters_and_values = d.pop("nIlettersAndValues", UNSET)
        for n_iletters_and_values_item_data in _n_iletters_and_values or []:
            n_iletters_and_values_item = FpsEmployeeNIlettersAndValues.from_dict(
                n_iletters_and_values_item_data
            )

            n_iletters_and_values.append(n_iletters_and_values_item)

        fps_employment = cls(
            employee_current_ni_letter=employee_current_ni_letter,
            off_payroll_worker=off_payroll_worker,
            occ_pen_ind=occ_pen_ind,
            directors_nic=directors_nic,
            tax_wk_of_appt_of_director=tax_wk_of_appt_of_director,
            starter=starter,
            pay_id=pay_id,
            pay_id_chgd=pay_id_chgd,
            payment_to_a_non_individual=payment_to_a_non_individual,
            irr_emp=irr_emp,
            leaving_date=leaving_date,
            figures_to_date=figures_to_date,
            payment=payment,
            n_iletters_and_values=n_iletters_and_values,
        )

        return fps_employment
