import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.employment_details import EmploymentDetails
from ..models.item import Item
from ..models.national_insurance_calculation import NationalInsuranceCalculation
from ..models.pay_options import PayOptions
from ..models.pay_periods import PayPeriods
from ..models.pay_run_state import PayRunState
from ..models.pay_run_totals import PayRunTotals
from ..models.pension_summary import PensionSummary
from ..models.personal_details import PersonalDetails
from ..models.tax_year import TaxYear
from ..models.umbrella_payment import UmbrellaPayment
from ..models.value_override import ValueOverride
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunEntry")


@attr.s(auto_attribs=True)
class PayRunEntry:
    """A PayRun contains multiple PayRunEntries, one for each Employee that is being paid.
    The value for <code>PersonalDetails</code> and <code>EmploymentDetails</code> is copied from the Employee record.
    So to change them you should update the Employee, not the PayRunEntry.
    Changes made to the Employee are only reflected whilst the PayRun is still open.
    Once you finalise and close the PayRun then a snapshot is taken of these values which is stored with the PayRunEntry
    for future reference.

        Attributes:
            tax_year (Union[Unset, TaxYear]):
            tax_month (Union[Unset, int]): [readonly] The Tax Month that the Payment Date falls in
            start_date (Union[Unset, datetime.date]): [readonly]
            end_date (Union[Unset, datetime.date]): [readonly]
            note (Union[Unset, None, str]): Any note that you'd like to appear on the payslip
            bacs_sub_reference (Union[Unset, None, str]): [readonly] A randomly generated string for use with the RTI Hash
                Cross Reference
            bacs_hash_code (Union[Unset, None, str]): [readonly] A Hash Code used for RTI BACS Hash Cross Reference
            percentage_of_working_days_paid_as_normal (Union[Unset, float]): [readonly] If the employee is paid a set amount
                per period (ie, not an hourly or daily rate) and there is any Leave that is either Not Paid or Statutory Pay
                then this value
                will give the percentage of working days (based on the Working Pattern) that should be paid as normal.
                If there is no Leave in the period or PayOptions.AutoAdjustForLeave is false, then this will be 1.
            working_days_not_paid_as_normal (Union[Unset, float]): [readonly] If PercentageOfWorkingDaysPaidAsNormal has a
                value other than 1
                then this property will tell you how many working days have been deducted from the basic pay
                due to either being Not Paid or Statutory Pay
            pay_period (Union[Unset, PayPeriods]):
            ordinal (Union[Unset, int]): [readonly] Indicates whether this uses the first, second, third (etc) PaySchedule
                for this PayPeriod.
            period (Union[Unset, int]): [readonly] The Tax Week or Tax Month number this PayRunEntry relates to
            is_new_starter (Union[Unset, bool]): Determines whether or not this Employee will be declared as a new starter
                on the resulting FPS
            unpaid_absence (Union[Unset, bool]): [readonly] Indicates that there was unpaid absence in the pay period
            has_attachment_orders (Union[Unset, bool]): [readonly] Indicates that there are AttachmentOrders for this
                Employee in this entry
            payment_date (Union[Unset, datetime.date]): The date this payment was or will be made
            prior_payroll_code (Union[Unset, None, str]): [readonly] If the FPS needs to declare a change of PayId then this
                will contain the previous code
                It's worked out automatically but can also be set from the Employees EmploymentDetails property.
            pension_summary (Union[Unset, PensionSummary]): If a PayRunEntry contains pension contributions then it'll also
                include a PensionSummary model
                giving further information about the Pension Scheme and the contributions made
            employee (Union[Unset, Item]):
            totals (Union[Unset, PayRunTotals]): Used to represent totals for a PayRun or PayRunEntry.
                If a value is 0 then it will not be shown in the JSON.
            period_overrides (Union[Unset, None, List[ValueOverride]]): Any calculated values for this period that should be
                overridden with a different value
            totals_ytd (Union[Unset, PayRunTotals]): Used to represent totals for a PayRun or PayRunEntry.
                If a value is 0 then it will not be shown in the JSON.
            totals_ytd_overrides (Union[Unset, None, List[ValueOverride]]): Any values of TotalsYtd that should be
                overridden with a different value
            forced_cis_vat_amount (Union[Unset, None, float]): If this employee is a CIS Subcontractor registered for VAT,
                we'll automatically work out VAT at the set rate.
                If you want to override this calculations then set this property to anything other than null.
            holiday_accrued (Union[Unset, float]): The amount of holiday days accrued in the period.
            state (Union[Unset, PayRunState]): The state of the payrun. You would set this value when updating a payrun to
                finalise or re-open it.
                Other states are used with Bureau functionality which isn't currently generally available.
            is_closed (Union[Unset, bool]): [readonly] Set to True if the PayRun is Finalised and changes can no longer be
                made to the PayRunEntries
            manual_ni (Union[Unset, bool]): If set to true then you must provide your own value for
                NationalInsuranceCalculation.
                You'd normally leave this set to false and let us automatically calculate NI amounts.
            national_insurance_calculation (Union[Unset, NationalInsuranceCalculation]): Included as part of the PayRunEntry
                model to provide details of how the National Insurance Contribution was calculated.
                Unless the PayRunEntry.ManualNi property is set to true then these value will all be read-only and are
                recalculated everytime a payrun is updated.
                This calculation could be made up of one or more calculations made on different NI table letters.
                Where more than NI table letter affects the calculation, the calculation for each NI table letter will be
                contain in the Breakdown.
            payroll_code_changed (Union[Unset, bool]): [readonly] Indicates whether or not the Payroll Code for this
                Employee has changed since the last FPS
            ae_not_enroled_warning (Union[Unset, bool]): [readonly] If true then this Employee needs to be on an Auto
                Enrolment pension but isn't yet.
            fps (Union[Unset, Item]):
            email_id (Union[Unset, None, str]): If the Payslip for this PayRunEntry has been emailed to the employee then
                the Id for an EmployerEmail will be provided here.
                if the value is all zeroes then the email is in the process of being created.
            recieving_offset_pay (Union[Unset, bool]): If the pay is being topped up due to an applied Leave having the
                offset value set to true then
                this will be set to true
            payment_after_leaving (Union[Unset, bool]): [readonly] If this payment is for an employee that has left then
                this is set to true.
            umbrella_payment (Union[Unset, UmbrellaPayment]):
            id (Union[Unset, str]): [readonly] The unique id of the object
            personal_details (Union[Unset, PersonalDetails]):
            employment_details (Union[Unset, EmploymentDetails]):
            pay_options (Union[Unset, PayOptions]): This object forms the basis of the Employees payment.
    """

    tax_year: Union[Unset, TaxYear] = UNSET
    tax_month: Union[Unset, int] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    end_date: Union[Unset, datetime.date] = UNSET
    note: Union[Unset, None, str] = UNSET
    bacs_sub_reference: Union[Unset, None, str] = UNSET
    bacs_hash_code: Union[Unset, None, str] = UNSET
    percentage_of_working_days_paid_as_normal: Union[Unset, float] = UNSET
    working_days_not_paid_as_normal: Union[Unset, float] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET
    is_new_starter: Union[Unset, bool] = UNSET
    unpaid_absence: Union[Unset, bool] = UNSET
    has_attachment_orders: Union[Unset, bool] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET
    prior_payroll_code: Union[Unset, None, str] = UNSET
    pension_summary: Union[Unset, PensionSummary] = UNSET
    employee: Union[Unset, Item] = UNSET
    totals: Union[Unset, PayRunTotals] = UNSET
    period_overrides: Union[Unset, None, List[ValueOverride]] = UNSET
    totals_ytd: Union[Unset, PayRunTotals] = UNSET
    totals_ytd_overrides: Union[Unset, None, List[ValueOverride]] = UNSET
    forced_cis_vat_amount: Union[Unset, None, float] = UNSET
    holiday_accrued: Union[Unset, float] = UNSET
    state: Union[Unset, PayRunState] = UNSET
    is_closed: Union[Unset, bool] = UNSET
    manual_ni: Union[Unset, bool] = UNSET
    national_insurance_calculation: Union[Unset, NationalInsuranceCalculation] = UNSET
    payroll_code_changed: Union[Unset, bool] = UNSET
    ae_not_enroled_warning: Union[Unset, bool] = UNSET
    fps: Union[Unset, Item] = UNSET
    email_id: Union[Unset, None, str] = UNSET
    recieving_offset_pay: Union[Unset, bool] = UNSET
    payment_after_leaving: Union[Unset, bool] = UNSET
    umbrella_payment: Union[Unset, UmbrellaPayment] = UNSET
    id: Union[Unset, str] = UNSET
    personal_details: Union[Unset, PersonalDetails] = UNSET
    employment_details: Union[Unset, EmploymentDetails] = UNSET
    pay_options: Union[Unset, PayOptions] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        tax_month = self.tax_month
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        note = self.note
        bacs_sub_reference = self.bacs_sub_reference
        bacs_hash_code = self.bacs_hash_code
        percentage_of_working_days_paid_as_normal = (
            self.percentage_of_working_days_paid_as_normal
        )
        working_days_not_paid_as_normal = self.working_days_not_paid_as_normal
        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period
        is_new_starter = self.is_new_starter
        unpaid_absence = self.unpaid_absence
        has_attachment_orders = self.has_attachment_orders
        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()

        prior_payroll_code = self.prior_payroll_code
        pension_summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pension_summary, Unset):
            pension_summary = self.pension_summary.to_dict()

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        totals: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals, Unset):
            totals = self.totals.to_dict()

        period_overrides: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.period_overrides, Unset):
            if self.period_overrides is None:
                period_overrides = None
            else:
                period_overrides = []
                for period_overrides_item_data in self.period_overrides:
                    period_overrides_item = period_overrides_item_data.to_dict()

                    period_overrides.append(period_overrides_item)

        totals_ytd: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals_ytd, Unset):
            totals_ytd = self.totals_ytd.to_dict()

        totals_ytd_overrides: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.totals_ytd_overrides, Unset):
            if self.totals_ytd_overrides is None:
                totals_ytd_overrides = None
            else:
                totals_ytd_overrides = []
                for totals_ytd_overrides_item_data in self.totals_ytd_overrides:
                    totals_ytd_overrides_item = totals_ytd_overrides_item_data.to_dict()

                    totals_ytd_overrides.append(totals_ytd_overrides_item)

        forced_cis_vat_amount = self.forced_cis_vat_amount
        holiday_accrued = self.holiday_accrued
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        is_closed = self.is_closed
        manual_ni = self.manual_ni
        national_insurance_calculation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.national_insurance_calculation, Unset):
            national_insurance_calculation = (
                self.national_insurance_calculation.to_dict()
            )

        payroll_code_changed = self.payroll_code_changed
        ae_not_enroled_warning = self.ae_not_enroled_warning
        fps: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fps, Unset):
            fps = self.fps.to_dict()

        email_id = self.email_id
        recieving_offset_pay = self.recieving_offset_pay
        payment_after_leaving = self.payment_after_leaving
        umbrella_payment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.umbrella_payment, Unset):
            umbrella_payment = self.umbrella_payment.to_dict()

        id = self.id
        personal_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.personal_details, Unset):
            personal_details = self.personal_details.to_dict()

        employment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employment_details, Unset):
            employment_details = self.employment_details.to_dict()

        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if tax_month is not UNSET:
            field_dict["taxMonth"] = tax_month
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if note is not UNSET:
            field_dict["note"] = note
        if bacs_sub_reference is not UNSET:
            field_dict["bacsSubReference"] = bacs_sub_reference
        if bacs_hash_code is not UNSET:
            field_dict["bacsHashCode"] = bacs_hash_code
        if percentage_of_working_days_paid_as_normal is not UNSET:
            field_dict[
                "percentageOfWorkingDaysPaidAsNormal"
            ] = percentage_of_working_days_paid_as_normal
        if working_days_not_paid_as_normal is not UNSET:
            field_dict["workingDaysNotPaidAsNormal"] = working_days_not_paid_as_normal
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period
        if is_new_starter is not UNSET:
            field_dict["isNewStarter"] = is_new_starter
        if unpaid_absence is not UNSET:
            field_dict["unpaidAbsence"] = unpaid_absence
        if has_attachment_orders is not UNSET:
            field_dict["hasAttachmentOrders"] = has_attachment_orders
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if prior_payroll_code is not UNSET:
            field_dict["priorPayrollCode"] = prior_payroll_code
        if pension_summary is not UNSET:
            field_dict["pensionSummary"] = pension_summary
        if employee is not UNSET:
            field_dict["employee"] = employee
        if totals is not UNSET:
            field_dict["totals"] = totals
        if period_overrides is not UNSET:
            field_dict["periodOverrides"] = period_overrides
        if totals_ytd is not UNSET:
            field_dict["totalsYtd"] = totals_ytd
        if totals_ytd_overrides is not UNSET:
            field_dict["totalsYtdOverrides"] = totals_ytd_overrides
        if forced_cis_vat_amount is not UNSET:
            field_dict["forcedCisVatAmount"] = forced_cis_vat_amount
        if holiday_accrued is not UNSET:
            field_dict["holidayAccrued"] = holiday_accrued
        if state is not UNSET:
            field_dict["state"] = state
        if is_closed is not UNSET:
            field_dict["isClosed"] = is_closed
        if manual_ni is not UNSET:
            field_dict["manualNi"] = manual_ni
        if national_insurance_calculation is not UNSET:
            field_dict["nationalInsuranceCalculation"] = national_insurance_calculation
        if payroll_code_changed is not UNSET:
            field_dict["payrollCodeChanged"] = payroll_code_changed
        if ae_not_enroled_warning is not UNSET:
            field_dict["aeNotEnroledWarning"] = ae_not_enroled_warning
        if fps is not UNSET:
            field_dict["fps"] = fps
        if email_id is not UNSET:
            field_dict["emailId"] = email_id
        if recieving_offset_pay is not UNSET:
            field_dict["recievingOffsetPay"] = recieving_offset_pay
        if payment_after_leaving is not UNSET:
            field_dict["paymentAfterLeaving"] = payment_after_leaving
        if umbrella_payment is not UNSET:
            field_dict["umbrellaPayment"] = umbrella_payment
        if id is not UNSET:
            field_dict["id"] = id
        if personal_details is not UNSET:
            field_dict["personalDetails"] = personal_details
        if employment_details is not UNSET:
            field_dict["employmentDetails"] = employment_details
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options

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

        tax_month = d.pop("taxMonth", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.date]
        if isinstance(_start_date, Unset):
            start_date = UNSET
        else:
            start_date = isoparse(_start_date).date()

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.date]
        if isinstance(_end_date, Unset):
            end_date = UNSET
        else:
            end_date = isoparse(_end_date).date()

        note = d.pop("note", UNSET)

        bacs_sub_reference = d.pop("bacsSubReference", UNSET)

        bacs_hash_code = d.pop("bacsHashCode", UNSET)

        percentage_of_working_days_paid_as_normal = d.pop(
            "percentageOfWorkingDaysPaidAsNormal", UNSET
        )

        working_days_not_paid_as_normal = d.pop("workingDaysNotPaidAsNormal", UNSET)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

        is_new_starter = d.pop("isNewStarter", UNSET)

        unpaid_absence = d.pop("unpaidAbsence", UNSET)

        has_attachment_orders = d.pop("hasAttachmentOrders", UNSET)

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

        prior_payroll_code = d.pop("priorPayrollCode", UNSET)

        _pension_summary = d.pop("pensionSummary", UNSET)
        pension_summary: Union[Unset, PensionSummary]
        if isinstance(_pension_summary, Unset):
            pension_summary = UNSET
        else:
            pension_summary = PensionSummary.from_dict(_pension_summary)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        _totals = d.pop("totals", UNSET)
        totals: Union[Unset, PayRunTotals]
        if isinstance(_totals, Unset):
            totals = UNSET
        else:
            totals = PayRunTotals.from_dict(_totals)

        period_overrides = []
        _period_overrides = d.pop("periodOverrides", UNSET)
        for period_overrides_item_data in _period_overrides or []:
            period_overrides_item = ValueOverride.from_dict(period_overrides_item_data)

            period_overrides.append(period_overrides_item)

        _totals_ytd = d.pop("totalsYtd", UNSET)
        totals_ytd: Union[Unset, PayRunTotals]
        if isinstance(_totals_ytd, Unset):
            totals_ytd = UNSET
        else:
            totals_ytd = PayRunTotals.from_dict(_totals_ytd)

        totals_ytd_overrides = []
        _totals_ytd_overrides = d.pop("totalsYtdOverrides", UNSET)
        for totals_ytd_overrides_item_data in _totals_ytd_overrides or []:
            totals_ytd_overrides_item = ValueOverride.from_dict(
                totals_ytd_overrides_item_data
            )

            totals_ytd_overrides.append(totals_ytd_overrides_item)

        forced_cis_vat_amount = d.pop("forcedCisVatAmount", UNSET)

        holiday_accrued = d.pop("holidayAccrued", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, PayRunState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = PayRunState(_state)

        is_closed = d.pop("isClosed", UNSET)

        manual_ni = d.pop("manualNi", UNSET)

        _national_insurance_calculation = d.pop("nationalInsuranceCalculation", UNSET)
        national_insurance_calculation: Union[Unset, NationalInsuranceCalculation]
        if isinstance(_national_insurance_calculation, Unset):
            national_insurance_calculation = UNSET
        else:
            national_insurance_calculation = NationalInsuranceCalculation.from_dict(
                _national_insurance_calculation
            )

        payroll_code_changed = d.pop("payrollCodeChanged", UNSET)

        ae_not_enroled_warning = d.pop("aeNotEnroledWarning", UNSET)

        _fps = d.pop("fps", UNSET)
        fps: Union[Unset, Item]
        if isinstance(_fps, Unset):
            fps = UNSET
        else:
            fps = Item.from_dict(_fps)

        email_id = d.pop("emailId", UNSET)

        recieving_offset_pay = d.pop("recievingOffsetPay", UNSET)

        payment_after_leaving = d.pop("paymentAfterLeaving", UNSET)

        _umbrella_payment = d.pop("umbrellaPayment", UNSET)
        umbrella_payment: Union[Unset, UmbrellaPayment]
        if isinstance(_umbrella_payment, Unset):
            umbrella_payment = UNSET
        else:
            umbrella_payment = UmbrellaPayment.from_dict(_umbrella_payment)

        id = d.pop("id", UNSET)

        _personal_details = d.pop("personalDetails", UNSET)
        personal_details: Union[Unset, PersonalDetails]
        if isinstance(_personal_details, Unset):
            personal_details = UNSET
        else:
            personal_details = PersonalDetails.from_dict(_personal_details)

        _employment_details = d.pop("employmentDetails", UNSET)
        employment_details: Union[Unset, EmploymentDetails]
        if isinstance(_employment_details, Unset):
            employment_details = UNSET
        else:
            employment_details = EmploymentDetails.from_dict(_employment_details)

        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, PayOptions]
        if isinstance(_pay_options, Unset):
            pay_options = UNSET
        else:
            pay_options = PayOptions.from_dict(_pay_options)

        pay_run_entry = cls(
            tax_year=tax_year,
            tax_month=tax_month,
            start_date=start_date,
            end_date=end_date,
            note=note,
            bacs_sub_reference=bacs_sub_reference,
            bacs_hash_code=bacs_hash_code,
            percentage_of_working_days_paid_as_normal=percentage_of_working_days_paid_as_normal,
            working_days_not_paid_as_normal=working_days_not_paid_as_normal,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
            is_new_starter=is_new_starter,
            unpaid_absence=unpaid_absence,
            has_attachment_orders=has_attachment_orders,
            payment_date=payment_date,
            prior_payroll_code=prior_payroll_code,
            pension_summary=pension_summary,
            employee=employee,
            totals=totals,
            period_overrides=period_overrides,
            totals_ytd=totals_ytd,
            totals_ytd_overrides=totals_ytd_overrides,
            forced_cis_vat_amount=forced_cis_vat_amount,
            holiday_accrued=holiday_accrued,
            state=state,
            is_closed=is_closed,
            manual_ni=manual_ni,
            national_insurance_calculation=national_insurance_calculation,
            payroll_code_changed=payroll_code_changed,
            ae_not_enroled_warning=ae_not_enroled_warning,
            fps=fps,
            email_id=email_id,
            recieving_offset_pay=recieving_offset_pay,
            payment_after_leaving=payment_after_leaving,
            umbrella_payment=umbrella_payment,
            id=id,
            personal_details=personal_details,
            employment_details=employment_details,
            pay_options=pay_options,
        )

        return pay_run_entry
