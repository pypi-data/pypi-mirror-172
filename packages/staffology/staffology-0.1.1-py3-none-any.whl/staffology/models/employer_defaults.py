from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.employer_item import EmployerItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerDefaults")


@attr.s(auto_attribs=True)
class EmployerDefaults:
    """When a user creates a new Employer, certain settings can be copied from an existing employer.
    This model determines which employer (if any) settings should be copied from and what should be copied.

        Attributes:
            employer (Union[Unset, EmployerItem]):
            pay_codes (Union[Unset, bool]): If true then PayCodes will be copied from the specified Employer
            csv_mappings (Union[Unset, bool]): If true then CSV Mappings will be copied from the specified Employer
            departments (Union[Unset, bool]): If true then Departments will be copied from the specified Employer
            rti (Union[Unset, bool]): If true then RTI Settings will be copied from the specified Employer
            users (Union[Unset, bool]): If true then Users will be copied from the specified Employer
            hmrc_notice_settings (Union[Unset, bool]): If true then HMRC Notice Settings will be copied from the specified
                Employer
            pay_options (Union[Unset, bool]): If true then Default Pay Options will be copied from the specified Employer.
    """

    employer: Union[Unset, EmployerItem] = UNSET
    pay_codes: Union[Unset, bool] = UNSET
    csv_mappings: Union[Unset, bool] = UNSET
    departments: Union[Unset, bool] = UNSET
    rti: Union[Unset, bool] = UNSET
    users: Union[Unset, bool] = UNSET
    hmrc_notice_settings: Union[Unset, bool] = UNSET
    pay_options: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        pay_codes = self.pay_codes
        csv_mappings = self.csv_mappings
        departments = self.departments
        rti = self.rti
        users = self.users
        hmrc_notice_settings = self.hmrc_notice_settings
        pay_options = self.pay_options

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer is not UNSET:
            field_dict["employer"] = employer
        if pay_codes is not UNSET:
            field_dict["payCodes"] = pay_codes
        if csv_mappings is not UNSET:
            field_dict["csvMappings"] = csv_mappings
        if departments is not UNSET:
            field_dict["departments"] = departments
        if rti is not UNSET:
            field_dict["rti"] = rti
        if users is not UNSET:
            field_dict["users"] = users
        if hmrc_notice_settings is not UNSET:
            field_dict["hmrcNoticeSettings"] = hmrc_notice_settings
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, EmployerItem]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = EmployerItem.from_dict(_employer)

        pay_codes = d.pop("payCodes", UNSET)

        csv_mappings = d.pop("csvMappings", UNSET)

        departments = d.pop("departments", UNSET)

        rti = d.pop("rti", UNSET)

        users = d.pop("users", UNSET)

        hmrc_notice_settings = d.pop("hmrcNoticeSettings", UNSET)

        pay_options = d.pop("payOptions", UNSET)

        employer_defaults = cls(
            employer=employer,
            pay_codes=pay_codes,
            csv_mappings=csv_mappings,
            departments=departments,
            rti=rti,
            users=users,
            hmrc_notice_settings=hmrc_notice_settings,
            pay_options=pay_options,
        )

        return employer_defaults
