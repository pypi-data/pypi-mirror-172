import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.holiday_type import HolidayType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LeaveSettings")


@attr.s(auto_attribs=True)
class LeaveSettings:
    """
    Attributes:
        use_default_holiday_type (Union[Unset, bool]): If true then the value for HolidayType comes from the Employer
            record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_allowance_reset_date (Union[Unset, bool]): If true then the value for the AllowanceResetDate comes
            from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_allowance (Union[Unset, bool]): If true then the value for the Allowance comes from the Employer
            record.
            This property only appears if the LeaveSettings if a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu (Union[Unset, bool]): If true then the value for AccruePaymentInLieu comes
            from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_rate (Union[Unset, bool]): If true then the value for AccruePaymentInLieuRate
            comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_all_gross_pay (Union[Unset, bool]): If true then the value for
            AccruePaymentInLieuAllGrossPay comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_payment_in_lieu_pay_automatically (Union[Unset, bool]): If true then the value for
            AccruePaymentInLieu comes from the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        use_default_accrue_hours_per_day (Union[Unset, bool]): If true then the value for AccrueHoursPerDay comes from
            the Employer record.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        allowance_reset_date (Union[Unset, datetime.date]): The date that the holiday allowance resets. Only the
            day/month part of the value is relevant.
        allowance (Union[Unset, float]): The number of days holiday an employee can take per year if HolidayType is
            Days.
            Otherwise this is readonly and gives you the number of days accrued since the last reset
        adjustment (Union[Unset, None, float]): Adjustment to number of hours/days/weeks holiday this employee can take
            per year.
            Will reset to 0 when the Allowance resets.
            This property only appears if the LeaveSettings is a child of an Employee (not of an Employer)
        allowance_used (Union[Unset, float]): [readonly] The number of days used from the allowance since last reset
        allowance_used_previous_period (Union[Unset, float]): [readonly] The number of days used in the 12 months prior
            to the last reset
        allowance_remaining (Union[Unset, float]): [readonly] The number of days remaining of the allowance until next
            reset
        holiday_type (Union[Unset, HolidayType]):
        accrue_set_amount (Union[Unset, bool]): If true and HolidayType is Accrual_Days then the AccruePaymentInLieuRate
            will be treated as the set amount to accrue per period worked.
        accrue_hours_per_day (Union[Unset, float]): If HolidayType is Accrual_Days then this value is used to help
            convert hours worked into days accrued
        show_allowance_on_payslip (Union[Unset, bool]): If true then the remaining Allowance will be shown on the
            employees payslip.
        show_ahp_on_payslip (Union[Unset, bool]): If true then the AHP balance will be shown on the employees payslip.
        accrue_payment_in_lieu_rate (Union[Unset, float]): The rate at which Payments in Lieu acrrue. Typically this
            should be 12.07%.
        accrue_payment_in_lieu_all_gross_pay (Union[Unset, bool]): Set to true if you want accrued holiday payments to
            be calculated on the total gross pay for the employee or just on the single regular pay element
        accrue_payment_in_lieu_pay_automatically (Union[Unset, bool]): Set to true if you want employees to be
            automatically paid any outstanding holiday pay
        accrued_payment_liability (Union[Unset, float]): [readonly] The total accrued payments for this employee over
            the lifetime of their employment so far
        accrued_payment_adjustment (Union[Unset, float]): Any manual adjustment to the total accrued
        accrued_payment_paid (Union[Unset, float]): [readonly] The Total amount paid to this employee in lieu of
            holidays
        accrued_payment_balance (Union[Unset, float]): [readonly] The balance of what is owed to this employee in lieu
            of holidays
    """

    use_default_holiday_type: Union[Unset, bool] = UNSET
    use_default_allowance_reset_date: Union[Unset, bool] = UNSET
    use_default_allowance: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_rate: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_all_gross_pay: Union[Unset, bool] = UNSET
    use_default_accrue_payment_in_lieu_pay_automatically: Union[Unset, bool] = UNSET
    use_default_accrue_hours_per_day: Union[Unset, bool] = UNSET
    allowance_reset_date: Union[Unset, datetime.date] = UNSET
    allowance: Union[Unset, float] = UNSET
    adjustment: Union[Unset, None, float] = UNSET
    allowance_used: Union[Unset, float] = UNSET
    allowance_used_previous_period: Union[Unset, float] = UNSET
    allowance_remaining: Union[Unset, float] = UNSET
    holiday_type: Union[Unset, HolidayType] = UNSET
    accrue_set_amount: Union[Unset, bool] = UNSET
    accrue_hours_per_day: Union[Unset, float] = UNSET
    show_allowance_on_payslip: Union[Unset, bool] = UNSET
    show_ahp_on_payslip: Union[Unset, bool] = UNSET
    accrue_payment_in_lieu_rate: Union[Unset, float] = UNSET
    accrue_payment_in_lieu_all_gross_pay: Union[Unset, bool] = UNSET
    accrue_payment_in_lieu_pay_automatically: Union[Unset, bool] = UNSET
    accrued_payment_liability: Union[Unset, float] = UNSET
    accrued_payment_adjustment: Union[Unset, float] = UNSET
    accrued_payment_paid: Union[Unset, float] = UNSET
    accrued_payment_balance: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        use_default_holiday_type = self.use_default_holiday_type
        use_default_allowance_reset_date = self.use_default_allowance_reset_date
        use_default_allowance = self.use_default_allowance
        use_default_accrue_payment_in_lieu = self.use_default_accrue_payment_in_lieu
        use_default_accrue_payment_in_lieu_rate = (
            self.use_default_accrue_payment_in_lieu_rate
        )
        use_default_accrue_payment_in_lieu_all_gross_pay = (
            self.use_default_accrue_payment_in_lieu_all_gross_pay
        )
        use_default_accrue_payment_in_lieu_pay_automatically = (
            self.use_default_accrue_payment_in_lieu_pay_automatically
        )
        use_default_accrue_hours_per_day = self.use_default_accrue_hours_per_day
        allowance_reset_date: Union[Unset, str] = UNSET
        if not isinstance(self.allowance_reset_date, Unset):
            allowance_reset_date = self.allowance_reset_date.isoformat()

        allowance = self.allowance
        adjustment = self.adjustment
        allowance_used = self.allowance_used
        allowance_used_previous_period = self.allowance_used_previous_period
        allowance_remaining = self.allowance_remaining
        holiday_type: Union[Unset, str] = UNSET
        if not isinstance(self.holiday_type, Unset):
            holiday_type = self.holiday_type.value

        accrue_set_amount = self.accrue_set_amount
        accrue_hours_per_day = self.accrue_hours_per_day
        show_allowance_on_payslip = self.show_allowance_on_payslip
        show_ahp_on_payslip = self.show_ahp_on_payslip
        accrue_payment_in_lieu_rate = self.accrue_payment_in_lieu_rate
        accrue_payment_in_lieu_all_gross_pay = self.accrue_payment_in_lieu_all_gross_pay
        accrue_payment_in_lieu_pay_automatically = (
            self.accrue_payment_in_lieu_pay_automatically
        )
        accrued_payment_liability = self.accrued_payment_liability
        accrued_payment_adjustment = self.accrued_payment_adjustment
        accrued_payment_paid = self.accrued_payment_paid
        accrued_payment_balance = self.accrued_payment_balance

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if use_default_holiday_type is not UNSET:
            field_dict["useDefaultHolidayType"] = use_default_holiday_type
        if use_default_allowance_reset_date is not UNSET:
            field_dict[
                "useDefaultAllowanceResetDate"
            ] = use_default_allowance_reset_date
        if use_default_allowance is not UNSET:
            field_dict["useDefaultAllowance"] = use_default_allowance
        if use_default_accrue_payment_in_lieu is not UNSET:
            field_dict[
                "useDefaultAccruePaymentInLieu"
            ] = use_default_accrue_payment_in_lieu
        if use_default_accrue_payment_in_lieu_rate is not UNSET:
            field_dict[
                "useDefaultAccruePaymentInLieuRate"
            ] = use_default_accrue_payment_in_lieu_rate
        if use_default_accrue_payment_in_lieu_all_gross_pay is not UNSET:
            field_dict[
                "useDefaultAccruePaymentInLieuAllGrossPay"
            ] = use_default_accrue_payment_in_lieu_all_gross_pay
        if use_default_accrue_payment_in_lieu_pay_automatically is not UNSET:
            field_dict[
                "useDefaultAccruePaymentInLieuPayAutomatically"
            ] = use_default_accrue_payment_in_lieu_pay_automatically
        if use_default_accrue_hours_per_day is not UNSET:
            field_dict["useDefaultAccrueHoursPerDay"] = use_default_accrue_hours_per_day
        if allowance_reset_date is not UNSET:
            field_dict["allowanceResetDate"] = allowance_reset_date
        if allowance is not UNSET:
            field_dict["allowance"] = allowance
        if adjustment is not UNSET:
            field_dict["adjustment"] = adjustment
        if allowance_used is not UNSET:
            field_dict["allowanceUsed"] = allowance_used
        if allowance_used_previous_period is not UNSET:
            field_dict["allowanceUsedPreviousPeriod"] = allowance_used_previous_period
        if allowance_remaining is not UNSET:
            field_dict["allowanceRemaining"] = allowance_remaining
        if holiday_type is not UNSET:
            field_dict["holidayType"] = holiday_type
        if accrue_set_amount is not UNSET:
            field_dict["accrueSetAmount"] = accrue_set_amount
        if accrue_hours_per_day is not UNSET:
            field_dict["accrueHoursPerDay"] = accrue_hours_per_day
        if show_allowance_on_payslip is not UNSET:
            field_dict["showAllowanceOnPayslip"] = show_allowance_on_payslip
        if show_ahp_on_payslip is not UNSET:
            field_dict["showAhpOnPayslip"] = show_ahp_on_payslip
        if accrue_payment_in_lieu_rate is not UNSET:
            field_dict["accruePaymentInLieuRate"] = accrue_payment_in_lieu_rate
        if accrue_payment_in_lieu_all_gross_pay is not UNSET:
            field_dict[
                "accruePaymentInLieuAllGrossPay"
            ] = accrue_payment_in_lieu_all_gross_pay
        if accrue_payment_in_lieu_pay_automatically is not UNSET:
            field_dict[
                "accruePaymentInLieuPayAutomatically"
            ] = accrue_payment_in_lieu_pay_automatically
        if accrued_payment_liability is not UNSET:
            field_dict["accruedPaymentLiability"] = accrued_payment_liability
        if accrued_payment_adjustment is not UNSET:
            field_dict["accruedPaymentAdjustment"] = accrued_payment_adjustment
        if accrued_payment_paid is not UNSET:
            field_dict["accruedPaymentPaid"] = accrued_payment_paid
        if accrued_payment_balance is not UNSET:
            field_dict["accruedPaymentBalance"] = accrued_payment_balance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        use_default_holiday_type = d.pop("useDefaultHolidayType", UNSET)

        use_default_allowance_reset_date = d.pop("useDefaultAllowanceResetDate", UNSET)

        use_default_allowance = d.pop("useDefaultAllowance", UNSET)

        use_default_accrue_payment_in_lieu = d.pop(
            "useDefaultAccruePaymentInLieu", UNSET
        )

        use_default_accrue_payment_in_lieu_rate = d.pop(
            "useDefaultAccruePaymentInLieuRate", UNSET
        )

        use_default_accrue_payment_in_lieu_all_gross_pay = d.pop(
            "useDefaultAccruePaymentInLieuAllGrossPay", UNSET
        )

        use_default_accrue_payment_in_lieu_pay_automatically = d.pop(
            "useDefaultAccruePaymentInLieuPayAutomatically", UNSET
        )

        use_default_accrue_hours_per_day = d.pop("useDefaultAccrueHoursPerDay", UNSET)

        _allowance_reset_date = d.pop("allowanceResetDate", UNSET)
        allowance_reset_date: Union[Unset, datetime.date]
        if isinstance(_allowance_reset_date, Unset):
            allowance_reset_date = UNSET
        else:
            allowance_reset_date = isoparse(_allowance_reset_date).date()

        allowance = d.pop("allowance", UNSET)

        adjustment = d.pop("adjustment", UNSET)

        allowance_used = d.pop("allowanceUsed", UNSET)

        allowance_used_previous_period = d.pop("allowanceUsedPreviousPeriod", UNSET)

        allowance_remaining = d.pop("allowanceRemaining", UNSET)

        _holiday_type = d.pop("holidayType", UNSET)
        holiday_type: Union[Unset, HolidayType]
        if isinstance(_holiday_type, Unset):
            holiday_type = UNSET
        else:
            holiday_type = HolidayType(_holiday_type)

        accrue_set_amount = d.pop("accrueSetAmount", UNSET)

        accrue_hours_per_day = d.pop("accrueHoursPerDay", UNSET)

        show_allowance_on_payslip = d.pop("showAllowanceOnPayslip", UNSET)

        show_ahp_on_payslip = d.pop("showAhpOnPayslip", UNSET)

        accrue_payment_in_lieu_rate = d.pop("accruePaymentInLieuRate", UNSET)

        accrue_payment_in_lieu_all_gross_pay = d.pop(
            "accruePaymentInLieuAllGrossPay", UNSET
        )

        accrue_payment_in_lieu_pay_automatically = d.pop(
            "accruePaymentInLieuPayAutomatically", UNSET
        )

        accrued_payment_liability = d.pop("accruedPaymentLiability", UNSET)

        accrued_payment_adjustment = d.pop("accruedPaymentAdjustment", UNSET)

        accrued_payment_paid = d.pop("accruedPaymentPaid", UNSET)

        accrued_payment_balance = d.pop("accruedPaymentBalance", UNSET)

        leave_settings = cls(
            use_default_holiday_type=use_default_holiday_type,
            use_default_allowance_reset_date=use_default_allowance_reset_date,
            use_default_allowance=use_default_allowance,
            use_default_accrue_payment_in_lieu=use_default_accrue_payment_in_lieu,
            use_default_accrue_payment_in_lieu_rate=use_default_accrue_payment_in_lieu_rate,
            use_default_accrue_payment_in_lieu_all_gross_pay=use_default_accrue_payment_in_lieu_all_gross_pay,
            use_default_accrue_payment_in_lieu_pay_automatically=use_default_accrue_payment_in_lieu_pay_automatically,
            use_default_accrue_hours_per_day=use_default_accrue_hours_per_day,
            allowance_reset_date=allowance_reset_date,
            allowance=allowance,
            adjustment=adjustment,
            allowance_used=allowance_used,
            allowance_used_previous_period=allowance_used_previous_period,
            allowance_remaining=allowance_remaining,
            holiday_type=holiday_type,
            accrue_set_amount=accrue_set_amount,
            accrue_hours_per_day=accrue_hours_per_day,
            show_allowance_on_payslip=show_allowance_on_payslip,
            show_ahp_on_payslip=show_ahp_on_payslip,
            accrue_payment_in_lieu_rate=accrue_payment_in_lieu_rate,
            accrue_payment_in_lieu_all_gross_pay=accrue_payment_in_lieu_all_gross_pay,
            accrue_payment_in_lieu_pay_automatically=accrue_payment_in_lieu_pay_automatically,
            accrued_payment_liability=accrued_payment_liability,
            accrued_payment_adjustment=accrued_payment_adjustment,
            accrued_payment_paid=accrued_payment_paid,
            accrued_payment_balance=accrued_payment_balance,
        )

        return leave_settings
