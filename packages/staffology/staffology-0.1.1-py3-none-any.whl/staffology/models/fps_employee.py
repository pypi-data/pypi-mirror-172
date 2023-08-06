from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.fps_employee_details import FpsEmployeeDetails
from ..models.fps_employment import FpsEmployment
from ..models.item import Item
from ..models.rti_validation_warning import RtiValidationWarning
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployee")


@attr.s(auto_attribs=True)
class FpsEmployee:
    """
    Attributes:
        employee_unique_id (Union[Unset, str]):
        item (Union[Unset, Item]):
        employee_details (Union[Unset, FpsEmployeeDetails]):
        employment (Union[Unset, FpsEmployment]):
        validation_warnings (Union[Unset, None, List[RtiValidationWarning]]):
    """

    employee_unique_id: Union[Unset, str] = UNSET
    item: Union[Unset, Item] = UNSET
    employee_details: Union[Unset, FpsEmployeeDetails] = UNSET
    employment: Union[Unset, FpsEmployment] = UNSET
    validation_warnings: Union[Unset, None, List[RtiValidationWarning]] = UNSET

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

        validation_warnings: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.validation_warnings, Unset):
            if self.validation_warnings is None:
                validation_warnings = None
            else:
                validation_warnings = []
                for validation_warnings_item_data in self.validation_warnings:
                    validation_warnings_item = validation_warnings_item_data.to_dict()

                    validation_warnings.append(validation_warnings_item)

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
        if validation_warnings is not UNSET:
            field_dict["validationWarnings"] = validation_warnings

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
        employee_details: Union[Unset, FpsEmployeeDetails]
        if isinstance(_employee_details, Unset):
            employee_details = UNSET
        else:
            employee_details = FpsEmployeeDetails.from_dict(_employee_details)

        _employment = d.pop("employment", UNSET)
        employment: Union[Unset, FpsEmployment]
        if isinstance(_employment, Unset):
            employment = UNSET
        else:
            employment = FpsEmployment.from_dict(_employment)

        validation_warnings = []
        _validation_warnings = d.pop("validationWarnings", UNSET)
        for validation_warnings_item_data in _validation_warnings or []:
            validation_warnings_item = RtiValidationWarning.from_dict(
                validation_warnings_item_data
            )

            validation_warnings.append(validation_warnings_item)

        fps_employee = cls(
            employee_unique_id=employee_unique_id,
            item=item,
            employee_details=employee_details,
            employment=employment,
            validation_warnings=validation_warnings,
        )

        return fps_employee
