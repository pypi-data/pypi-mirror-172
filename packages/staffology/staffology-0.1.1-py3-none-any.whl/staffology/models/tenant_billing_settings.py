from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantBillingSettings")


@attr.s(auto_attribs=True)
class TenantBillingSettings:
    """
    Attributes:
        discount (Union[Unset, float]):
        monthly_minimum (Union[Unset, float]):
        aggregated_pricing (Union[Unset, bool]):
        bill_to (Union[Unset, None, str]): If all activity for a Tenant is being biulled to a specifc user, set the
            email address here
    """

    discount: Union[Unset, float] = UNSET
    monthly_minimum: Union[Unset, float] = UNSET
    aggregated_pricing: Union[Unset, bool] = UNSET
    bill_to: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        discount = self.discount
        monthly_minimum = self.monthly_minimum
        aggregated_pricing = self.aggregated_pricing
        bill_to = self.bill_to

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if discount is not UNSET:
            field_dict["discount"] = discount
        if monthly_minimum is not UNSET:
            field_dict["monthlyMinimum"] = monthly_minimum
        if aggregated_pricing is not UNSET:
            field_dict["aggregatedPricing"] = aggregated_pricing
        if bill_to is not UNSET:
            field_dict["billTo"] = bill_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        discount = d.pop("discount", UNSET)

        monthly_minimum = d.pop("monthlyMinimum", UNSET)

        aggregated_pricing = d.pop("aggregatedPricing", UNSET)

        bill_to = d.pop("billTo", UNSET)

        tenant_billing_settings = cls(
            discount=discount,
            monthly_minimum=monthly_minimum,
            aggregated_pricing=aggregated_pricing,
            bill_to=bill_to,
        )

        return tenant_billing_settings
