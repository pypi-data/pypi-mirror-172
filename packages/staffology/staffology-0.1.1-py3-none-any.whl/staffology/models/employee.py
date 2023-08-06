from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.auto_enrolment import AutoEnrolment
from ..models.bank_details import BankDetails
from ..models.employee_status import EmployeeStatus
from ..models.employment_details import EmploymentDetails
from ..models.leave_settings import LeaveSettings
from ..models.pay_options import PayOptions
from ..models.personal_details import PersonalDetails
from ..models.right_to_work import RightToWork
from ..types import UNSET, Unset

T = TypeVar("T", bound="Employee")


@attr.s(auto_attribs=True)
class Employee:
    """
    Attributes:
        has_pension (Union[Unset, bool]):
        id (Union[Unset, str]): [readonly] The unique id of the object
        personal_details (Union[Unset, PersonalDetails]):
        employment_details (Union[Unset, EmploymentDetails]):
        auto_enrolment (Union[Unset, AutoEnrolment]):
        leave_settings (Union[Unset, LeaveSettings]):
        right_to_work (Union[Unset, RightToWork]):
        bank_details (Union[Unset, BankDetails]):
        tags (Union[Unset, None, List[str]]):
        pay_options (Union[Unset, PayOptions]): This object forms the basis of the Employees payment.
        status (Union[Unset, EmployeeStatus]): [readonly] Indicates whether the Employee is currently employed or not
        ae_not_enroled_warning (Union[Unset, bool]): [readonly] If true then the employee should be enrolled in an Auto
            Enrolment Qualifying pension but isn't
        source_system_id (Union[Unset, None, str]): [readonly] Can only be given a value when the employee is created.
            It can then never be changed.
            Used by external systems so they can store an immutable reference
    """

    has_pension: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    personal_details: Union[Unset, PersonalDetails] = UNSET
    employment_details: Union[Unset, EmploymentDetails] = UNSET
    auto_enrolment: Union[Unset, AutoEnrolment] = UNSET
    leave_settings: Union[Unset, LeaveSettings] = UNSET
    right_to_work: Union[Unset, RightToWork] = UNSET
    bank_details: Union[Unset, BankDetails] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    pay_options: Union[Unset, PayOptions] = UNSET
    status: Union[Unset, EmployeeStatus] = UNSET
    ae_not_enroled_warning: Union[Unset, bool] = UNSET
    source_system_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        has_pension = self.has_pension
        id = self.id
        personal_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.personal_details, Unset):
            personal_details = self.personal_details.to_dict()

        employment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employment_details, Unset):
            employment_details = self.employment_details.to_dict()

        auto_enrolment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.auto_enrolment, Unset):
            auto_enrolment = self.auto_enrolment.to_dict()

        leave_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leave_settings, Unset):
            leave_settings = self.leave_settings.to_dict()

        right_to_work: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.right_to_work, Unset):
            right_to_work = self.right_to_work.to_dict()

        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        ae_not_enroled_warning = self.ae_not_enroled_warning
        source_system_id = self.source_system_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if has_pension is not UNSET:
            field_dict["hasPension"] = has_pension
        if id is not UNSET:
            field_dict["id"] = id
        if personal_details is not UNSET:
            field_dict["personalDetails"] = personal_details
        if employment_details is not UNSET:
            field_dict["employmentDetails"] = employment_details
        if auto_enrolment is not UNSET:
            field_dict["autoEnrolment"] = auto_enrolment
        if leave_settings is not UNSET:
            field_dict["leaveSettings"] = leave_settings
        if right_to_work is not UNSET:
            field_dict["rightToWork"] = right_to_work
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if tags is not UNSET:
            field_dict["tags"] = tags
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options
        if status is not UNSET:
            field_dict["status"] = status
        if ae_not_enroled_warning is not UNSET:
            field_dict["aeNotEnroledWarning"] = ae_not_enroled_warning
        if source_system_id is not UNSET:
            field_dict["sourceSystemId"] = source_system_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        has_pension = d.pop("hasPension", UNSET)

        id = d.pop("id", UNSET)

        _personal_details = d.pop("personalDetails", UNSET)
        personal_details: Union[Unset, PersonalDetails]
        if isinstance(_personal_details, Unset):
            personal_details = UNSET
        else:
            personal_details = PersonalDetails.from_dict(_personal_details)

        _employment_details = d.pop("employmentDetails", UNSET)
        employment_details: Union[Unset, EmploymentDetails]
        if isinstance(_employment_details, Unset):
            employment_details = UNSET
        else:
            employment_details = EmploymentDetails.from_dict(_employment_details)

        _auto_enrolment = d.pop("autoEnrolment", UNSET)
        auto_enrolment: Union[Unset, AutoEnrolment]
        if isinstance(_auto_enrolment, Unset):
            auto_enrolment = UNSET
        else:
            auto_enrolment = AutoEnrolment.from_dict(_auto_enrolment)

        _leave_settings = d.pop("leaveSettings", UNSET)
        leave_settings: Union[Unset, LeaveSettings]
        if isinstance(_leave_settings, Unset):
            leave_settings = UNSET
        else:
            leave_settings = LeaveSettings.from_dict(_leave_settings)

        _right_to_work = d.pop("rightToWork", UNSET)
        right_to_work: Union[Unset, RightToWork]
        if isinstance(_right_to_work, Unset):
            right_to_work = UNSET
        else:
            right_to_work = RightToWork.from_dict(_right_to_work)

        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details, Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)

        tags = cast(List[str], d.pop("tags", UNSET))

        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, PayOptions]
        if isinstance(_pay_options, Unset):
            pay_options = UNSET
        else:
            pay_options = PayOptions.from_dict(_pay_options)

        _status = d.pop("status", UNSET)
        status: Union[Unset, EmployeeStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = EmployeeStatus(_status)

        ae_not_enroled_warning = d.pop("aeNotEnroledWarning", UNSET)

        source_system_id = d.pop("sourceSystemId", UNSET)

        employee = cls(
            has_pension=has_pension,
            id=id,
            personal_details=personal_details,
            employment_details=employment_details,
            auto_enrolment=auto_enrolment,
            leave_settings=leave_settings,
            right_to_work=right_to_work,
            bank_details=bank_details,
            tags=tags,
            pay_options=pay_options,
            status=status,
            ae_not_enroled_warning=ae_not_enroled_warning,
            source_system_id=source_system_id,
        )

        return employee
