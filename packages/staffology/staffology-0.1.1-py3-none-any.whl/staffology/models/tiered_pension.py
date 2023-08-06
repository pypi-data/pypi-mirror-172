from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pension_contribution_level_type import PensionContributionLevelType
from ..models.tiered_pension_rate import TieredPensionRate
from ..types import UNSET, Unset

T = TypeVar("T", bound="TieredPension")


@attr.s(auto_attribs=True)
class TieredPension:
    """Part of the TaxYearConfig that our engine uses to calculate tiered pension contributions.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            type (Union[Unset, PensionContributionLevelType]):
            rates (Union[Unset, None, List[TieredPensionRate]]):
            employer_contrib_rate (Union[Unset, float]):
    """

    type: Union[Unset, PensionContributionLevelType] = UNSET
    rates: Union[Unset, None, List[TieredPensionRate]] = UNSET
    employer_contrib_rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        rates: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.rates, Unset):
            if self.rates is None:
                rates = None
            else:
                rates = []
                for rates_item_data in self.rates:
                    rates_item = rates_item_data.to_dict()

                    rates.append(rates_item)

        employer_contrib_rate = self.employer_contrib_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if rates is not UNSET:
            field_dict["rates"] = rates
        if employer_contrib_rate is not UNSET:
            field_dict["employerContribRate"] = employer_contrib_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PensionContributionLevelType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PensionContributionLevelType(_type)

        rates = []
        _rates = d.pop("rates", UNSET)
        for rates_item_data in _rates or []:
            rates_item = TieredPensionRate.from_dict(rates_item_data)

            rates.append(rates_item)

        employer_contrib_rate = d.pop("employerContribRate", UNSET)

        tiered_pension = cls(
            type=type,
            rates=rates,
            employer_contrib_rate=employer_contrib_rate,
        )

        return tiered_pension
