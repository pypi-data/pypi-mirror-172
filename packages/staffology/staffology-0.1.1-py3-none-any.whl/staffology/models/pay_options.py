from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fps_fields import FpsFields
from ..models.mileage_vehicle_type import MileageVehicleType
from ..models.pay_basis import PayBasis
from ..models.pay_line import PayLine
from ..models.pay_method import PayMethod
from ..models.pay_periods import PayPeriods
from ..models.tax_and_ni import TaxAndNi
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayOptions")


@attr.s(auto_attribs=True)
class PayOptions:
    """This object forms the basis of the Employees payment.

    Attributes:
        period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]): Indicates whether to use first, second, third (etc) PaySchedule for this PayPeriod.
        pay_amount (Union[Unset, float]): The amount the Employee is regularly paid each period
        basis (Union[Unset, PayBasis]):
        national_minimum_wage (Union[Unset, bool]):
        pay_amount_multiplier (Union[Unset, float]): This property is irrelevant if the basis is Monthly.
            But if the basis is Daily or Hourly then this property sets how many days/hours the employee should be paid for
            in the period.
        base_hourly_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base hourly rate. Eg Overtime.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        base_daily_rate (Union[Unset, float]): This property is used to calculate values for PayCodes that are set as
            multiples of
            the employees base daily rate. Eg sick.
            If this is set as zero then we'll attempt to calculate a value based on the other fields
        auto_adjust_for_leave (Union[Unset, bool]): Automatically reduce the PayAmount when the Employee has Leave that
            is either Not Paid or has Statutory Pay.
            Can only be set to True if the Basis is Monthly (ie, employee is not paid an hourly or daily rate).
            If set to false then you must manually reduce their payment to reflect any Leave
        method (Union[Unset, PayMethod]):
        pay_code (Union[Unset, None, str]): If you want the Employees pay to be allocated to a code other than BASIC,
            specify it here
        withhold_tax_refund_if_pay_is_zero (Union[Unset, bool]): If you don't want negative PAYE values when the Gross
            pay is zero, set this to true
        mileage_vehicle_type (Union[Unset, MileageVehicleType]):
        maps_miles (Union[Unset, None, int]): The number of miles to pay for as Mileage Allowance Payments
        tax_and_ni (Union[Unset, TaxAndNi]):
        fps_fields (Union[Unset, FpsFields]):
        regular_pay_lines (Union[Unset, None, List[PayLine]]): These are used to make additions/deductions to the pay
            for this Employee.
            You do not need to include Pension, Tax, NI,  Loan Repayments, etc as these will all be automatically created.
        tags (Union[Unset, None, List[str]]):
    """

    period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    pay_amount: Union[Unset, float] = UNSET
    basis: Union[Unset, PayBasis] = UNSET
    national_minimum_wage: Union[Unset, bool] = UNSET
    pay_amount_multiplier: Union[Unset, float] = UNSET
    base_hourly_rate: Union[Unset, float] = UNSET
    base_daily_rate: Union[Unset, float] = UNSET
    auto_adjust_for_leave: Union[Unset, bool] = UNSET
    method: Union[Unset, PayMethod] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    withhold_tax_refund_if_pay_is_zero: Union[Unset, bool] = UNSET
    mileage_vehicle_type: Union[Unset, MileageVehicleType] = UNSET
    maps_miles: Union[Unset, None, int] = UNSET
    tax_and_ni: Union[Unset, TaxAndNi] = UNSET
    fps_fields: Union[Unset, FpsFields] = UNSET
    regular_pay_lines: Union[Unset, None, List[PayLine]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        period: Union[Unset, str] = UNSET
        if not isinstance(self.period, Unset):
            period = self.period.value

        ordinal = self.ordinal
        pay_amount = self.pay_amount
        basis: Union[Unset, str] = UNSET
        if not isinstance(self.basis, Unset):
            basis = self.basis.value

        national_minimum_wage = self.national_minimum_wage
        pay_amount_multiplier = self.pay_amount_multiplier
        base_hourly_rate = self.base_hourly_rate
        base_daily_rate = self.base_daily_rate
        auto_adjust_for_leave = self.auto_adjust_for_leave
        method: Union[Unset, str] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        pay_code = self.pay_code
        withhold_tax_refund_if_pay_is_zero = self.withhold_tax_refund_if_pay_is_zero
        mileage_vehicle_type: Union[Unset, str] = UNSET
        if not isinstance(self.mileage_vehicle_type, Unset):
            mileage_vehicle_type = self.mileage_vehicle_type.value

        maps_miles = self.maps_miles
        tax_and_ni: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tax_and_ni, Unset):
            tax_and_ni = self.tax_and_ni.to_dict()

        fps_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fps_fields, Unset):
            fps_fields = self.fps_fields.to_dict()

        regular_pay_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.regular_pay_lines, Unset):
            if self.regular_pay_lines is None:
                regular_pay_lines = None
            else:
                regular_pay_lines = []
                for regular_pay_lines_item_data in self.regular_pay_lines:
                    regular_pay_lines_item = regular_pay_lines_item_data.to_dict()

                    regular_pay_lines.append(regular_pay_lines_item)

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if period is not UNSET:
            field_dict["period"] = period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if pay_amount is not UNSET:
            field_dict["payAmount"] = pay_amount
        if basis is not UNSET:
            field_dict["basis"] = basis
        if national_minimum_wage is not UNSET:
            field_dict["nationalMinimumWage"] = national_minimum_wage
        if pay_amount_multiplier is not UNSET:
            field_dict["payAmountMultiplier"] = pay_amount_multiplier
        if base_hourly_rate is not UNSET:
            field_dict["baseHourlyRate"] = base_hourly_rate
        if base_daily_rate is not UNSET:
            field_dict["baseDailyRate"] = base_daily_rate
        if auto_adjust_for_leave is not UNSET:
            field_dict["autoAdjustForLeave"] = auto_adjust_for_leave
        if method is not UNSET:
            field_dict["method"] = method
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if withhold_tax_refund_if_pay_is_zero is not UNSET:
            field_dict[
                "withholdTaxRefundIfPayIsZero"
            ] = withhold_tax_refund_if_pay_is_zero
        if mileage_vehicle_type is not UNSET:
            field_dict["mileageVehicleType"] = mileage_vehicle_type
        if maps_miles is not UNSET:
            field_dict["mapsMiles"] = maps_miles
        if tax_and_ni is not UNSET:
            field_dict["taxAndNi"] = tax_and_ni
        if fps_fields is not UNSET:
            field_dict["fpsFields"] = fps_fields
        if regular_pay_lines is not UNSET:
            field_dict["regularPayLines"] = regular_pay_lines
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _period = d.pop("period", UNSET)
        period: Union[Unset, PayPeriods]
        if isinstance(_period, Unset):
            period = UNSET
        else:
            period = PayPeriods(_period)

        ordinal = d.pop("ordinal", UNSET)

        pay_amount = d.pop("payAmount", UNSET)

        _basis = d.pop("basis", UNSET)
        basis: Union[Unset, PayBasis]
        if isinstance(_basis, Unset):
            basis = UNSET
        else:
            basis = PayBasis(_basis)

        national_minimum_wage = d.pop("nationalMinimumWage", UNSET)

        pay_amount_multiplier = d.pop("payAmountMultiplier", UNSET)

        base_hourly_rate = d.pop("baseHourlyRate", UNSET)

        base_daily_rate = d.pop("baseDailyRate", UNSET)

        auto_adjust_for_leave = d.pop("autoAdjustForLeave", UNSET)

        _method = d.pop("method", UNSET)
        method: Union[Unset, PayMethod]
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = PayMethod(_method)

        pay_code = d.pop("payCode", UNSET)

        withhold_tax_refund_if_pay_is_zero = d.pop(
            "withholdTaxRefundIfPayIsZero", UNSET
        )

        _mileage_vehicle_type = d.pop("mileageVehicleType", UNSET)
        mileage_vehicle_type: Union[Unset, MileageVehicleType]
        if isinstance(_mileage_vehicle_type, Unset):
            mileage_vehicle_type = UNSET
        else:
            mileage_vehicle_type = MileageVehicleType(_mileage_vehicle_type)

        maps_miles = d.pop("mapsMiles", UNSET)

        _tax_and_ni = d.pop("taxAndNi", UNSET)
        tax_and_ni: Union[Unset, TaxAndNi]
        if isinstance(_tax_and_ni, Unset):
            tax_and_ni = UNSET
        else:
            tax_and_ni = TaxAndNi.from_dict(_tax_and_ni)

        _fps_fields = d.pop("fpsFields", UNSET)
        fps_fields: Union[Unset, FpsFields]
        if isinstance(_fps_fields, Unset):
            fps_fields = UNSET
        else:
            fps_fields = FpsFields.from_dict(_fps_fields)

        regular_pay_lines = []
        _regular_pay_lines = d.pop("regularPayLines", UNSET)
        for regular_pay_lines_item_data in _regular_pay_lines or []:
            regular_pay_lines_item = PayLine.from_dict(regular_pay_lines_item_data)

            regular_pay_lines.append(regular_pay_lines_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        pay_options = cls(
            period=period,
            ordinal=ordinal,
            pay_amount=pay_amount,
            basis=basis,
            national_minimum_wage=national_minimum_wage,
            pay_amount_multiplier=pay_amount_multiplier,
            base_hourly_rate=base_hourly_rate,
            base_daily_rate=base_daily_rate,
            auto_adjust_for_leave=auto_adjust_for_leave,
            method=method,
            pay_code=pay_code,
            withhold_tax_refund_if_pay_is_zero=withhold_tax_refund_if_pay_is_zero,
            mileage_vehicle_type=mileage_vehicle_type,
            maps_miles=maps_miles,
            tax_and_ni=tax_and_ni,
            fps_fields=fps_fields,
            regular_pay_lines=regular_pay_lines,
            tags=tags,
        )

        return pay_options
