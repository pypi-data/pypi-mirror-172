from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.exb_p11d_employee import ExbP11DEmployee
from ..models.p11d_asset_available_collection import P11DAssetAvailableCollection
from ..models.p11d_asset_transferred_collection import P11DAssetTransferredCollection
from ..models.p11d_car_collection import P11DCarCollection
from ..models.p11d_expenses import P11DExpenses
from ..models.p11d_loan_collection import P11DLoanCollection
from ..models.p11d_other import P11DOther
from ..models.p11d_payment_collection import P11DPaymentCollection
from ..models.p11d_single_item import P11DSingleItem
from ..models.p11d_vans import P11DVans
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11D")


@attr.s(auto_attribs=True)
class ExbP11D:
    """
    Attributes:
        employee (Union[Unset, ExbP11DEmployee]):
        transferred (Union[Unset, P11DAssetTransferredCollection]):
        payments (Union[Unset, P11DPaymentCollection]):
        vouchers_or_c_cs (Union[Unset, P11DSingleItem]):
        living_accom (Union[Unset, P11DSingleItem]):
        mileage_allow (Union[Unset, P11DSingleItem]):
        cars (Union[Unset, P11DCarCollection]):
        vans (Union[Unset, P11DVans]):
        loans (Union[Unset, P11DLoanCollection]):
        medical (Union[Unset, P11DSingleItem]):
        relocation (Union[Unset, P11DSingleItem]):
        services (Union[Unset, P11DSingleItem]):
        assets_avail (Union[Unset, P11DAssetAvailableCollection]):
        other (Union[Unset, P11DOther]):
        exp_paid (Union[Unset, P11DExpenses]):
    """

    employee: Union[Unset, ExbP11DEmployee] = UNSET
    transferred: Union[Unset, P11DAssetTransferredCollection] = UNSET
    payments: Union[Unset, P11DPaymentCollection] = UNSET
    vouchers_or_c_cs: Union[Unset, P11DSingleItem] = UNSET
    living_accom: Union[Unset, P11DSingleItem] = UNSET
    mileage_allow: Union[Unset, P11DSingleItem] = UNSET
    cars: Union[Unset, P11DCarCollection] = UNSET
    vans: Union[Unset, P11DVans] = UNSET
    loans: Union[Unset, P11DLoanCollection] = UNSET
    medical: Union[Unset, P11DSingleItem] = UNSET
    relocation: Union[Unset, P11DSingleItem] = UNSET
    services: Union[Unset, P11DSingleItem] = UNSET
    assets_avail: Union[Unset, P11DAssetAvailableCollection] = UNSET
    other: Union[Unset, P11DOther] = UNSET
    exp_paid: Union[Unset, P11DExpenses] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        transferred: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transferred, Unset):
            transferred = self.transferred.to_dict()

        payments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payments, Unset):
            payments = self.payments.to_dict()

        vouchers_or_c_cs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.vouchers_or_c_cs, Unset):
            vouchers_or_c_cs = self.vouchers_or_c_cs.to_dict()

        living_accom: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.living_accom, Unset):
            living_accom = self.living_accom.to_dict()

        mileage_allow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mileage_allow, Unset):
            mileage_allow = self.mileage_allow.to_dict()

        cars: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cars, Unset):
            cars = self.cars.to_dict()

        vans: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.vans, Unset):
            vans = self.vans.to_dict()

        loans: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.loans, Unset):
            loans = self.loans.to_dict()

        medical: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.medical, Unset):
            medical = self.medical.to_dict()

        relocation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relocation, Unset):
            relocation = self.relocation.to_dict()

        services: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.services, Unset):
            services = self.services.to_dict()

        assets_avail: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assets_avail, Unset):
            assets_avail = self.assets_avail.to_dict()

        other: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.other, Unset):
            other = self.other.to_dict()

        exp_paid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exp_paid, Unset):
            exp_paid = self.exp_paid.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if transferred is not UNSET:
            field_dict["transferred"] = transferred
        if payments is not UNSET:
            field_dict["payments"] = payments
        if vouchers_or_c_cs is not UNSET:
            field_dict["vouchersOrCCs"] = vouchers_or_c_cs
        if living_accom is not UNSET:
            field_dict["livingAccom"] = living_accom
        if mileage_allow is not UNSET:
            field_dict["mileageAllow"] = mileage_allow
        if cars is not UNSET:
            field_dict["cars"] = cars
        if vans is not UNSET:
            field_dict["vans"] = vans
        if loans is not UNSET:
            field_dict["loans"] = loans
        if medical is not UNSET:
            field_dict["medical"] = medical
        if relocation is not UNSET:
            field_dict["relocation"] = relocation
        if services is not UNSET:
            field_dict["services"] = services
        if assets_avail is not UNSET:
            field_dict["assetsAvail"] = assets_avail
        if other is not UNSET:
            field_dict["other"] = other
        if exp_paid is not UNSET:
            field_dict["expPaid"] = exp_paid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, ExbP11DEmployee]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = ExbP11DEmployee.from_dict(_employee)

        _transferred = d.pop("transferred", UNSET)
        transferred: Union[Unset, P11DAssetTransferredCollection]
        if isinstance(_transferred, Unset):
            transferred = UNSET
        else:
            transferred = P11DAssetTransferredCollection.from_dict(_transferred)

        _payments = d.pop("payments", UNSET)
        payments: Union[Unset, P11DPaymentCollection]
        if isinstance(_payments, Unset):
            payments = UNSET
        else:
            payments = P11DPaymentCollection.from_dict(_payments)

        _vouchers_or_c_cs = d.pop("vouchersOrCCs", UNSET)
        vouchers_or_c_cs: Union[Unset, P11DSingleItem]
        if isinstance(_vouchers_or_c_cs, Unset):
            vouchers_or_c_cs = UNSET
        else:
            vouchers_or_c_cs = P11DSingleItem.from_dict(_vouchers_or_c_cs)

        _living_accom = d.pop("livingAccom", UNSET)
        living_accom: Union[Unset, P11DSingleItem]
        if isinstance(_living_accom, Unset):
            living_accom = UNSET
        else:
            living_accom = P11DSingleItem.from_dict(_living_accom)

        _mileage_allow = d.pop("mileageAllow", UNSET)
        mileage_allow: Union[Unset, P11DSingleItem]
        if isinstance(_mileage_allow, Unset):
            mileage_allow = UNSET
        else:
            mileage_allow = P11DSingleItem.from_dict(_mileage_allow)

        _cars = d.pop("cars", UNSET)
        cars: Union[Unset, P11DCarCollection]
        if isinstance(_cars, Unset):
            cars = UNSET
        else:
            cars = P11DCarCollection.from_dict(_cars)

        _vans = d.pop("vans", UNSET)
        vans: Union[Unset, P11DVans]
        if isinstance(_vans, Unset):
            vans = UNSET
        else:
            vans = P11DVans.from_dict(_vans)

        _loans = d.pop("loans", UNSET)
        loans: Union[Unset, P11DLoanCollection]
        if isinstance(_loans, Unset):
            loans = UNSET
        else:
            loans = P11DLoanCollection.from_dict(_loans)

        _medical = d.pop("medical", UNSET)
        medical: Union[Unset, P11DSingleItem]
        if isinstance(_medical, Unset):
            medical = UNSET
        else:
            medical = P11DSingleItem.from_dict(_medical)

        _relocation = d.pop("relocation", UNSET)
        relocation: Union[Unset, P11DSingleItem]
        if isinstance(_relocation, Unset):
            relocation = UNSET
        else:
            relocation = P11DSingleItem.from_dict(_relocation)

        _services = d.pop("services", UNSET)
        services: Union[Unset, P11DSingleItem]
        if isinstance(_services, Unset):
            services = UNSET
        else:
            services = P11DSingleItem.from_dict(_services)

        _assets_avail = d.pop("assetsAvail", UNSET)
        assets_avail: Union[Unset, P11DAssetAvailableCollection]
        if isinstance(_assets_avail, Unset):
            assets_avail = UNSET
        else:
            assets_avail = P11DAssetAvailableCollection.from_dict(_assets_avail)

        _other = d.pop("other", UNSET)
        other: Union[Unset, P11DOther]
        if isinstance(_other, Unset):
            other = UNSET
        else:
            other = P11DOther.from_dict(_other)

        _exp_paid = d.pop("expPaid", UNSET)
        exp_paid: Union[Unset, P11DExpenses]
        if isinstance(_exp_paid, Unset):
            exp_paid = UNSET
        else:
            exp_paid = P11DExpenses.from_dict(_exp_paid)

        exb_p11d = cls(
            employee=employee,
            transferred=transferred,
            payments=payments,
            vouchers_or_c_cs=vouchers_or_c_cs,
            living_accom=living_accom,
            mileage_allow=mileage_allow,
            cars=cars,
            vans=vans,
            loans=loans,
            medical=medical,
            relocation=relocation,
            services=services,
            assets_avail=assets_avail,
            other=other,
            exp_paid=exp_paid,
        )

        return exb_p11d
