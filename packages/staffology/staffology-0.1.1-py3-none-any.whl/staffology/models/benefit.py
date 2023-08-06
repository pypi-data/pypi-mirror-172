from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.benefit_declaration_type import BenefitDeclarationType
from ..models.benefit_details_asset_type import BenefitDetailsAssetType
from ..models.benefit_details_car import BenefitDetailsCar
from ..models.benefit_details_class_1a_type import BenefitDetailsClass1AType
from ..models.benefit_details_loan import BenefitDetailsLoan
from ..models.benefit_details_non_class_1a_type import BenefitDetailsNonClass1AType
from ..models.benefit_details_payment_type import BenefitDetailsPaymentType
from ..models.benefit_details_use_of_asset_type import BenefitDetailsUseOfAssetType
from ..models.benefit_type import BenefitType
from ..models.item import Item
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Benefit")


@attr.s(auto_attribs=True)
class Benefit:
    """Used to represent Benefits and Expenses

    Attributes:
        tax_year (Union[Unset, TaxYear]):
        type (Union[Unset, BenefitType]):
        declaration_type (Union[Unset, BenefitDeclarationType]):
        description (Union[Unset, None, str]): A description of this benefit
        value (Union[Unset, float]):
        employee_contribution (Union[Unset, float]):
        cash_equivalent (Union[Unset, float]): [readonly]
        asset_type (Union[Unset, BenefitDetailsAssetType]):
        use_of_asset_type (Union[Unset, BenefitDetailsUseOfAssetType]):
        class_1a_type (Union[Unset, BenefitDetailsClass1AType]):
        non_class_1a_type (Union[Unset, BenefitDetailsNonClass1AType]):
        payment_type (Union[Unset, BenefitDetailsPaymentType]):
        trading_organisation (Union[Unset, bool]): Only relevant to Benefits with Type Entertainment
        cash_equivalent_fuel (Union[Unset, float]): Only relevant to Benefits with Type Vans
        loan (Union[Unset, BenefitDetailsLoan]):
        car (Union[Unset, BenefitDetailsCar]):
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    type: Union[Unset, BenefitType] = UNSET
    declaration_type: Union[Unset, BenefitDeclarationType] = UNSET
    description: Union[Unset, None, str] = UNSET
    value: Union[Unset, float] = UNSET
    employee_contribution: Union[Unset, float] = UNSET
    cash_equivalent: Union[Unset, float] = UNSET
    asset_type: Union[Unset, BenefitDetailsAssetType] = UNSET
    use_of_asset_type: Union[Unset, BenefitDetailsUseOfAssetType] = UNSET
    class_1a_type: Union[Unset, BenefitDetailsClass1AType] = UNSET
    non_class_1a_type: Union[Unset, BenefitDetailsNonClass1AType] = UNSET
    payment_type: Union[Unset, BenefitDetailsPaymentType] = UNSET
    trading_organisation: Union[Unset, bool] = UNSET
    cash_equivalent_fuel: Union[Unset, float] = UNSET
    loan: Union[Unset, BenefitDetailsLoan] = UNSET
    car: Union[Unset, BenefitDetailsCar] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        declaration_type: Union[Unset, str] = UNSET
        if not isinstance(self.declaration_type, Unset):
            declaration_type = self.declaration_type.value

        description = self.description
        value = self.value
        employee_contribution = self.employee_contribution
        cash_equivalent = self.cash_equivalent
        asset_type: Union[Unset, str] = UNSET
        if not isinstance(self.asset_type, Unset):
            asset_type = self.asset_type.value

        use_of_asset_type: Union[Unset, str] = UNSET
        if not isinstance(self.use_of_asset_type, Unset):
            use_of_asset_type = self.use_of_asset_type.value

        class_1a_type: Union[Unset, str] = UNSET
        if not isinstance(self.class_1a_type, Unset):
            class_1a_type = self.class_1a_type.value

        non_class_1a_type: Union[Unset, str] = UNSET
        if not isinstance(self.non_class_1a_type, Unset):
            non_class_1a_type = self.non_class_1a_type.value

        payment_type: Union[Unset, str] = UNSET
        if not isinstance(self.payment_type, Unset):
            payment_type = self.payment_type.value

        trading_organisation = self.trading_organisation
        cash_equivalent_fuel = self.cash_equivalent_fuel
        loan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.loan, Unset):
            loan = self.loan.to_dict()

        car: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.car, Unset):
            car = self.car.to_dict()

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if type is not UNSET:
            field_dict["type"] = type
        if declaration_type is not UNSET:
            field_dict["declarationType"] = declaration_type
        if description is not UNSET:
            field_dict["description"] = description
        if value is not UNSET:
            field_dict["value"] = value
        if employee_contribution is not UNSET:
            field_dict["employeeContribution"] = employee_contribution
        if cash_equivalent is not UNSET:
            field_dict["cashEquivalent"] = cash_equivalent
        if asset_type is not UNSET:
            field_dict["assetType"] = asset_type
        if use_of_asset_type is not UNSET:
            field_dict["useOfAssetType"] = use_of_asset_type
        if class_1a_type is not UNSET:
            field_dict["class1AType"] = class_1a_type
        if non_class_1a_type is not UNSET:
            field_dict["nonClass1AType"] = non_class_1a_type
        if payment_type is not UNSET:
            field_dict["paymentType"] = payment_type
        if trading_organisation is not UNSET:
            field_dict["tradingOrganisation"] = trading_organisation
        if cash_equivalent_fuel is not UNSET:
            field_dict["cashEquivalentFuel"] = cash_equivalent_fuel
        if loan is not UNSET:
            field_dict["loan"] = loan
        if car is not UNSET:
            field_dict["car"] = car
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _type = d.pop("type", UNSET)
        type: Union[Unset, BenefitType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = BenefitType(_type)

        _declaration_type = d.pop("declarationType", UNSET)
        declaration_type: Union[Unset, BenefitDeclarationType]
        if isinstance(_declaration_type, Unset):
            declaration_type = UNSET
        else:
            declaration_type = BenefitDeclarationType(_declaration_type)

        description = d.pop("description", UNSET)

        value = d.pop("value", UNSET)

        employee_contribution = d.pop("employeeContribution", UNSET)

        cash_equivalent = d.pop("cashEquivalent", UNSET)

        _asset_type = d.pop("assetType", UNSET)
        asset_type: Union[Unset, BenefitDetailsAssetType]
        if isinstance(_asset_type, Unset):
            asset_type = UNSET
        else:
            asset_type = BenefitDetailsAssetType(_asset_type)

        _use_of_asset_type = d.pop("useOfAssetType", UNSET)
        use_of_asset_type: Union[Unset, BenefitDetailsUseOfAssetType]
        if isinstance(_use_of_asset_type, Unset):
            use_of_asset_type = UNSET
        else:
            use_of_asset_type = BenefitDetailsUseOfAssetType(_use_of_asset_type)

        _class_1a_type = d.pop("class1AType", UNSET)
        class_1a_type: Union[Unset, BenefitDetailsClass1AType]
        if isinstance(_class_1a_type, Unset):
            class_1a_type = UNSET
        else:
            class_1a_type = BenefitDetailsClass1AType(_class_1a_type)

        _non_class_1a_type = d.pop("nonClass1AType", UNSET)
        non_class_1a_type: Union[Unset, BenefitDetailsNonClass1AType]
        if isinstance(_non_class_1a_type, Unset):
            non_class_1a_type = UNSET
        else:
            non_class_1a_type = BenefitDetailsNonClass1AType(_non_class_1a_type)

        _payment_type = d.pop("paymentType", UNSET)
        payment_type: Union[Unset, BenefitDetailsPaymentType]
        if isinstance(_payment_type, Unset):
            payment_type = UNSET
        else:
            payment_type = BenefitDetailsPaymentType(_payment_type)

        trading_organisation = d.pop("tradingOrganisation", UNSET)

        cash_equivalent_fuel = d.pop("cashEquivalentFuel", UNSET)

        _loan = d.pop("loan", UNSET)
        loan: Union[Unset, BenefitDetailsLoan]
        if isinstance(_loan, Unset):
            loan = UNSET
        else:
            loan = BenefitDetailsLoan.from_dict(_loan)

        _car = d.pop("car", UNSET)
        car: Union[Unset, BenefitDetailsCar]
        if isinstance(_car, Unset):
            car = UNSET
        else:
            car = BenefitDetailsCar.from_dict(_car)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        benefit = cls(
            tax_year=tax_year,
            type=type,
            declaration_type=declaration_type,
            description=description,
            value=value,
            employee_contribution=employee_contribution,
            cash_equivalent=cash_equivalent,
            asset_type=asset_type,
            use_of_asset_type=use_of_asset_type,
            class_1a_type=class_1a_type,
            non_class_1a_type=non_class_1a_type,
            payment_type=payment_type,
            trading_organisation=trading_organisation,
            cash_equivalent_fuel=cash_equivalent_fuel,
            loan=loan,
            car=car,
            employee=employee,
            id=id,
        )

        return benefit
