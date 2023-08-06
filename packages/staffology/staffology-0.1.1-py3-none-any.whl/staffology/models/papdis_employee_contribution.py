from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeContribution")


@attr.s(auto_attribs=True)
class PapdisEmployeeContribution:
    """
    Attributes:
        employer_contributions_amount (Union[Unset, float]): [readonly]
        employer_contributions_percent (Union[Unset, float]): [readonly]
        employee_contributions_amount (Union[Unset, float]): [readonly]
        employee_contributions_percent (Union[Unset, float]): [readonly]
        additional_voluntary_contributions_amount (Union[Unset, float]): [readonly]
        additional_voluntary_contributions_percent (Union[Unset, float]): [readonly]
        salary_sacrifice_indicator (Union[Unset, bool]): [readonly]
    """

    employer_contributions_amount: Union[Unset, float] = UNSET
    employer_contributions_percent: Union[Unset, float] = UNSET
    employee_contributions_amount: Union[Unset, float] = UNSET
    employee_contributions_percent: Union[Unset, float] = UNSET
    additional_voluntary_contributions_amount: Union[Unset, float] = UNSET
    additional_voluntary_contributions_percent: Union[Unset, float] = UNSET
    salary_sacrifice_indicator: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer_contributions_amount = self.employer_contributions_amount
        employer_contributions_percent = self.employer_contributions_percent
        employee_contributions_amount = self.employee_contributions_amount
        employee_contributions_percent = self.employee_contributions_percent
        additional_voluntary_contributions_amount = (
            self.additional_voluntary_contributions_amount
        )
        additional_voluntary_contributions_percent = (
            self.additional_voluntary_contributions_percent
        )
        salary_sacrifice_indicator = self.salary_sacrifice_indicator

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer_contributions_amount is not UNSET:
            field_dict["employerContributionsAmount"] = employer_contributions_amount
        if employer_contributions_percent is not UNSET:
            field_dict["employerContributionsPercent"] = employer_contributions_percent
        if employee_contributions_amount is not UNSET:
            field_dict["employeeContributionsAmount"] = employee_contributions_amount
        if employee_contributions_percent is not UNSET:
            field_dict["employeeContributionsPercent"] = employee_contributions_percent
        if additional_voluntary_contributions_amount is not UNSET:
            field_dict[
                "additionalVoluntaryContributionsAmount"
            ] = additional_voluntary_contributions_amount
        if additional_voluntary_contributions_percent is not UNSET:
            field_dict[
                "additionalVoluntaryContributionsPercent"
            ] = additional_voluntary_contributions_percent
        if salary_sacrifice_indicator is not UNSET:
            field_dict["salarySacrificeIndicator"] = salary_sacrifice_indicator

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_contributions_amount = d.pop("employerContributionsAmount", UNSET)

        employer_contributions_percent = d.pop("employerContributionsPercent", UNSET)

        employee_contributions_amount = d.pop("employeeContributionsAmount", UNSET)

        employee_contributions_percent = d.pop("employeeContributionsPercent", UNSET)

        additional_voluntary_contributions_amount = d.pop(
            "additionalVoluntaryContributionsAmount", UNSET
        )

        additional_voluntary_contributions_percent = d.pop(
            "additionalVoluntaryContributionsPercent", UNSET
        )

        salary_sacrifice_indicator = d.pop("salarySacrificeIndicator", UNSET)

        papdis_employee_contribution = cls(
            employer_contributions_amount=employer_contributions_amount,
            employer_contributions_percent=employer_contributions_percent,
            employee_contributions_amount=employee_contributions_amount,
            employee_contributions_percent=employee_contributions_percent,
            additional_voluntary_contributions_amount=additional_voluntary_contributions_amount,
            additional_voluntary_contributions_percent=additional_voluntary_contributions_percent,
            salary_sacrifice_indicator=salary_sacrifice_indicator,
        )

        return papdis_employee_contribution
