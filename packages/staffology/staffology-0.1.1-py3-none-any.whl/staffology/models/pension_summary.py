import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.pension_rule import PensionRule
from ..models.tiered_pension_rate import TieredPensionRate
from ..models.worker_group import WorkerGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionSummary")


@attr.s(auto_attribs=True)
class PensionSummary:
    """If a PayRunEntry contains pension contributions then it'll also include a PensionSummary model
    giving further information about the Pension Scheme and the contributions made

        Attributes:
            pension_id (Union[Unset, str]): [readonly] The Id of the Pension.
            name (Union[Unset, None, str]): [readonly] The name of the PensionScheme to which contributions have been made.
            pension_scheme_id (Union[Unset, str]): [readonly] The Id of the PensionScheme.
            start_date (Union[Unset, datetime.date]): [readonly]
            worker_group_id (Union[Unset, str]): [readonly] The Id of the WorkerGroup.
            pension_rule (Union[Unset, PensionRule]):
            papdis_pension_provider_id (Union[Unset, None, str]): [readonly] Papdis information from the PensionScheme
            papdis_employer_id (Union[Unset, None, str]): [readonly] Papdis information from the PensionScheme
            employee_pension_contribution_multiplier (Union[Unset, float]): [readonly] If the PensionScheme is set to
                SubtractBasicRateTax then this value  is used to reduce the contribution amount.
                Otherwise it is set as 1.
            additional_voluntary_contribution (Union[Unset, float]): [readonly] Any Additional Voluntary Contribution the
                Employee has chosen to make
                Otherwise it is set as 1.
            avc_is_percentage (Union[Unset, bool]): [readonly] Determines whether the Value of the Additional Voluntary
                Contribution is a fixed amount or a percentage,
            auto_enrolled (Union[Unset, bool]): [readonly] Any Additional Voluntary Contribution the Employee has chosen to
                make
                Otherwise it is set as 1.
            worker_group (Union[Unset, WorkerGroup]):
            forced_tier (Union[Unset, None, str]): [readonly] If the WorkerGroup ContributionLevelType is a Tiered Scheme
                then the name of the tier to force the employee on to may be specified.
                If none is specified then the Tier is determined by the earnings in the period
            tiers (Union[Unset, None, List[TieredPensionRate]]):
            assumed_pensionable_pay (Union[Unset, None, float]): [readonly] Assumed Pensionable Pay. If the employee is
                receiving any Statutory Leave that has an AssumedPensionablePay value set
                then it'll be shown here.
            pensionable_pay_codes (Union[Unset, None, List[str]]): [readonly] If the pension scheme is set to override the
                Pensionale PayCodes, then this is what they've been set to.
    """

    pension_id: Union[Unset, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    pension_scheme_id: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    pension_rule: Union[Unset, PensionRule] = UNSET
    papdis_pension_provider_id: Union[Unset, None, str] = UNSET
    papdis_employer_id: Union[Unset, None, str] = UNSET
    employee_pension_contribution_multiplier: Union[Unset, float] = UNSET
    additional_voluntary_contribution: Union[Unset, float] = UNSET
    avc_is_percentage: Union[Unset, bool] = UNSET
    auto_enrolled: Union[Unset, bool] = UNSET
    worker_group: Union[Unset, WorkerGroup] = UNSET
    forced_tier: Union[Unset, None, str] = UNSET
    tiers: Union[Unset, None, List[TieredPensionRate]] = UNSET
    assumed_pensionable_pay: Union[Unset, None, float] = UNSET
    pensionable_pay_codes: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pension_id = self.pension_id
        name = self.name
        pension_scheme_id = self.pension_scheme_id
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        worker_group_id = self.worker_group_id
        pension_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pension_rule, Unset):
            pension_rule = self.pension_rule.value

        papdis_pension_provider_id = self.papdis_pension_provider_id
        papdis_employer_id = self.papdis_employer_id
        employee_pension_contribution_multiplier = (
            self.employee_pension_contribution_multiplier
        )
        additional_voluntary_contribution = self.additional_voluntary_contribution
        avc_is_percentage = self.avc_is_percentage
        auto_enrolled = self.auto_enrolled
        worker_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.worker_group, Unset):
            worker_group = self.worker_group.to_dict()

        forced_tier = self.forced_tier
        tiers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tiers, Unset):
            if self.tiers is None:
                tiers = None
            else:
                tiers = []
                for tiers_item_data in self.tiers:
                    tiers_item = tiers_item_data.to_dict()

                    tiers.append(tiers_item)

        assumed_pensionable_pay = self.assumed_pensionable_pay
        pensionable_pay_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.pensionable_pay_codes, Unset):
            if self.pensionable_pay_codes is None:
                pensionable_pay_codes = None
            else:
                pensionable_pay_codes = self.pensionable_pay_codes

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pension_id is not UNSET:
            field_dict["pensionId"] = pension_id
        if name is not UNSET:
            field_dict["name"] = name
        if pension_scheme_id is not UNSET:
            field_dict["pensionSchemeId"] = pension_scheme_id
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if pension_rule is not UNSET:
            field_dict["pensionRule"] = pension_rule
        if papdis_pension_provider_id is not UNSET:
            field_dict["papdisPensionProviderId"] = papdis_pension_provider_id
        if papdis_employer_id is not UNSET:
            field_dict["papdisEmployerId"] = papdis_employer_id
        if employee_pension_contribution_multiplier is not UNSET:
            field_dict[
                "employeePensionContributionMultiplier"
            ] = employee_pension_contribution_multiplier
        if additional_voluntary_contribution is not UNSET:
            field_dict[
                "additionalVoluntaryContribution"
            ] = additional_voluntary_contribution
        if avc_is_percentage is not UNSET:
            field_dict["avcIsPercentage"] = avc_is_percentage
        if auto_enrolled is not UNSET:
            field_dict["autoEnrolled"] = auto_enrolled
        if worker_group is not UNSET:
            field_dict["workerGroup"] = worker_group
        if forced_tier is not UNSET:
            field_dict["forcedTier"] = forced_tier
        if tiers is not UNSET:
            field_dict["tiers"] = tiers
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if pensionable_pay_codes is not UNSET:
            field_dict["pensionablePayCodes"] = pensionable_pay_codes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pension_id = d.pop("pensionId", UNSET)

        name = d.pop("name", UNSET)

        pension_scheme_id = d.pop("pensionSchemeId", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        worker_group_id = d.pop("workerGroupId", UNSET)

        _pension_rule = d.pop("pensionRule", UNSET)
        pension_rule: Union[Unset, PensionRule]
        if isinstance(_pension_rule, Unset):
            pension_rule = UNSET
        else:
            pension_rule = PensionRule(_pension_rule)

        papdis_pension_provider_id = d.pop("papdisPensionProviderId", UNSET)

        papdis_employer_id = d.pop("papdisEmployerId", UNSET)

        employee_pension_contribution_multiplier = d.pop(
            "employeePensionContributionMultiplier", UNSET
        )

        additional_voluntary_contribution = d.pop(
            "additionalVoluntaryContribution", UNSET
        )

        avc_is_percentage = d.pop("avcIsPercentage", UNSET)

        auto_enrolled = d.pop("autoEnrolled", UNSET)

        _worker_group = d.pop("workerGroup", UNSET)
        worker_group: Union[Unset, WorkerGroup]
        if isinstance(_worker_group, Unset):
            worker_group = UNSET
        else:
            worker_group = WorkerGroup.from_dict(_worker_group)

        forced_tier = d.pop("forcedTier", UNSET)

        tiers = []
        _tiers = d.pop("tiers", UNSET)
        for tiers_item_data in _tiers or []:
            tiers_item = TieredPensionRate.from_dict(tiers_item_data)

            tiers.append(tiers_item)

        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        pensionable_pay_codes = cast(List[str], d.pop("pensionablePayCodes", UNSET))

        pension_summary = cls(
            pension_id=pension_id,
            name=name,
            pension_scheme_id=pension_scheme_id,
            start_date=start_date,
            worker_group_id=worker_group_id,
            pension_rule=pension_rule,
            papdis_pension_provider_id=papdis_pension_provider_id,
            papdis_employer_id=papdis_employer_id,
            employee_pension_contribution_multiplier=employee_pension_contribution_multiplier,
            additional_voluntary_contribution=additional_voluntary_contribution,
            avc_is_percentage=avc_is_percentage,
            auto_enrolled=auto_enrolled,
            worker_group=worker_group,
            forced_tier=forced_tier,
            tiers=tiers,
            assumed_pensionable_pay=assumed_pensionable_pay,
            pensionable_pay_codes=pensionable_pay_codes,
        )

        return pension_summary
