from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pension_contribution_level_type import PensionContributionLevelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkerGroup")


@attr.s(auto_attribs=True)
class WorkerGroup:
    """
    Attributes:
        name (str):
        contribution_level_type (Union[Unset, PensionContributionLevelType]):
        employee_contribution (Union[Unset, float]):
        employee_contribution_is_percentage (Union[Unset, bool]):
        employer_contribution (Union[Unset, float]):
        employer_contribution_is_percentage (Union[Unset, bool]):
        employer_contribution_top_up_percentage (Union[Unset, float]): Increase Employer Contribution by this percentage
            of the Employee Contribution
        custom_threshold (Union[Unset, bool]):
        lower_limit (Union[Unset, float]):
        upper_limit (Union[Unset, float]):
        papdis_group (Union[Unset, None, str]):
        papdis_sub_group (Union[Unset, None, str]):
        local_authority_number (Union[Unset, None, str]): Only applicable if ContributionLevelType is Tp2020
        school_employer_type (Union[Unset, None, str]): Only applicable if ContributionLevelType is Tp2020
        worker_group_id (Union[Unset, str]): [readonly]
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    contribution_level_type: Union[Unset, PensionContributionLevelType] = UNSET
    employee_contribution: Union[Unset, float] = UNSET
    employee_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution: Union[Unset, float] = UNSET
    employer_contribution_is_percentage: Union[Unset, bool] = UNSET
    employer_contribution_top_up_percentage: Union[Unset, float] = UNSET
    custom_threshold: Union[Unset, bool] = UNSET
    lower_limit: Union[Unset, float] = UNSET
    upper_limit: Union[Unset, float] = UNSET
    papdis_group: Union[Unset, None, str] = UNSET
    papdis_sub_group: Union[Unset, None, str] = UNSET
    local_authority_number: Union[Unset, None, str] = UNSET
    school_employer_type: Union[Unset, None, str] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        contribution_level_type: Union[Unset, str] = UNSET
        if not isinstance(self.contribution_level_type, Unset):
            contribution_level_type = self.contribution_level_type.value

        employee_contribution = self.employee_contribution
        employee_contribution_is_percentage = self.employee_contribution_is_percentage
        employer_contribution = self.employer_contribution
        employer_contribution_is_percentage = self.employer_contribution_is_percentage
        employer_contribution_top_up_percentage = (
            self.employer_contribution_top_up_percentage
        )
        custom_threshold = self.custom_threshold
        lower_limit = self.lower_limit
        upper_limit = self.upper_limit
        papdis_group = self.papdis_group
        papdis_sub_group = self.papdis_sub_group
        local_authority_number = self.local_authority_number
        school_employer_type = self.school_employer_type
        worker_group_id = self.worker_group_id
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if contribution_level_type is not UNSET:
            field_dict["contributionLevelType"] = contribution_level_type
        if employee_contribution is not UNSET:
            field_dict["employeeContribution"] = employee_contribution
        if employee_contribution_is_percentage is not UNSET:
            field_dict[
                "employeeContributionIsPercentage"
            ] = employee_contribution_is_percentage
        if employer_contribution is not UNSET:
            field_dict["employerContribution"] = employer_contribution
        if employer_contribution_is_percentage is not UNSET:
            field_dict[
                "employerContributionIsPercentage"
            ] = employer_contribution_is_percentage
        if employer_contribution_top_up_percentage is not UNSET:
            field_dict[
                "employerContributionTopUpPercentage"
            ] = employer_contribution_top_up_percentage
        if custom_threshold is not UNSET:
            field_dict["customThreshold"] = custom_threshold
        if lower_limit is not UNSET:
            field_dict["lowerLimit"] = lower_limit
        if upper_limit is not UNSET:
            field_dict["upperLimit"] = upper_limit
        if papdis_group is not UNSET:
            field_dict["papdisGroup"] = papdis_group
        if papdis_sub_group is not UNSET:
            field_dict["papdisSubGroup"] = papdis_sub_group
        if local_authority_number is not UNSET:
            field_dict["localAuthorityNumber"] = local_authority_number
        if school_employer_type is not UNSET:
            field_dict["schoolEmployerType"] = school_employer_type
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _contribution_level_type = d.pop("contributionLevelType", UNSET)
        contribution_level_type: Union[Unset, PensionContributionLevelType]
        if isinstance(_contribution_level_type, Unset):
            contribution_level_type = UNSET
        else:
            contribution_level_type = PensionContributionLevelType(
                _contribution_level_type
            )

        employee_contribution = d.pop("employeeContribution", UNSET)

        employee_contribution_is_percentage = d.pop(
            "employeeContributionIsPercentage", UNSET
        )

        employer_contribution = d.pop("employerContribution", UNSET)

        employer_contribution_is_percentage = d.pop(
            "employerContributionIsPercentage", UNSET
        )

        employer_contribution_top_up_percentage = d.pop(
            "employerContributionTopUpPercentage", UNSET
        )

        custom_threshold = d.pop("customThreshold", UNSET)

        lower_limit = d.pop("lowerLimit", UNSET)

        upper_limit = d.pop("upperLimit", UNSET)

        papdis_group = d.pop("papdisGroup", UNSET)

        papdis_sub_group = d.pop("papdisSubGroup", UNSET)

        local_authority_number = d.pop("localAuthorityNumber", UNSET)

        school_employer_type = d.pop("schoolEmployerType", UNSET)

        worker_group_id = d.pop("workerGroupId", UNSET)

        id = d.pop("id", UNSET)

        worker_group = cls(
            name=name,
            contribution_level_type=contribution_level_type,
            employee_contribution=employee_contribution,
            employee_contribution_is_percentage=employee_contribution_is_percentage,
            employer_contribution=employer_contribution,
            employer_contribution_is_percentage=employer_contribution_is_percentage,
            employer_contribution_top_up_percentage=employer_contribution_top_up_percentage,
            custom_threshold=custom_threshold,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            papdis_group=papdis_group,
            papdis_sub_group=papdis_sub_group,
            local_authority_number=local_authority_number,
            school_employer_type=school_employer_type,
            worker_group_id=worker_group_id,
            id=id,
        )

        return worker_group
