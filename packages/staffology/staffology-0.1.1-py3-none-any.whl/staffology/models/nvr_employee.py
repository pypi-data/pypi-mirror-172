from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..models.nvr_employee_details import NvrEmployeeDetails
from ..models.nvr_employment import NvrEmployment
from ..types import UNSET, Unset

T = TypeVar("T", bound="NvrEmployee")


@attr.s(auto_attribs=True)
class NvrEmployee:
    """
    Attributes:
        employee_unique_id (Union[Unset, str]):
        item (Union[Unset, Item]):
        employee_details (Union[Unset, NvrEmployeeDetails]):
        employment (Union[Unset, NvrEmployment]):
    """

    employee_unique_id: Union[Unset, str] = UNSET
    item: Union[Unset, Item] = UNSET
    employee_details: Union[Unset, NvrEmployeeDetails] = UNSET
    employment: Union[Unset, NvrEmployment] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_unique_id = self.employee_unique_id
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        employee_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee_details, Unset):
            employee_details = self.employee_details.to_dict()

        employment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employment, Unset):
            employment = self.employment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_unique_id is not UNSET:
            field_dict["employeeUniqueId"] = employee_unique_id
        if item is not UNSET:
            field_dict["item"] = item
        if employee_details is not UNSET:
            field_dict["employeeDetails"] = employee_details
        if employment is not UNSET:
            field_dict["employment"] = employment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_unique_id = d.pop("employeeUniqueId", UNSET)

        _item = d.pop("item", UNSET)
        item: Union[Unset, Item]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = Item.from_dict(_item)

        _employee_details = d.pop("employeeDetails", UNSET)
        employee_details: Union[Unset, NvrEmployeeDetails]
        if isinstance(_employee_details, Unset):
            employee_details = UNSET
        else:
            employee_details = NvrEmployeeDetails.from_dict(_employee_details)

        _employment = d.pop("employment", UNSET)
        employment: Union[Unset, NvrEmployment]
        if isinstance(_employment, Unset):
            employment = UNSET
        else:
            employment = NvrEmployment.from_dict(_employment)

        nvr_employee = cls(
            employee_unique_id=employee_unique_id,
            item=item,
            employee_details=employee_details,
            employment=employment,
        )

        return nvr_employee
