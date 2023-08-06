from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_code_calculation_type import PayCodeCalculationType
from ..models.pay_code_multiplier_type import PayCodeMultiplierType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayCode")


@attr.s(auto_attribs=True)
class PayCode:
    """Each PayLine has a Code. The Code will match the Code property of a PayCode.
    The PayCode that is used determines how the amount is treated with regards to tax, NI and pensions

        Attributes:
            title (str):
            code (str):
            default_value (Union[Unset, None, float]): If a non-zero value is provided then when this code is selected in
                our UI the value will be automatically filled.
            is_deduction (Union[Unset, bool]): If set to true then a PayLine using this code will be treated as a deduction
                as opposed to an addition.
            is_niable (Union[Unset, bool]): Determines whether or not the value of PayLines using this code should be taken
                into consideration when calculating National Insurance Contributions.
            is_taxable (Union[Unset, bool]): Determines whether or not the value of PayLines using this code should be taken
                into consideration when calculating the PAYE liability.
            is_pensionable (Union[Unset, bool]): Determines whether or not the value of PayLines using this code should be
                taken into consideration when calculating the total pensionable pay.
            is_attachable (Union[Unset, bool]): Determines whether or not the value of PayLines using this code should be
                taken into consideration when calculating the attachable pay for AttachmentOrders.
            is_real_time_class_1_a_niable (Union[Unset, bool]): Determines whether or not the value of PayLines using this
                code are subject to real time Class 1A NIC.
            is_not_contributing_to_holiday_pay (Union[Unset, bool]): If true then any payments made using this code will not
                contribute towards holiday pay calculations.
            is_qualifying_earnings_for_ae (Union[Unset, None, bool]): If true then any payments made using this code will be
                used as the basis for calculating QualifyingEarnings for AutoEnrolment assessments.
                If it is set to null then when it's next retrieved it'll have the same value as PensionablePay
            is_not_tierable (Union[Unset, bool]): If true then any payments made using this code will not be included when
                calculating the tier an employee should be on for a Tiered Pension.
            is_tcp_tcls (Union[Unset, bool]): If true then any payments made using this code will be reported as
                a Trivial Commutation Payment (A - TCLS)
            is_tcp_pp (Union[Unset, bool]): If true then any payments made using this code will be reported as
                a Trivial Commutation Payment (B - Personal Pension)
            is_tcp_op (Union[Unset, bool]): If true then any payments made using this code will be reported as
                a Trivial Commutation Payment (C - Occupational Pension)
            is_flexi_dd_death_benefit (Union[Unset, bool]): If true then any payments made using this code will be reported
                as
                a Flexible Drawdown of Death Benefit
            is_flexi_dd_pension (Union[Unset, bool]): If true then any payments made using this code will be reported as
                a Flexible Drawdown flexibly accessing a pension
            calculation_type (Union[Unset, PayCodeCalculationType]):
            multiplier_type (Union[Unset, PayCodeMultiplierType]):
            daily_rate_multiplier (Union[Unset, float]): If the MultiplierType is MultipleOfDailyRate then this sets the
                multiple to be used, ie 1.5
            hourly_rate_multiplier (Union[Unset, float]): If the MultiplierType is MultipleOfHourlyRate then this sets the
                multiple to be used, ie 1.5
            is_system_code (Union[Unset, bool]): [readonly] System Codes cannot be deleted or edited
            is_control_code (Union[Unset, bool]): [readonly] Control Codes cannot be deleted or edited nor can PayLines be
                assigned to them.
            payee (Union[Unset, None, str]): The Id of the Payee, if any, that deductions are to be paid to.
    """

    title: str
    code: str
    default_value: Union[Unset, None, float] = UNSET
    is_deduction: Union[Unset, bool] = UNSET
    is_niable: Union[Unset, bool] = UNSET
    is_taxable: Union[Unset, bool] = UNSET
    is_pensionable: Union[Unset, bool] = UNSET
    is_attachable: Union[Unset, bool] = UNSET
    is_real_time_class_1_a_niable: Union[Unset, bool] = UNSET
    is_not_contributing_to_holiday_pay: Union[Unset, bool] = UNSET
    is_qualifying_earnings_for_ae: Union[Unset, None, bool] = UNSET
    is_not_tierable: Union[Unset, bool] = UNSET
    is_tcp_tcls: Union[Unset, bool] = UNSET
    is_tcp_pp: Union[Unset, bool] = UNSET
    is_tcp_op: Union[Unset, bool] = UNSET
    is_flexi_dd_death_benefit: Union[Unset, bool] = UNSET
    is_flexi_dd_pension: Union[Unset, bool] = UNSET
    calculation_type: Union[Unset, PayCodeCalculationType] = UNSET
    multiplier_type: Union[Unset, PayCodeMultiplierType] = UNSET
    daily_rate_multiplier: Union[Unset, float] = UNSET
    hourly_rate_multiplier: Union[Unset, float] = UNSET
    is_system_code: Union[Unset, bool] = UNSET
    is_control_code: Union[Unset, bool] = UNSET
    payee: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        code = self.code
        default_value = self.default_value
        is_deduction = self.is_deduction
        is_niable = self.is_niable
        is_taxable = self.is_taxable
        is_pensionable = self.is_pensionable
        is_attachable = self.is_attachable
        is_real_time_class_1_a_niable = self.is_real_time_class_1_a_niable
        is_not_contributing_to_holiday_pay = self.is_not_contributing_to_holiday_pay
        is_qualifying_earnings_for_ae = self.is_qualifying_earnings_for_ae
        is_not_tierable = self.is_not_tierable
        is_tcp_tcls = self.is_tcp_tcls
        is_tcp_pp = self.is_tcp_pp
        is_tcp_op = self.is_tcp_op
        is_flexi_dd_death_benefit = self.is_flexi_dd_death_benefit
        is_flexi_dd_pension = self.is_flexi_dd_pension
        calculation_type: Union[Unset, str] = UNSET
        if not isinstance(self.calculation_type, Unset):
            calculation_type = self.calculation_type.value

        multiplier_type: Union[Unset, str] = UNSET
        if not isinstance(self.multiplier_type, Unset):
            multiplier_type = self.multiplier_type.value

        daily_rate_multiplier = self.daily_rate_multiplier
        hourly_rate_multiplier = self.hourly_rate_multiplier
        is_system_code = self.is_system_code
        is_control_code = self.is_control_code
        payee = self.payee

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "title": title,
                "code": code,
            }
        )
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if is_deduction is not UNSET:
            field_dict["isDeduction"] = is_deduction
        if is_niable is not UNSET:
            field_dict["isNiable"] = is_niable
        if is_taxable is not UNSET:
            field_dict["isTaxable"] = is_taxable
        if is_pensionable is not UNSET:
            field_dict["isPensionable"] = is_pensionable
        if is_attachable is not UNSET:
            field_dict["isAttachable"] = is_attachable
        if is_real_time_class_1_a_niable is not UNSET:
            field_dict["isRealTimeClass1aNiable"] = is_real_time_class_1_a_niable
        if is_not_contributing_to_holiday_pay is not UNSET:
            field_dict[
                "isNotContributingToHolidayPay"
            ] = is_not_contributing_to_holiday_pay
        if is_qualifying_earnings_for_ae is not UNSET:
            field_dict["isQualifyingEarningsForAe"] = is_qualifying_earnings_for_ae
        if is_not_tierable is not UNSET:
            field_dict["isNotTierable"] = is_not_tierable
        if is_tcp_tcls is not UNSET:
            field_dict["isTcp_Tcls"] = is_tcp_tcls
        if is_tcp_pp is not UNSET:
            field_dict["isTcp_Pp"] = is_tcp_pp
        if is_tcp_op is not UNSET:
            field_dict["isTcp_Op"] = is_tcp_op
        if is_flexi_dd_death_benefit is not UNSET:
            field_dict["isFlexiDd_DeathBenefit"] = is_flexi_dd_death_benefit
        if is_flexi_dd_pension is not UNSET:
            field_dict["isFlexiDd_Pension"] = is_flexi_dd_pension
        if calculation_type is not UNSET:
            field_dict["calculationType"] = calculation_type
        if multiplier_type is not UNSET:
            field_dict["multiplierType"] = multiplier_type
        if daily_rate_multiplier is not UNSET:
            field_dict["dailyRateMultiplier"] = daily_rate_multiplier
        if hourly_rate_multiplier is not UNSET:
            field_dict["hourlyRateMultiplier"] = hourly_rate_multiplier
        if is_system_code is not UNSET:
            field_dict["isSystemCode"] = is_system_code
        if is_control_code is not UNSET:
            field_dict["isControlCode"] = is_control_code
        if payee is not UNSET:
            field_dict["payee"] = payee

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        code = d.pop("code")

        default_value = d.pop("defaultValue", UNSET)

        is_deduction = d.pop("isDeduction", UNSET)

        is_niable = d.pop("isNiable", UNSET)

        is_taxable = d.pop("isTaxable", UNSET)

        is_pensionable = d.pop("isPensionable", UNSET)

        is_attachable = d.pop("isAttachable", UNSET)

        is_real_time_class_1_a_niable = d.pop("isRealTimeClass1aNiable", UNSET)

        is_not_contributing_to_holiday_pay = d.pop(
            "isNotContributingToHolidayPay", UNSET
        )

        is_qualifying_earnings_for_ae = d.pop("isQualifyingEarningsForAe", UNSET)

        is_not_tierable = d.pop("isNotTierable", UNSET)

        is_tcp_tcls = d.pop("isTcp_Tcls", UNSET)

        is_tcp_pp = d.pop("isTcp_Pp", UNSET)

        is_tcp_op = d.pop("isTcp_Op", UNSET)

        is_flexi_dd_death_benefit = d.pop("isFlexiDd_DeathBenefit", UNSET)

        is_flexi_dd_pension = d.pop("isFlexiDd_Pension", UNSET)

        _calculation_type = d.pop("calculationType", UNSET)
        calculation_type: Union[Unset, PayCodeCalculationType]
        if isinstance(_calculation_type, Unset):
            calculation_type = UNSET
        else:
            calculation_type = PayCodeCalculationType(_calculation_type)

        _multiplier_type = d.pop("multiplierType", UNSET)
        multiplier_type: Union[Unset, PayCodeMultiplierType]
        if isinstance(_multiplier_type, Unset):
            multiplier_type = UNSET
        else:
            multiplier_type = PayCodeMultiplierType(_multiplier_type)

        daily_rate_multiplier = d.pop("dailyRateMultiplier", UNSET)

        hourly_rate_multiplier = d.pop("hourlyRateMultiplier", UNSET)

        is_system_code = d.pop("isSystemCode", UNSET)

        is_control_code = d.pop("isControlCode", UNSET)

        payee = d.pop("payee", UNSET)

        pay_code = cls(
            title=title,
            code=code,
            default_value=default_value,
            is_deduction=is_deduction,
            is_niable=is_niable,
            is_taxable=is_taxable,
            is_pensionable=is_pensionable,
            is_attachable=is_attachable,
            is_real_time_class_1_a_niable=is_real_time_class_1_a_niable,
            is_not_contributing_to_holiday_pay=is_not_contributing_to_holiday_pay,
            is_qualifying_earnings_for_ae=is_qualifying_earnings_for_ae,
            is_not_tierable=is_not_tierable,
            is_tcp_tcls=is_tcp_tcls,
            is_tcp_pp=is_tcp_pp,
            is_tcp_op=is_tcp_op,
            is_flexi_dd_death_benefit=is_flexi_dd_death_benefit,
            is_flexi_dd_pension=is_flexi_dd_pension,
            calculation_type=calculation_type,
            multiplier_type=multiplier_type,
            daily_rate_multiplier=daily_rate_multiplier,
            hourly_rate_multiplier=hourly_rate_multiplier,
            is_system_code=is_system_code,
            is_control_code=is_control_code,
            payee=payee,
        )

        return pay_code
