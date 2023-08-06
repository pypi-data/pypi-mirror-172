from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.mileage_vehicle_type import MileageVehicleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MileageAllowancePaymentsRate")


@attr.s(auto_attribs=True)
class MileageAllowancePaymentsRate:
    """Part of the TaxYearConfig that our engine uses to calculate Mileage Allowance Payments.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            vehicle_type (Union[Unset, MileageVehicleType]):
            rate (Union[Unset, float]):
            threshold (Union[Unset, None, int]):
            above_threshold_rate (Union[Unset, float]):
    """

    vehicle_type: Union[Unset, MileageVehicleType] = UNSET
    rate: Union[Unset, float] = UNSET
    threshold: Union[Unset, None, int] = UNSET
    above_threshold_rate: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        vehicle_type: Union[Unset, str] = UNSET
        if not isinstance(self.vehicle_type, Unset):
            vehicle_type = self.vehicle_type.value

        rate = self.rate
        threshold = self.threshold
        above_threshold_rate = self.above_threshold_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if vehicle_type is not UNSET:
            field_dict["vehicleType"] = vehicle_type
        if rate is not UNSET:
            field_dict["rate"] = rate
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if above_threshold_rate is not UNSET:
            field_dict["aboveThresholdRate"] = above_threshold_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _vehicle_type = d.pop("vehicleType", UNSET)
        vehicle_type: Union[Unset, MileageVehicleType]
        if isinstance(_vehicle_type, Unset):
            vehicle_type = UNSET
        else:
            vehicle_type = MileageVehicleType(_vehicle_type)

        rate = d.pop("rate", UNSET)

        threshold = d.pop("threshold", UNSET)

        above_threshold_rate = d.pop("aboveThresholdRate", UNSET)

        mileage_allowance_payments_rate = cls(
            vehicle_type=vehicle_type,
            rate=rate,
            threshold=threshold,
            above_threshold_rate=above_threshold_rate,
        )

        return mileage_allowance_payments_rate
