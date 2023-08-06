from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.p11d_car import P11DCar
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DCarCollection")


@attr.s(auto_attribs=True)
class P11DCarCollection:
    """
    Attributes:
        car (Union[Unset, None, List[P11DCar]]):
        total_cars_or_relevant_amt (Union[Unset, None, str]):
        total_fuel_or_relevant_amt (Union[Unset, None, str]):
        type_letter (Union[Unset, None, str]):
    """

    car: Union[Unset, None, List[P11DCar]] = UNSET
    total_cars_or_relevant_amt: Union[Unset, None, str] = UNSET
    total_fuel_or_relevant_amt: Union[Unset, None, str] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        car: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.car, Unset):
            if self.car is None:
                car = None
            else:
                car = []
                for car_item_data in self.car:
                    car_item = car_item_data.to_dict()

                    car.append(car_item)

        total_cars_or_relevant_amt = self.total_cars_or_relevant_amt
        total_fuel_or_relevant_amt = self.total_fuel_or_relevant_amt
        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if car is not UNSET:
            field_dict["car"] = car
        if total_cars_or_relevant_amt is not UNSET:
            field_dict["totalCarsOrRelevantAmt"] = total_cars_or_relevant_amt
        if total_fuel_or_relevant_amt is not UNSET:
            field_dict["totalFuelOrRelevantAmt"] = total_fuel_or_relevant_amt
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        car = []
        _car = d.pop("car", UNSET)
        for car_item_data in _car or []:
            car_item = P11DCar.from_dict(car_item_data)

            car.append(car_item)

        total_cars_or_relevant_amt = d.pop("totalCarsOrRelevantAmt", UNSET)

        total_fuel_or_relevant_amt = d.pop("totalFuelOrRelevantAmt", UNSET)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_car_collection = cls(
            car=car,
            total_cars_or_relevant_amt=total_cars_or_relevant_amt,
            total_fuel_or_relevant_amt=total_fuel_or_relevant_amt,
            type_letter=type_letter,
        )

        return p11d_car_collection
