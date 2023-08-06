import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.benefit_details_car_power_type import BenefitDetailsCarPowerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenefitDetailsCar")


@attr.s(auto_attribs=True)
class BenefitDetailsCar:
    """
    Attributes:
        make_and_model (Union[Unset, None, str]):
        registration (Union[Unset, None, str]):
        first_registered (Union[Unset, None, datetime.date]):
        has_approved_emissions_value (Union[Unset, bool]):
        co_2_emissions (Union[Unset, int]):
        engine_size (Union[Unset, int]):
        zero_emissions_mileage (Union[Unset, int]):
        fuel_type (Union[Unset, BenefitDetailsCarPowerType]):
        available_from (Union[Unset, None, datetime.date]):
        available_to (Union[Unset, None, datetime.date]):
        days_unavailable (Union[Unset, int]):
        list_price (Union[Unset, float]):
        non_standard_accessories (Union[Unset, float]):
        employee_capital_contributions (Union[Unset, float]):
        employee_private_contributions (Union[Unset, float]):
        free_fuel (Union[Unset, bool]):
        fuel_available_from (Union[Unset, None, datetime.date]):
        fuel_available_to (Union[Unset, None, datetime.date]):
        free_fuel_reinstated (Union[Unset, bool]):
        registered_prior_to_1998 (Union[Unset, bool]): [readonly]
        rate (Union[Unset, float]): [readonly] The applicable rate based on CO2Emissions and Engine Size
        chargeable_value (Union[Unset, float]): [readonly] The chargeable value of the car
        full_year_charge (Union[Unset, float]): [readonly] The charge for the car for a full year, not taking in to
            account available dates or EmployeePrivateContributions
        cash_equivalent (Union[Unset, float]): [readonly]
        cash_equivalent_fuel (Union[Unset, float]): [readonly]
    """

    make_and_model: Union[Unset, None, str] = UNSET
    registration: Union[Unset, None, str] = UNSET
    first_registered: Union[Unset, None, datetime.date] = UNSET
    has_approved_emissions_value: Union[Unset, bool] = UNSET
    co_2_emissions: Union[Unset, int] = UNSET
    engine_size: Union[Unset, int] = UNSET
    zero_emissions_mileage: Union[Unset, int] = UNSET
    fuel_type: Union[Unset, BenefitDetailsCarPowerType] = UNSET
    available_from: Union[Unset, None, datetime.date] = UNSET
    available_to: Union[Unset, None, datetime.date] = UNSET
    days_unavailable: Union[Unset, int] = UNSET
    list_price: Union[Unset, float] = UNSET
    non_standard_accessories: Union[Unset, float] = UNSET
    employee_capital_contributions: Union[Unset, float] = UNSET
    employee_private_contributions: Union[Unset, float] = UNSET
    free_fuel: Union[Unset, bool] = UNSET
    fuel_available_from: Union[Unset, None, datetime.date] = UNSET
    fuel_available_to: Union[Unset, None, datetime.date] = UNSET
    free_fuel_reinstated: Union[Unset, bool] = UNSET
    registered_prior_to_1998: Union[Unset, bool] = UNSET
    rate: Union[Unset, float] = UNSET
    chargeable_value: Union[Unset, float] = UNSET
    full_year_charge: Union[Unset, float] = UNSET
    cash_equivalent: Union[Unset, float] = UNSET
    cash_equivalent_fuel: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        make_and_model = self.make_and_model
        registration = self.registration
        first_registered: Union[Unset, None, str] = UNSET
        if not isinstance(self.first_registered, Unset):
            first_registered = (
                self.first_registered.isoformat() if self.first_registered else None
            )

        has_approved_emissions_value = self.has_approved_emissions_value
        co_2_emissions = self.co_2_emissions
        engine_size = self.engine_size
        zero_emissions_mileage = self.zero_emissions_mileage
        fuel_type: Union[Unset, str] = UNSET
        if not isinstance(self.fuel_type, Unset):
            fuel_type = self.fuel_type.value

        available_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.available_from, Unset):
            available_from = (
                self.available_from.isoformat() if self.available_from else None
            )

        available_to: Union[Unset, None, str] = UNSET
        if not isinstance(self.available_to, Unset):
            available_to = self.available_to.isoformat() if self.available_to else None

        days_unavailable = self.days_unavailable
        list_price = self.list_price
        non_standard_accessories = self.non_standard_accessories
        employee_capital_contributions = self.employee_capital_contributions
        employee_private_contributions = self.employee_private_contributions
        free_fuel = self.free_fuel
        fuel_available_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.fuel_available_from, Unset):
            fuel_available_from = (
                self.fuel_available_from.isoformat()
                if self.fuel_available_from
                else None
            )

        fuel_available_to: Union[Unset, None, str] = UNSET
        if not isinstance(self.fuel_available_to, Unset):
            fuel_available_to = (
                self.fuel_available_to.isoformat() if self.fuel_available_to else None
            )

        free_fuel_reinstated = self.free_fuel_reinstated
        registered_prior_to_1998 = self.registered_prior_to_1998
        rate = self.rate
        chargeable_value = self.chargeable_value
        full_year_charge = self.full_year_charge
        cash_equivalent = self.cash_equivalent
        cash_equivalent_fuel = self.cash_equivalent_fuel

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if make_and_model is not UNSET:
            field_dict["makeAndModel"] = make_and_model
        if registration is not UNSET:
            field_dict["registration"] = registration
        if first_registered is not UNSET:
            field_dict["firstRegistered"] = first_registered
        if has_approved_emissions_value is not UNSET:
            field_dict["hasApprovedEmissionsValue"] = has_approved_emissions_value
        if co_2_emissions is not UNSET:
            field_dict["co2Emissions"] = co_2_emissions
        if engine_size is not UNSET:
            field_dict["engineSize"] = engine_size
        if zero_emissions_mileage is not UNSET:
            field_dict["zeroEmissionsMileage"] = zero_emissions_mileage
        if fuel_type is not UNSET:
            field_dict["fuelType"] = fuel_type
        if available_from is not UNSET:
            field_dict["availableFrom"] = available_from
        if available_to is not UNSET:
            field_dict["availableTo"] = available_to
        if days_unavailable is not UNSET:
            field_dict["daysUnavailable"] = days_unavailable
        if list_price is not UNSET:
            field_dict["listPrice"] = list_price
        if non_standard_accessories is not UNSET:
            field_dict["nonStandardAccessories"] = non_standard_accessories
        if employee_capital_contributions is not UNSET:
            field_dict["employeeCapitalContributions"] = employee_capital_contributions
        if employee_private_contributions is not UNSET:
            field_dict["employeePrivateContributions"] = employee_private_contributions
        if free_fuel is not UNSET:
            field_dict["freeFuel"] = free_fuel
        if fuel_available_from is not UNSET:
            field_dict["fuelAvailableFrom"] = fuel_available_from
        if fuel_available_to is not UNSET:
            field_dict["fuelAvailableTo"] = fuel_available_to
        if free_fuel_reinstated is not UNSET:
            field_dict["freeFuelReinstated"] = free_fuel_reinstated
        if registered_prior_to_1998 is not UNSET:
            field_dict["registeredPriorTo1998"] = registered_prior_to_1998
        if rate is not UNSET:
            field_dict["rate"] = rate
        if chargeable_value is not UNSET:
            field_dict["chargeableValue"] = chargeable_value
        if full_year_charge is not UNSET:
            field_dict["fullYearCharge"] = full_year_charge
        if cash_equivalent is not UNSET:
            field_dict["cashEquivalent"] = cash_equivalent
        if cash_equivalent_fuel is not UNSET:
            field_dict["cashEquivalentFuel"] = cash_equivalent_fuel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        make_and_model = d.pop("makeAndModel", UNSET)

        registration = d.pop("registration", UNSET)

        _first_registered = d.pop("firstRegistered", UNSET)
        first_registered: Union[Unset, None, datetime.date]
        if _first_registered is None:
            first_registered = None
        elif isinstance(_first_registered, Unset):
            first_registered = UNSET
        else:
            first_registered = isoparse(_first_registered).date()

        has_approved_emissions_value = d.pop("hasApprovedEmissionsValue", UNSET)

        co_2_emissions = d.pop("co2Emissions", UNSET)

        engine_size = d.pop("engineSize", UNSET)

        zero_emissions_mileage = d.pop("zeroEmissionsMileage", UNSET)

        _fuel_type = d.pop("fuelType", UNSET)
        fuel_type: Union[Unset, BenefitDetailsCarPowerType]
        if isinstance(_fuel_type, Unset):
            fuel_type = UNSET
        else:
            fuel_type = BenefitDetailsCarPowerType(_fuel_type)

        _available_from = d.pop("availableFrom", UNSET)
        available_from: Union[Unset, None, datetime.date]
        if _available_from is None:
            available_from = None
        elif isinstance(_available_from, Unset):
            available_from = UNSET
        else:
            available_from = isoparse(_available_from).date()

        _available_to = d.pop("availableTo", UNSET)
        available_to: Union[Unset, None, datetime.date]
        if _available_to is None:
            available_to = None
        elif isinstance(_available_to, Unset):
            available_to = UNSET
        else:
            available_to = isoparse(_available_to).date()

        days_unavailable = d.pop("daysUnavailable", UNSET)

        list_price = d.pop("listPrice", UNSET)

        non_standard_accessories = d.pop("nonStandardAccessories", UNSET)

        employee_capital_contributions = d.pop("employeeCapitalContributions", UNSET)

        employee_private_contributions = d.pop("employeePrivateContributions", UNSET)

        free_fuel = d.pop("freeFuel", UNSET)

        _fuel_available_from = d.pop("fuelAvailableFrom", UNSET)
        fuel_available_from: Union[Unset, None, datetime.date]
        if _fuel_available_from is None:
            fuel_available_from = None
        elif isinstance(_fuel_available_from, Unset):
            fuel_available_from = UNSET
        else:
            fuel_available_from = isoparse(_fuel_available_from).date()

        _fuel_available_to = d.pop("fuelAvailableTo", UNSET)
        fuel_available_to: Union[Unset, None, datetime.date]
        if _fuel_available_to is None:
            fuel_available_to = None
        elif isinstance(_fuel_available_to, Unset):
            fuel_available_to = UNSET
        else:
            fuel_available_to = isoparse(_fuel_available_to).date()

        free_fuel_reinstated = d.pop("freeFuelReinstated", UNSET)

        registered_prior_to_1998 = d.pop("registeredPriorTo1998", UNSET)

        rate = d.pop("rate", UNSET)

        chargeable_value = d.pop("chargeableValue", UNSET)

        full_year_charge = d.pop("fullYearCharge", UNSET)

        cash_equivalent = d.pop("cashEquivalent", UNSET)

        cash_equivalent_fuel = d.pop("cashEquivalentFuel", UNSET)

        benefit_details_car = cls(
            make_and_model=make_and_model,
            registration=registration,
            first_registered=first_registered,
            has_approved_emissions_value=has_approved_emissions_value,
            co_2_emissions=co_2_emissions,
            engine_size=engine_size,
            zero_emissions_mileage=zero_emissions_mileage,
            fuel_type=fuel_type,
            available_from=available_from,
            available_to=available_to,
            days_unavailable=days_unavailable,
            list_price=list_price,
            non_standard_accessories=non_standard_accessories,
            employee_capital_contributions=employee_capital_contributions,
            employee_private_contributions=employee_private_contributions,
            free_fuel=free_fuel,
            fuel_available_from=fuel_available_from,
            fuel_available_to=fuel_available_to,
            free_fuel_reinstated=free_fuel_reinstated,
            registered_prior_to_1998=registered_prior_to_1998,
            rate=rate,
            chargeable_value=chargeable_value,
            full_year_charge=full_year_charge,
            cash_equivalent=cash_equivalent,
            cash_equivalent_fuel=cash_equivalent_fuel,
        )

        return benefit_details_car
