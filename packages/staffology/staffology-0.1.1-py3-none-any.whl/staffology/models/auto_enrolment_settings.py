import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.deferal_period_type import DeferalPeriodType
from ..models.pension_selection import PensionSelection
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoEnrolmentSettings")


@attr.s(auto_attribs=True)
class AutoEnrolmentSettings:
    """
    Attributes:
        staging_date (Union[Unset, datetime.date]):
        cyclical_reenrolment_date (Union[Unset, None, datetime.date]):
        previous_cyclical_reenrolment_date (Union[Unset, None, datetime.date]):
        default_pension (Union[Unset, PensionSelection]):
        pension_same_as_default (Union[Unset, bool]):
        days_to_defer_assessment (Union[Unset, int]): The number of days, if any, to defer assessment of new employees.
            You're allowed to defer assessment of new employees by up to 3 months.
            This is the default value used when you create a new employee. It can be changed on a per-employee basis.
        defer_by_months_not_days (Union[Unset, bool]): If set to true then the value in DaysToDeferAssessment will be
            treated as a number of months, not a number of days
        defer_enrolment_by (Union[Unset, int]): The number of days )or weeks, or months), if any, to defer enrolment of
            employees that are Eligible Jobholders.
            For example, if this is set to 30 days then if an employee meets the criteria for enrolment then they'll only be
            enrolled if they still meet the criteria 30 days later
        defer_enrolment_by_period_type (Union[Unset, DeferalPeriodType]):
        include_non_pensioned_employees_in_submission (Union[Unset, bool]): Whether or not to include details of non-
            pensioned employees in your submissions to this provider
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    staging_date: Union[Unset, datetime.date] = UNSET
    cyclical_reenrolment_date: Union[Unset, None, datetime.date] = UNSET
    previous_cyclical_reenrolment_date: Union[Unset, None, datetime.date] = UNSET
    default_pension: Union[Unset, PensionSelection] = UNSET
    pension_same_as_default: Union[Unset, bool] = UNSET
    days_to_defer_assessment: Union[Unset, int] = UNSET
    defer_by_months_not_days: Union[Unset, bool] = UNSET
    defer_enrolment_by: Union[Unset, int] = UNSET
    defer_enrolment_by_period_type: Union[Unset, DeferalPeriodType] = UNSET
    include_non_pensioned_employees_in_submission: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        staging_date: Union[Unset, str] = UNSET
        if not isinstance(self.staging_date, Unset):
            staging_date = self.staging_date.isoformat()

        cyclical_reenrolment_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.cyclical_reenrolment_date, Unset):
            cyclical_reenrolment_date = (
                self.cyclical_reenrolment_date.isoformat()
                if self.cyclical_reenrolment_date
                else None
            )

        previous_cyclical_reenrolment_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.previous_cyclical_reenrolment_date, Unset):
            previous_cyclical_reenrolment_date = (
                self.previous_cyclical_reenrolment_date.isoformat()
                if self.previous_cyclical_reenrolment_date
                else None
            )

        default_pension: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_pension, Unset):
            default_pension = self.default_pension.to_dict()

        pension_same_as_default = self.pension_same_as_default
        days_to_defer_assessment = self.days_to_defer_assessment
        defer_by_months_not_days = self.defer_by_months_not_days
        defer_enrolment_by = self.defer_enrolment_by
        defer_enrolment_by_period_type: Union[Unset, str] = UNSET
        if not isinstance(self.defer_enrolment_by_period_type, Unset):
            defer_enrolment_by_period_type = self.defer_enrolment_by_period_type.value

        include_non_pensioned_employees_in_submission = (
            self.include_non_pensioned_employees_in_submission
        )
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if staging_date is not UNSET:
            field_dict["stagingDate"] = staging_date
        if cyclical_reenrolment_date is not UNSET:
            field_dict["cyclicalReenrolmentDate"] = cyclical_reenrolment_date
        if previous_cyclical_reenrolment_date is not UNSET:
            field_dict[
                "previousCyclicalReenrolmentDate"
            ] = previous_cyclical_reenrolment_date
        if default_pension is not UNSET:
            field_dict["defaultPension"] = default_pension
        if pension_same_as_default is not UNSET:
            field_dict["pensionSameAsDefault"] = pension_same_as_default
        if days_to_defer_assessment is not UNSET:
            field_dict["daysToDeferAssessment"] = days_to_defer_assessment
        if defer_by_months_not_days is not UNSET:
            field_dict["deferByMonthsNotDays"] = defer_by_months_not_days
        if defer_enrolment_by is not UNSET:
            field_dict["deferEnrolmentBy"] = defer_enrolment_by
        if defer_enrolment_by_period_type is not UNSET:
            field_dict["deferEnrolmentByPeriodType"] = defer_enrolment_by_period_type
        if include_non_pensioned_employees_in_submission is not UNSET:
            field_dict[
                "includeNonPensionedEmployeesInSubmission"
            ] = include_non_pensioned_employees_in_submission
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _staging_date = d.pop("stagingDate", UNSET)
        staging_date: Union[Unset, datetime.date]
        if isinstance(_staging_date, Unset):
            staging_date = UNSET
        else:
            staging_date = isoparse(_staging_date).date()

        _cyclical_reenrolment_date = d.pop("cyclicalReenrolmentDate", UNSET)
        cyclical_reenrolment_date: Union[Unset, None, datetime.date]
        if _cyclical_reenrolment_date is None:
            cyclical_reenrolment_date = None
        elif isinstance(_cyclical_reenrolment_date, Unset):
            cyclical_reenrolment_date = UNSET
        else:
            cyclical_reenrolment_date = isoparse(_cyclical_reenrolment_date).date()

        _previous_cyclical_reenrolment_date = d.pop(
            "previousCyclicalReenrolmentDate", UNSET
        )
        previous_cyclical_reenrolment_date: Union[Unset, None, datetime.date]
        if _previous_cyclical_reenrolment_date is None:
            previous_cyclical_reenrolment_date = None
        elif isinstance(_previous_cyclical_reenrolment_date, Unset):
            previous_cyclical_reenrolment_date = UNSET
        else:
            previous_cyclical_reenrolment_date = isoparse(
                _previous_cyclical_reenrolment_date
            ).date()

        _default_pension = d.pop("defaultPension", UNSET)
        default_pension: Union[Unset, PensionSelection]
        if isinstance(_default_pension, Unset):
            default_pension = UNSET
        else:
            default_pension = PensionSelection.from_dict(_default_pension)

        pension_same_as_default = d.pop("pensionSameAsDefault", UNSET)

        days_to_defer_assessment = d.pop("daysToDeferAssessment", UNSET)

        defer_by_months_not_days = d.pop("deferByMonthsNotDays", UNSET)

        defer_enrolment_by = d.pop("deferEnrolmentBy", UNSET)

        _defer_enrolment_by_period_type = d.pop("deferEnrolmentByPeriodType", UNSET)
        defer_enrolment_by_period_type: Union[Unset, DeferalPeriodType]
        if isinstance(_defer_enrolment_by_period_type, Unset):
            defer_enrolment_by_period_type = UNSET
        else:
            defer_enrolment_by_period_type = DeferalPeriodType(
                _defer_enrolment_by_period_type
            )

        include_non_pensioned_employees_in_submission = d.pop(
            "includeNonPensionedEmployeesInSubmission", UNSET
        )

        id = d.pop("id", UNSET)

        auto_enrolment_settings = cls(
            staging_date=staging_date,
            cyclical_reenrolment_date=cyclical_reenrolment_date,
            previous_cyclical_reenrolment_date=previous_cyclical_reenrolment_date,
            default_pension=default_pension,
            pension_same_as_default=pension_same_as_default,
            days_to_defer_assessment=days_to_defer_assessment,
            defer_by_months_not_days=defer_by_months_not_days,
            defer_enrolment_by=defer_enrolment_by,
            defer_enrolment_by_period_type=defer_enrolment_by_period_type,
            include_non_pensioned_employees_in_submission=include_non_pensioned_employees_in_submission,
            id=id,
        )

        return auto_enrolment_settings
