from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.hours_normally_worked import HoursNormallyWorked
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsFields")


@attr.s(auto_attribs=True)
class FpsFields:
    """
    Attributes:
        off_payroll_worker (Union[Unset, bool]):
        irregular_payment_pattern (Union[Unset, bool]): True if employee is currently on an irregular payment patter
        non_individual (Union[Unset, bool]): True if Employee's payments are being made to a body (eg, trustee,
            corporate organisation or personal representative)
        hours_normally_worked (Union[Unset, HoursNormallyWorked]):
    """

    off_payroll_worker: Union[Unset, bool] = UNSET
    irregular_payment_pattern: Union[Unset, bool] = UNSET
    non_individual: Union[Unset, bool] = UNSET
    hours_normally_worked: Union[Unset, HoursNormallyWorked] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        off_payroll_worker = self.off_payroll_worker
        irregular_payment_pattern = self.irregular_payment_pattern
        non_individual = self.non_individual
        hours_normally_worked: Union[Unset, str] = UNSET
        if not isinstance(self.hours_normally_worked, Unset):
            hours_normally_worked = self.hours_normally_worked.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if off_payroll_worker is not UNSET:
            field_dict["offPayrollWorker"] = off_payroll_worker
        if irregular_payment_pattern is not UNSET:
            field_dict["irregularPaymentPattern"] = irregular_payment_pattern
        if non_individual is not UNSET:
            field_dict["nonIndividual"] = non_individual
        if hours_normally_worked is not UNSET:
            field_dict["hoursNormallyWorked"] = hours_normally_worked

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        off_payroll_worker = d.pop("offPayrollWorker", UNSET)

        irregular_payment_pattern = d.pop("irregularPaymentPattern", UNSET)

        non_individual = d.pop("nonIndividual", UNSET)

        _hours_normally_worked = d.pop("hoursNormallyWorked", UNSET)
        hours_normally_worked: Union[Unset, HoursNormallyWorked]
        if isinstance(_hours_normally_worked, Unset):
            hours_normally_worked = UNSET
        else:
            hours_normally_worked = HoursNormallyWorked(_hours_normally_worked)

        fps_fields = cls(
            off_payroll_worker=off_payroll_worker,
            irregular_payment_pattern=irregular_payment_pattern,
            non_individual=non_individual,
            hours_normally_worked=hours_normally_worked,
        )

        return fps_fields
