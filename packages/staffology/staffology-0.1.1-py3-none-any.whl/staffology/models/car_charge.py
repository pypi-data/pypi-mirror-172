import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.car_charge_rate import CarChargeRate
from ..types import UNSET, Unset

T = TypeVar("T", bound="CarCharge")


@attr.s(auto_attribs=True)
class CarCharge:
    """Part of the TaxYearConfig that our engine uses to calculate charges for a Company Car.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            diesel_surcharge (Union[Unset, float]):
            max_charge (Union[Unset, float]):
            min_charge (Union[Unset, float]):
            fuel_charge (Union[Unset, float]):
            new_car_rate_reduction_date (Union[Unset, None, datetime.date]):
            new_car_rate_reduction_amount (Union[Unset, float]):
            co_2_table (Union[Unset, None, List[CarChargeRate]]):
            engine_size_table (Union[Unset, None, List[CarChargeRate]]):
            zero_emissions_table (Union[Unset, None, List[CarChargeRate]]):
    """

    diesel_surcharge: Union[Unset, float] = UNSET
    max_charge: Union[Unset, float] = UNSET
    min_charge: Union[Unset, float] = UNSET
    fuel_charge: Union[Unset, float] = UNSET
    new_car_rate_reduction_date: Union[Unset, None, datetime.date] = UNSET
    new_car_rate_reduction_amount: Union[Unset, float] = UNSET
    co_2_table: Union[Unset, None, List[CarChargeRate]] = UNSET
    engine_size_table: Union[Unset, None, List[CarChargeRate]] = UNSET
    zero_emissions_table: Union[Unset, None, List[CarChargeRate]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        diesel_surcharge = self.diesel_surcharge
        max_charge = self.max_charge
        min_charge = self.min_charge
        fuel_charge = self.fuel_charge
        new_car_rate_reduction_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.new_car_rate_reduction_date, Unset):
            new_car_rate_reduction_date = (
                self.new_car_rate_reduction_date.isoformat()
                if self.new_car_rate_reduction_date
                else None
            )

        new_car_rate_reduction_amount = self.new_car_rate_reduction_amount
        co_2_table: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.co_2_table, Unset):
            if self.co_2_table is None:
                co_2_table = None
            else:
                co_2_table = []
                for co_2_table_item_data in self.co_2_table:
                    co_2_table_item = co_2_table_item_data.to_dict()

                    co_2_table.append(co_2_table_item)

        engine_size_table: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.engine_size_table, Unset):
            if self.engine_size_table is None:
                engine_size_table = None
            else:
                engine_size_table = []
                for engine_size_table_item_data in self.engine_size_table:
                    engine_size_table_item = engine_size_table_item_data.to_dict()

                    engine_size_table.append(engine_size_table_item)

        zero_emissions_table: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.zero_emissions_table, Unset):
            if self.zero_emissions_table is None:
                zero_emissions_table = None
            else:
                zero_emissions_table = []
                for zero_emissions_table_item_data in self.zero_emissions_table:
                    zero_emissions_table_item = zero_emissions_table_item_data.to_dict()

                    zero_emissions_table.append(zero_emissions_table_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if diesel_surcharge is not UNSET:
            field_dict["dieselSurcharge"] = diesel_surcharge
        if max_charge is not UNSET:
            field_dict["maxCharge"] = max_charge
        if min_charge is not UNSET:
            field_dict["minCharge"] = min_charge
        if fuel_charge is not UNSET:
            field_dict["fuelCharge"] = fuel_charge
        if new_car_rate_reduction_date is not UNSET:
            field_dict["newCarRateReductionDate"] = new_car_rate_reduction_date
        if new_car_rate_reduction_amount is not UNSET:
            field_dict["newCarRateReductionAmount"] = new_car_rate_reduction_amount
        if co_2_table is not UNSET:
            field_dict["co2Table"] = co_2_table
        if engine_size_table is not UNSET:
            field_dict["engineSizeTable"] = engine_size_table
        if zero_emissions_table is not UNSET:
            field_dict["zeroEmissionsTable"] = zero_emissions_table

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        diesel_surcharge = d.pop("dieselSurcharge", UNSET)

        max_charge = d.pop("maxCharge", UNSET)

        min_charge = d.pop("minCharge", UNSET)

        fuel_charge = d.pop("fuelCharge", UNSET)

        _new_car_rate_reduction_date = d.pop("newCarRateReductionDate", UNSET)
        new_car_rate_reduction_date: Union[Unset, None, datetime.date]
        if _new_car_rate_reduction_date is None:
            new_car_rate_reduction_date = None
        elif isinstance(_new_car_rate_reduction_date, Unset):
            new_car_rate_reduction_date = UNSET
        else:
            new_car_rate_reduction_date = isoparse(_new_car_rate_reduction_date).date()

        new_car_rate_reduction_amount = d.pop("newCarRateReductionAmount", UNSET)

        co_2_table = []
        _co_2_table = d.pop("co2Table", UNSET)
        for co_2_table_item_data in _co_2_table or []:
            co_2_table_item = CarChargeRate.from_dict(co_2_table_item_data)

            co_2_table.append(co_2_table_item)

        engine_size_table = []
        _engine_size_table = d.pop("engineSizeTable", UNSET)
        for engine_size_table_item_data in _engine_size_table or []:
            engine_size_table_item = CarChargeRate.from_dict(
                engine_size_table_item_data
            )

            engine_size_table.append(engine_size_table_item)

        zero_emissions_table = []
        _zero_emissions_table = d.pop("zeroEmissionsTable", UNSET)
        for zero_emissions_table_item_data in _zero_emissions_table or []:
            zero_emissions_table_item = CarChargeRate.from_dict(
                zero_emissions_table_item_data
            )

            zero_emissions_table.append(zero_emissions_table_item)

        car_charge = cls(
            diesel_surcharge=diesel_surcharge,
            max_charge=max_charge,
            min_charge=min_charge,
            fuel_charge=fuel_charge,
            new_car_rate_reduction_date=new_car_rate_reduction_date,
            new_car_rate_reduction_amount=new_car_rate_reduction_amount,
            co_2_table=co_2_table,
            engine_size_table=engine_size_table,
            zero_emissions_table=zero_emissions_table,
        )

        return car_charge
