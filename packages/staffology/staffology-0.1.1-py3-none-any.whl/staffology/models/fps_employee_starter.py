from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fps_employee_starter_occ_pension import FpsEmployeeStarterOccPension
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeStarter")


@attr.s(auto_attribs=True)
class FpsEmployeeStarter:
    """
    Attributes:
        start_date (Union[Unset, None, str]):
        start_dec (Union[Unset, None, str]):
        student_loan (Union[Unset, None, str]):
        postgrad_loan (Union[Unset, None, str]):
        occ_pension (Union[Unset, FpsEmployeeStarterOccPension]):
    """

    start_date: Union[Unset, None, str] = UNSET
    start_dec: Union[Unset, None, str] = UNSET
    student_loan: Union[Unset, None, str] = UNSET
    postgrad_loan: Union[Unset, None, str] = UNSET
    occ_pension: Union[Unset, FpsEmployeeStarterOccPension] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start_date = self.start_date
        start_dec = self.start_dec
        student_loan = self.student_loan
        postgrad_loan = self.postgrad_loan
        occ_pension: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.occ_pension, Unset):
            occ_pension = self.occ_pension.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if start_dec is not UNSET:
            field_dict["startDec"] = start_dec
        if student_loan is not UNSET:
            field_dict["studentLoan"] = student_loan
        if postgrad_loan is not UNSET:
            field_dict["postgradLoan"] = postgrad_loan
        if occ_pension is not UNSET:
            field_dict["occPension"] = occ_pension

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_date = d.pop("startDate", UNSET)

        start_dec = d.pop("startDec", UNSET)

        student_loan = d.pop("studentLoan", UNSET)

        postgrad_loan = d.pop("postgradLoan", UNSET)

        _occ_pension = d.pop("occPension", UNSET)
        occ_pension: Union[Unset, FpsEmployeeStarterOccPension]
        if isinstance(_occ_pension, Unset):
            occ_pension = UNSET
        else:
            occ_pension = FpsEmployeeStarterOccPension.from_dict(_occ_pension)

        fps_employee_starter = cls(
            start_date=start_date,
            start_dec=start_dec,
            student_loan=student_loan,
            postgrad_loan=postgrad_loan,
            occ_pension=occ_pension,
        )

        return fps_employee_starter
