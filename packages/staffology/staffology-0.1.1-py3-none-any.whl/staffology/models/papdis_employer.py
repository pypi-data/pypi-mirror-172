import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.papdis_payroll_period import PapdisPayrollPeriod
from ..models.pension_rule import PensionRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployer")


@attr.s(auto_attribs=True)
class PapdisEmployer:
    """
    Attributes:
        pension_rule (Union[Unset, PensionRule]):
        employer_id (Union[Unset, None, str]): [readonly] Taken from the papdisEmployerId property of the
            PensionProvider
        group (Union[Unset, None, str]): [readonly] Taken from the papdisGroup property of the WorkerGroup
        sub_group (Union[Unset, None, str]): [readonly] Taken from the papdisSubGroup property of the WorkerGroup
        payroll_period (Union[Unset, PapdisPayrollPeriod]):
        staging_date (Union[Unset, datetime.date]): [readonly]
        cyclical_reenrolment_date (Union[Unset, None, datetime.date]): [readonly]
    """

    pension_rule: Union[Unset, PensionRule] = UNSET
    employer_id: Union[Unset, None, str] = UNSET
    group: Union[Unset, None, str] = UNSET
    sub_group: Union[Unset, None, str] = UNSET
    payroll_period: Union[Unset, PapdisPayrollPeriod] = UNSET
    staging_date: Union[Unset, datetime.date] = UNSET
    cyclical_reenrolment_date: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pension_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pension_rule, Unset):
            pension_rule = self.pension_rule.value

        employer_id = self.employer_id
        group = self.group
        sub_group = self.sub_group
        payroll_period: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payroll_period, Unset):
            payroll_period = self.payroll_period.to_dict()

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

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pension_rule is not UNSET:
            field_dict["pensionRule"] = pension_rule
        if employer_id is not UNSET:
            field_dict["employerId"] = employer_id
        if group is not UNSET:
            field_dict["group"] = group
        if sub_group is not UNSET:
            field_dict["subGroup"] = sub_group
        if payroll_period is not UNSET:
            field_dict["payrollPeriod"] = payroll_period
        if staging_date is not UNSET:
            field_dict["stagingDate"] = staging_date
        if cyclical_reenrolment_date is not UNSET:
            field_dict["cyclicalReenrolmentDate"] = cyclical_reenrolment_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _pension_rule = d.pop("pensionRule", UNSET)
        pension_rule: Union[Unset, PensionRule]
        if isinstance(_pension_rule, Unset):
            pension_rule = UNSET
        else:
            pension_rule = PensionRule(_pension_rule)

        employer_id = d.pop("employerId", UNSET)

        group = d.pop("group", UNSET)

        sub_group = d.pop("subGroup", UNSET)

        _payroll_period = d.pop("payrollPeriod", UNSET)
        payroll_period: Union[Unset, PapdisPayrollPeriod]
        if isinstance(_payroll_period, Unset):
            payroll_period = UNSET
        else:
            payroll_period = PapdisPayrollPeriod.from_dict(_payroll_period)

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

        papdis_employer = cls(
            pension_rule=pension_rule,
            employer_id=employer_id,
            group=group,
            sub_group=sub_group,
            payroll_period=payroll_period,
            staging_date=staging_date,
            cyclical_reenrolment_date=cyclical_reenrolment_date,
        )

        return papdis_employer
