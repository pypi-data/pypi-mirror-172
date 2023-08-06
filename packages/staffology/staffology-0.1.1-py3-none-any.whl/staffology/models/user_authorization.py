from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.employer_item import EmployerItem
from ..models.tenant_item import TenantItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserAuthorization")


@attr.s(auto_attribs=True)
class UserAuthorization:
    """This model provides information about what the User is able to access.
    This would usually just be a list of Employers. But if the user is an administrator for a White Label instance then
    this will be shown in the list of Tenants.

        Attributes:
            employers (Union[Unset, None, List[EmployerItem]]): [readonly] A list of any Employers that the user can access
            tenants (Union[Unset, None, List[TenantItem]]): [readonly] A list of any Tenants that the user can administrate
    """

    employers: Union[Unset, None, List[EmployerItem]] = UNSET
    tenants: Union[Unset, None, List[TenantItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.employers, Unset):
            if self.employers is None:
                employers = None
            else:
                employers = []
                for employers_item_data in self.employers:
                    employers_item = employers_item_data.to_dict()

                    employers.append(employers_item)

        tenants: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tenants, Unset):
            if self.tenants is None:
                tenants = None
            else:
                tenants = []
                for tenants_item_data in self.tenants:
                    tenants_item = tenants_item_data.to_dict()

                    tenants.append(tenants_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employers is not UNSET:
            field_dict["employers"] = employers
        if tenants is not UNSET:
            field_dict["tenants"] = tenants

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employers = []
        _employers = d.pop("employers", UNSET)
        for employers_item_data in _employers or []:
            employers_item = EmployerItem.from_dict(employers_item_data)

            employers.append(employers_item)

        tenants = []
        _tenants = d.pop("tenants", UNSET)
        for tenants_item_data in _tenants or []:
            tenants_item = TenantItem.from_dict(tenants_item_data)

            tenants.append(tenants_item)

        user_authorization = cls(
            employers=employers,
            tenants=tenants,
        )

        return user_authorization
