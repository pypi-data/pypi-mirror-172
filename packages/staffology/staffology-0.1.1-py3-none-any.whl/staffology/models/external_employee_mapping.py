import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.employee import Employee
from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.external_employee_mapping_status import ExternalEmployeeMappingStatus
from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalEmployeeMapping")


@attr.s(auto_attribs=True)
class ExternalEmployeeMapping:
    """Used to represent details of an employee from an ExternalDataProvider, along with mapping information to an employee
    in the payroll system

        Attributes:
            external_id (Union[Unset, None, str]): [readonly] The id for the employee in the external system
            provider_id (Union[Unset, ExternalDataProviderId]):
            status (Union[Unset, ExternalEmployeeMappingStatus]):
            employee (Union[Unset, Item]):
            external_employee (Union[Unset, Employee]):
            last_sync_date (Union[Unset, None, datetime.date]): [readonly] The date and time this mapping was last
                synchronised
    """

    external_id: Union[Unset, None, str] = UNSET
    provider_id: Union[Unset, ExternalDataProviderId] = UNSET
    status: Union[Unset, ExternalEmployeeMappingStatus] = UNSET
    employee: Union[Unset, Item] = UNSET
    external_employee: Union[Unset, Employee] = UNSET
    last_sync_date: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id
        provider_id: Union[Unset, str] = UNSET
        if not isinstance(self.provider_id, Unset):
            provider_id = self.provider_id.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        external_employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.external_employee, Unset):
            external_employee = self.external_employee.to_dict()

        last_sync_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_sync_date, Unset):
            last_sync_date = (
                self.last_sync_date.isoformat() if self.last_sync_date else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if provider_id is not UNSET:
            field_dict["providerId"] = provider_id
        if status is not UNSET:
            field_dict["status"] = status
        if employee is not UNSET:
            field_dict["employee"] = employee
        if external_employee is not UNSET:
            field_dict["externalEmployee"] = external_employee
        if last_sync_date is not UNSET:
            field_dict["lastSyncDate"] = last_sync_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_id = d.pop("externalId", UNSET)

        _provider_id = d.pop("providerId", UNSET)
        provider_id: Union[Unset, ExternalDataProviderId]
        if isinstance(_provider_id, Unset):
            provider_id = UNSET
        else:
            provider_id = ExternalDataProviderId(_provider_id)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExternalEmployeeMappingStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExternalEmployeeMappingStatus(_status)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        _external_employee = d.pop("externalEmployee", UNSET)
        external_employee: Union[Unset, Employee]
        if isinstance(_external_employee, Unset):
            external_employee = UNSET
        else:
            external_employee = Employee.from_dict(_external_employee)

        _last_sync_date = d.pop("lastSyncDate", UNSET)
        last_sync_date: Union[Unset, None, datetime.date]
        if _last_sync_date is None:
            last_sync_date = None
        elif isinstance(_last_sync_date, Unset):
            last_sync_date = UNSET
        else:
            last_sync_date = isoparse(_last_sync_date).date()

        external_employee_mapping = cls(
            external_id=external_id,
            provider_id=provider_id,
            status=status,
            employee=employee,
            external_employee=external_employee,
            last_sync_date=last_sync_date,
        )

        return external_employee_mapping
