from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsCarFuel")


@attr.s(auto_attribs=True)
class FpsCarFuel:
    """
    Attributes:
        provided (Union[Unset, None, str]):
        cash_equiv (Union[Unset, None, str]):
        withdrawn (Union[Unset, None, str]):
    """

    provided: Union[Unset, None, str] = UNSET
    cash_equiv: Union[Unset, None, str] = UNSET
    withdrawn: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        provided = self.provided
        cash_equiv = self.cash_equiv
        withdrawn = self.withdrawn

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if provided is not UNSET:
            field_dict["provided"] = provided
        if cash_equiv is not UNSET:
            field_dict["cashEquiv"] = cash_equiv
        if withdrawn is not UNSET:
            field_dict["withdrawn"] = withdrawn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provided = d.pop("provided", UNSET)

        cash_equiv = d.pop("cashEquiv", UNSET)

        withdrawn = d.pop("withdrawn", UNSET)

        fps_car_fuel = cls(
            provided=provided,
            cash_equiv=cash_equiv,
            withdrawn=withdrawn,
        )

        return fps_car_fuel
