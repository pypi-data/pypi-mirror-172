from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.rti_validation_warning_type import RtiValidationWarningType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiValidationWarning")


@attr.s(auto_attribs=True)
class RtiValidationWarning:
    """
    Attributes:
        type (Union[Unset, RtiValidationWarningType]):
        employee_id (Union[Unset, None, str]):
    """

    type: Union[Unset, RtiValidationWarningType] = UNSET
    employee_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        employee_id = self.employee_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, RtiValidationWarningType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = RtiValidationWarningType(_type)

        employee_id = d.pop("employeeId", UNSET)

        rti_validation_warning = cls(
            type=type,
            employee_id=employee_id,
        )

        return rti_validation_warning
