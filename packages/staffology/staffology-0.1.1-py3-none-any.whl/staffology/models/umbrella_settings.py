from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UmbrellaSettings")


@attr.s(auto_attribs=True)
class UmbrellaSettings:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        charge_per_timesheet (Union[Unset, float]):
        apprenticeship_levy_dedn_rate (Union[Unset, float]):
        holiday_rate (Union[Unset, float]):
        dpsb_code (Union[Unset, None, str]):
        expenses_code (Union[Unset, None, str]):
        gross_deduction_code (Union[Unset, None, str]):
        holiday_code (Union[Unset, None, str]):
        cis_fee_code (Union[Unset, None, str]):
        detail_fee_in_comment (Union[Unset, bool]):
    """

    enabled: Union[Unset, bool] = UNSET
    charge_per_timesheet: Union[Unset, float] = UNSET
    apprenticeship_levy_dedn_rate: Union[Unset, float] = UNSET
    holiday_rate: Union[Unset, float] = UNSET
    dpsb_code: Union[Unset, None, str] = UNSET
    expenses_code: Union[Unset, None, str] = UNSET
    gross_deduction_code: Union[Unset, None, str] = UNSET
    holiday_code: Union[Unset, None, str] = UNSET
    cis_fee_code: Union[Unset, None, str] = UNSET
    detail_fee_in_comment: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        charge_per_timesheet = self.charge_per_timesheet
        apprenticeship_levy_dedn_rate = self.apprenticeship_levy_dedn_rate
        holiday_rate = self.holiday_rate
        dpsb_code = self.dpsb_code
        expenses_code = self.expenses_code
        gross_deduction_code = self.gross_deduction_code
        holiday_code = self.holiday_code
        cis_fee_code = self.cis_fee_code
        detail_fee_in_comment = self.detail_fee_in_comment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if charge_per_timesheet is not UNSET:
            field_dict["chargePerTimesheet"] = charge_per_timesheet
        if apprenticeship_levy_dedn_rate is not UNSET:
            field_dict["apprenticeshipLevyDednRate"] = apprenticeship_levy_dedn_rate
        if holiday_rate is not UNSET:
            field_dict["holidayRate"] = holiday_rate
        if dpsb_code is not UNSET:
            field_dict["dpsbCode"] = dpsb_code
        if expenses_code is not UNSET:
            field_dict["expensesCode"] = expenses_code
        if gross_deduction_code is not UNSET:
            field_dict["grossDeductionCode"] = gross_deduction_code
        if holiday_code is not UNSET:
            field_dict["holidayCode"] = holiday_code
        if cis_fee_code is not UNSET:
            field_dict["cisFeeCode"] = cis_fee_code
        if detail_fee_in_comment is not UNSET:
            field_dict["detailFeeInComment"] = detail_fee_in_comment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        charge_per_timesheet = d.pop("chargePerTimesheet", UNSET)

        apprenticeship_levy_dedn_rate = d.pop("apprenticeshipLevyDednRate", UNSET)

        holiday_rate = d.pop("holidayRate", UNSET)

        dpsb_code = d.pop("dpsbCode", UNSET)

        expenses_code = d.pop("expensesCode", UNSET)

        gross_deduction_code = d.pop("grossDeductionCode", UNSET)

        holiday_code = d.pop("holidayCode", UNSET)

        cis_fee_code = d.pop("cisFeeCode", UNSET)

        detail_fee_in_comment = d.pop("detailFeeInComment", UNSET)

        umbrella_settings = cls(
            enabled=enabled,
            charge_per_timesheet=charge_per_timesheet,
            apprenticeship_levy_dedn_rate=apprenticeship_levy_dedn_rate,
            holiday_rate=holiday_rate,
            dpsb_code=dpsb_code,
            expenses_code=expenses_code,
            gross_deduction_code=gross_deduction_code,
            holiday_code=holiday_code,
            cis_fee_code=cis_fee_code,
            detail_fee_in_comment=detail_fee_in_comment,
        )

        return umbrella_settings
