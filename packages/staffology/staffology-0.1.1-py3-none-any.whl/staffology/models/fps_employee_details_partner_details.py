from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.rti_employee_name import RtiEmployeeName
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeDetailsPartnerDetails")


@attr.s(auto_attribs=True)
class FpsEmployeeDetailsPartnerDetails:
    """
    Attributes:
        nino (Union[Unset, None, str]):
        name (Union[Unset, RtiEmployeeName]):
    """

    nino: Union[Unset, None, str] = UNSET
    name: Union[Unset, RtiEmployeeName] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        nino = self.nino
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if nino is not UNSET:
            field_dict["nino"] = nino
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nino = d.pop("nino", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, RtiEmployeeName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = RtiEmployeeName.from_dict(_name)

        fps_employee_details_partner_details = cls(
            nino=nino,
            name=name,
        )

        return fps_employee_details_partner_details
