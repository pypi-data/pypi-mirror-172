from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fps_car_fuel import FpsCarFuel
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsCar")


@attr.s(auto_attribs=True)
class FpsCar:
    """
    Attributes:
        make (Union[Unset, None, str]):
        first_regd (Union[Unset, None, str]):
        c_o2 (Union[Unset, None, str]):
        zero_emissions_mileage (Union[Unset, None, str]):
        fuel (Union[Unset, None, str]):
        id (Union[Unset, None, str]):
        amendment (Union[Unset, None, str]):
        price (Union[Unset, None, str]):
        avail_from (Union[Unset, None, str]):
        cash_equiv (Union[Unset, None, str]):
        avail_to (Union[Unset, None, str]):
        free_fuel (Union[Unset, FpsCarFuel]):
    """

    make: Union[Unset, None, str] = UNSET
    first_regd: Union[Unset, None, str] = UNSET
    c_o2: Union[Unset, None, str] = UNSET
    zero_emissions_mileage: Union[Unset, None, str] = UNSET
    fuel: Union[Unset, None, str] = UNSET
    id: Union[Unset, None, str] = UNSET
    amendment: Union[Unset, None, str] = UNSET
    price: Union[Unset, None, str] = UNSET
    avail_from: Union[Unset, None, str] = UNSET
    cash_equiv: Union[Unset, None, str] = UNSET
    avail_to: Union[Unset, None, str] = UNSET
    free_fuel: Union[Unset, FpsCarFuel] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        make = self.make
        first_regd = self.first_regd
        c_o2 = self.c_o2
        zero_emissions_mileage = self.zero_emissions_mileage
        fuel = self.fuel
        id = self.id
        amendment = self.amendment
        price = self.price
        avail_from = self.avail_from
        cash_equiv = self.cash_equiv
        avail_to = self.avail_to
        free_fuel: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.free_fuel, Unset):
            free_fuel = self.free_fuel.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if make is not UNSET:
            field_dict["make"] = make
        if first_regd is not UNSET:
            field_dict["firstRegd"] = first_regd
        if c_o2 is not UNSET:
            field_dict["cO2"] = c_o2
        if zero_emissions_mileage is not UNSET:
            field_dict["zeroEmissionsMileage"] = zero_emissions_mileage
        if fuel is not UNSET:
            field_dict["fuel"] = fuel
        if id is not UNSET:
            field_dict["id"] = id
        if amendment is not UNSET:
            field_dict["amendment"] = amendment
        if price is not UNSET:
            field_dict["price"] = price
        if avail_from is not UNSET:
            field_dict["availFrom"] = avail_from
        if cash_equiv is not UNSET:
            field_dict["cashEquiv"] = cash_equiv
        if avail_to is not UNSET:
            field_dict["availTo"] = avail_to
        if free_fuel is not UNSET:
            field_dict["freeFuel"] = free_fuel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        make = d.pop("make", UNSET)

        first_regd = d.pop("firstRegd", UNSET)

        c_o2 = d.pop("cO2", UNSET)

        zero_emissions_mileage = d.pop("zeroEmissionsMileage", UNSET)

        fuel = d.pop("fuel", UNSET)

        id = d.pop("id", UNSET)

        amendment = d.pop("amendment", UNSET)

        price = d.pop("price", UNSET)

        avail_from = d.pop("availFrom", UNSET)

        cash_equiv = d.pop("cashEquiv", UNSET)

        avail_to = d.pop("availTo", UNSET)

        _free_fuel = d.pop("freeFuel", UNSET)
        free_fuel: Union[Unset, FpsCarFuel]
        if isinstance(_free_fuel, Unset):
            free_fuel = UNSET
        else:
            free_fuel = FpsCarFuel.from_dict(_free_fuel)

        fps_car = cls(
            make=make,
            first_regd=first_regd,
            c_o2=c_o2,
            zero_emissions_mileage=zero_emissions_mileage,
            fuel=fuel,
            id=id,
            amendment=amendment,
            price=price,
            avail_from=avail_from,
            cash_equiv=cash_equiv,
            avail_to=avail_to,
            free_fuel=free_fuel,
        )

        return fps_car
