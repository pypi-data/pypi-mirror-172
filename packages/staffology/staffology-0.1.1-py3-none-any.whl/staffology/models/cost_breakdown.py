from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cost_breakdown_breakdown import CostBreakdownBreakdown
from ..types import UNSET, Unset

T = TypeVar("T", bound="CostBreakdown")


@attr.s(auto_attribs=True)
class CostBreakdown:
    """Represents the breakdown of a PayRun cost.
    The Value if calculated using the breakdown of the cost.

        Attributes:
            value (Union[Unset, float]): The value of cost
            breakdown (Union[Unset, None, CostBreakdownBreakdown]): Breakdown of the cost
    """

    value: Union[Unset, float] = UNSET
    breakdown: Union[Unset, None, CostBreakdownBreakdown] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        breakdown: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.breakdown, Unset):
            breakdown = self.breakdown.to_dict() if self.breakdown else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if breakdown is not UNSET:
            field_dict["breakdown"] = breakdown

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        _breakdown = d.pop("breakdown", UNSET)
        breakdown: Union[Unset, None, CostBreakdownBreakdown]
        if _breakdown is None:
            breakdown = None
        elif isinstance(_breakdown, Unset):
            breakdown = UNSET
        else:
            breakdown = CostBreakdownBreakdown.from_dict(_breakdown)

        cost_breakdown = cls(
            value=value,
            breakdown=breakdown,
        )

        return cost_breakdown
