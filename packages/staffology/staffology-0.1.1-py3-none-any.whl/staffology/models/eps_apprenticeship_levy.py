from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EpsApprenticeshipLevy")


@attr.s(auto_attribs=True)
class EpsApprenticeshipLevy:
    """Used on an EPS to declare an Apprenticeship Levy amount

    Attributes:
        tax_month (Union[Unset, int]):
        levy_due_ytd (Union[Unset, float]):
        annual_allce (Union[Unset, float]):
    """

    tax_month: Union[Unset, int] = UNSET
    levy_due_ytd: Union[Unset, float] = UNSET
    annual_allce: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_month = self.tax_month
        levy_due_ytd = self.levy_due_ytd
        annual_allce = self.annual_allce

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_month is not UNSET:
            field_dict["taxMonth"] = tax_month
        if levy_due_ytd is not UNSET:
            field_dict["levyDueYTD"] = levy_due_ytd
        if annual_allce is not UNSET:
            field_dict["annualAllce"] = annual_allce

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tax_month = d.pop("taxMonth", UNSET)

        levy_due_ytd = d.pop("levyDueYTD", UNSET)

        annual_allce = d.pop("annualAllce", UNSET)

        eps_apprenticeship_levy = cls(
            tax_month=tax_month,
            levy_due_ytd=levy_due_ytd,
            annual_allce=annual_allce,
        )

        return eps_apprenticeship_levy
