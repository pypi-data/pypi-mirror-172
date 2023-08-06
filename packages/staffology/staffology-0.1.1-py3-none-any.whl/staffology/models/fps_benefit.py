from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.fps_car import FpsCar
from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsBenefit")


@attr.s(auto_attribs=True)
class FpsBenefit:
    """
    Attributes:
        car (Union[Unset, None, List[FpsCar]]):
    """

    car: Union[Unset, None, List[FpsCar]] = UNSET

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

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if car is not UNSET:
            field_dict["car"] = car

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        car = []
        _car = d.pop("car", UNSET)
        for car_item_data in _car or []:
            car_item = FpsCar.from_dict(car_item_data)

            car.append(car_item)

        fps_benefit = cls(
            car=car,
        )

        return fps_benefit
