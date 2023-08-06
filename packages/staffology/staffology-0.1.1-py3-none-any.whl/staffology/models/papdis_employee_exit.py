import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeExit")


@attr.s(auto_attribs=True)
class PapdisEmployeeExit:
    """
    Attributes:
        exit_date (Union[Unset, datetime.date]): [readonly]
        exit_reason_code (Union[Unset, None, int]): [readonly]
        ae_opt_out_date (Union[Unset, None, datetime.date]): [readonly]
        ae_opt_out_reference (Union[Unset, None, str]): [readonly]
    """

    exit_date: Union[Unset, datetime.date] = UNSET
    exit_reason_code: Union[Unset, None, int] = UNSET
    ae_opt_out_date: Union[Unset, None, datetime.date] = UNSET
    ae_opt_out_reference: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        exit_date: Union[Unset, str] = UNSET
        if not isinstance(self.exit_date, Unset):
            exit_date = self.exit_date.isoformat()

        exit_reason_code = self.exit_reason_code
        ae_opt_out_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.ae_opt_out_date, Unset):
            ae_opt_out_date = (
                self.ae_opt_out_date.isoformat() if self.ae_opt_out_date else None
            )

        ae_opt_out_reference = self.ae_opt_out_reference

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if exit_date is not UNSET:
            field_dict["exitDate"] = exit_date
        if exit_reason_code is not UNSET:
            field_dict["exitReasonCode"] = exit_reason_code
        if ae_opt_out_date is not UNSET:
            field_dict["aeOptOutDate"] = ae_opt_out_date
        if ae_opt_out_reference is not UNSET:
            field_dict["aeOptOutReference"] = ae_opt_out_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _exit_date = d.pop("exitDate", UNSET)
        exit_date: Union[Unset, datetime.date]
        if isinstance(_exit_date, Unset):
            exit_date = UNSET
        else:
            exit_date = isoparse(_exit_date).date()

        exit_reason_code = d.pop("exitReasonCode", UNSET)

        _ae_opt_out_date = d.pop("aeOptOutDate", UNSET)
        ae_opt_out_date: Union[Unset, None, datetime.date]
        if _ae_opt_out_date is None:
            ae_opt_out_date = None
        elif isinstance(_ae_opt_out_date, Unset):
            ae_opt_out_date = UNSET
        else:
            ae_opt_out_date = isoparse(_ae_opt_out_date).date()

        ae_opt_out_reference = d.pop("aeOptOutReference", UNSET)

        papdis_employee_exit = cls(
            exit_date=exit_date,
            exit_reason_code=exit_reason_code,
            ae_opt_out_date=ae_opt_out_date,
            ae_opt_out_reference=ae_opt_out_reference,
        )

        return papdis_employee_exit
