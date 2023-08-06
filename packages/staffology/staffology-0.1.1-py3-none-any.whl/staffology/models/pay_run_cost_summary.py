from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cost_breakdown import CostBreakdown
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunCostSummary")


@attr.s(auto_attribs=True)
class PayRunCostSummary:
    """Represents the various components that make up the costs of a PayRun

    Attributes:
        tax (Union[Unset, CostBreakdown]): Represents the breakdown of a PayRun cost.
            The Value if calculated using the breakdown of the cost.
        national_insurance (Union[Unset, CostBreakdown]): Represents the breakdown of a PayRun cost.
            The Value if calculated using the breakdown of the cost.
    """

    tax: Union[Unset, CostBreakdown] = UNSET
    national_insurance: Union[Unset, CostBreakdown] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tax, Unset):
            tax = self.tax.to_dict()

        national_insurance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.national_insurance, Unset):
            national_insurance = self.national_insurance.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax is not UNSET:
            field_dict["tax"] = tax
        if national_insurance is not UNSET:
            field_dict["nationalInsurance"] = national_insurance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tax = d.pop("tax", UNSET)
        tax: Union[Unset, CostBreakdown]
        if isinstance(_tax, Unset):
            tax = UNSET
        else:
            tax = CostBreakdown.from_dict(_tax)

        _national_insurance = d.pop("nationalInsurance", UNSET)
        national_insurance: Union[Unset, CostBreakdown]
        if isinstance(_national_insurance, Unset):
            national_insurance = UNSET
        else:
            national_insurance = CostBreakdown.from_dict(_national_insurance)

        pay_run_cost_summary = cls(
            tax=tax,
            national_insurance=national_insurance,
        )

        return pay_run_cost_summary
