from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.auto_pilot_finalise_time import AutoPilotFinaliseTime
from ..models.payrun_email import PayrunEmail
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationSettings")


@attr.s(auto_attribs=True)
class AutomationSettings:
    """Configures various automation settings for an Employer

    Attributes:
        enable_auto_pilot (Union[Unset, bool]): IF enabled then payruns will be automatically finalised on the payment
            date and the next payrun will be started
        auto_pilot_time (Union[Unset, AutoPilotFinaliseTime]):
        auto_pilot_offset (Union[Unset, int]): How many days before the payment date a payrun should be finalised.
            Set it to 0 if you want the payrun to be automatically finalised on the payment date itself
        enable_auto_open (Union[Unset, bool]): IF enabled then whenever you close a payrun, the next one will be
            started. Automatically set to true if EnableAutoPilot is true
        auto_submit_fps (Union[Unset, bool]): If set to true, we'll automatically send your FPS to HMRC whenever you
            finalise a PayRun.
            This property will always have the same value as the property with the same name on the RtiSubmissionSettings
            model.
        auto_submit_payments (Union[Unset, bool]): If set to true, we'll automatically submit payments whenever you
            finalise a PayRun.
            The employer must be connected to an ExternalDataProvider supporting Type of 'Payments'.
        auto_submit_journal (Union[Unset, bool]): If set to true, we'll automatically submit the payroll journal
            whenever you finalise a PayRun.
            The employer must be connected to an ExternalDataProvider supporting Type of 'Accounting'.
        auto_submit_payments_employee (Union[Unset, bool]): Used in conjunction with AutoSubmitPayments.
        auto_submit_payments_hmrc (Union[Unset, bool]): Used in conjunction with AutoSubmitPayments.
        auto_submit_payments_deductions (Union[Unset, bool]): Used in conjunction with AutoSubmitPayments.
        auto_submit_payments_aeos (Union[Unset, bool]): Used in conjunction with AutoSubmitPayments.
        auto_submit_payments_pensions (Union[Unset, bool]): Used in conjunction with AutoSubmitPayments.
        employees_without_email_address (Union[Unset, int]): [readonly] A count of how many employees or subcontractors
            for this employer do not have email addresses
        employees_with_email_address_but_not_auto_sending (Union[Unset, int]): [readonly] A count of how many employees
            or subcontractors for this employer do have email addresses but don't have the option enabled to auto-email
            payslips
        subcontractors_not_auto_sending_statement (Union[Unset, int]): [readonly] A count of how many subscontractors
            for this employer do don't have the option enabled to auto-email statement
        coding_notices_automatically_applied (Union[Unset, bool]): [readonly] An indicator of whether or not this
            employer is automatically applying DpsNotices
        payrun_emails (Union[Unset, None, List[PayrunEmail]]): Automated emails that will be sent when a PayRun is
            finalised
    """

    enable_auto_pilot: Union[Unset, bool] = UNSET
    auto_pilot_time: Union[Unset, AutoPilotFinaliseTime] = UNSET
    auto_pilot_offset: Union[Unset, int] = UNSET
    enable_auto_open: Union[Unset, bool] = UNSET
    auto_submit_fps: Union[Unset, bool] = UNSET
    auto_submit_payments: Union[Unset, bool] = UNSET
    auto_submit_journal: Union[Unset, bool] = UNSET
    auto_submit_payments_employee: Union[Unset, bool] = UNSET
    auto_submit_payments_hmrc: Union[Unset, bool] = UNSET
    auto_submit_payments_deductions: Union[Unset, bool] = UNSET
    auto_submit_payments_aeos: Union[Unset, bool] = UNSET
    auto_submit_payments_pensions: Union[Unset, bool] = UNSET
    employees_without_email_address: Union[Unset, int] = UNSET
    employees_with_email_address_but_not_auto_sending: Union[Unset, int] = UNSET
    subcontractors_not_auto_sending_statement: Union[Unset, int] = UNSET
    coding_notices_automatically_applied: Union[Unset, bool] = UNSET
    payrun_emails: Union[Unset, None, List[PayrunEmail]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enable_auto_pilot = self.enable_auto_pilot
        auto_pilot_time: Union[Unset, str] = UNSET
        if not isinstance(self.auto_pilot_time, Unset):
            auto_pilot_time = self.auto_pilot_time.value

        auto_pilot_offset = self.auto_pilot_offset
        enable_auto_open = self.enable_auto_open
        auto_submit_fps = self.auto_submit_fps
        auto_submit_payments = self.auto_submit_payments
        auto_submit_journal = self.auto_submit_journal
        auto_submit_payments_employee = self.auto_submit_payments_employee
        auto_submit_payments_hmrc = self.auto_submit_payments_hmrc
        auto_submit_payments_deductions = self.auto_submit_payments_deductions
        auto_submit_payments_aeos = self.auto_submit_payments_aeos
        auto_submit_payments_pensions = self.auto_submit_payments_pensions
        employees_without_email_address = self.employees_without_email_address
        employees_with_email_address_but_not_auto_sending = (
            self.employees_with_email_address_but_not_auto_sending
        )
        subcontractors_not_auto_sending_statement = (
            self.subcontractors_not_auto_sending_statement
        )
        coding_notices_automatically_applied = self.coding_notices_automatically_applied
        payrun_emails: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.payrun_emails, Unset):
            if self.payrun_emails is None:
                payrun_emails = None
            else:
                payrun_emails = []
                for payrun_emails_item_data in self.payrun_emails:
                    payrun_emails_item = payrun_emails_item_data.to_dict()

                    payrun_emails.append(payrun_emails_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enable_auto_pilot is not UNSET:
            field_dict["enableAutoPilot"] = enable_auto_pilot
        if auto_pilot_time is not UNSET:
            field_dict["autoPilotTime"] = auto_pilot_time
        if auto_pilot_offset is not UNSET:
            field_dict["autoPilotOffset"] = auto_pilot_offset
        if enable_auto_open is not UNSET:
            field_dict["enableAutoOpen"] = enable_auto_open
        if auto_submit_fps is not UNSET:
            field_dict["autoSubmitFps"] = auto_submit_fps
        if auto_submit_payments is not UNSET:
            field_dict["autoSubmitPayments"] = auto_submit_payments
        if auto_submit_journal is not UNSET:
            field_dict["autoSubmitJournal"] = auto_submit_journal
        if auto_submit_payments_employee is not UNSET:
            field_dict["autoSubmitPayments_Employee"] = auto_submit_payments_employee
        if auto_submit_payments_hmrc is not UNSET:
            field_dict["autoSubmitPayments_Hmrc"] = auto_submit_payments_hmrc
        if auto_submit_payments_deductions is not UNSET:
            field_dict[
                "autoSubmitPayments_Deductions"
            ] = auto_submit_payments_deductions
        if auto_submit_payments_aeos is not UNSET:
            field_dict["autoSubmitPayments_Aeos"] = auto_submit_payments_aeos
        if auto_submit_payments_pensions is not UNSET:
            field_dict["autoSubmitPayments_Pensions"] = auto_submit_payments_pensions
        if employees_without_email_address is not UNSET:
            field_dict["employeesWithoutEmailAddress"] = employees_without_email_address
        if employees_with_email_address_but_not_auto_sending is not UNSET:
            field_dict[
                "employeesWithEmailAddressButNotAutoSending"
            ] = employees_with_email_address_but_not_auto_sending
        if subcontractors_not_auto_sending_statement is not UNSET:
            field_dict[
                "subcontractorsNotAutoSendingStatement"
            ] = subcontractors_not_auto_sending_statement
        if coding_notices_automatically_applied is not UNSET:
            field_dict[
                "codingNoticesAutomaticallyApplied"
            ] = coding_notices_automatically_applied
        if payrun_emails is not UNSET:
            field_dict["payrunEmails"] = payrun_emails

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enable_auto_pilot = d.pop("enableAutoPilot", UNSET)

        _auto_pilot_time = d.pop("autoPilotTime", UNSET)
        auto_pilot_time: Union[Unset, AutoPilotFinaliseTime]
        if isinstance(_auto_pilot_time, Unset):
            auto_pilot_time = UNSET
        else:
            auto_pilot_time = AutoPilotFinaliseTime(_auto_pilot_time)

        auto_pilot_offset = d.pop("autoPilotOffset", UNSET)

        enable_auto_open = d.pop("enableAutoOpen", UNSET)

        auto_submit_fps = d.pop("autoSubmitFps", UNSET)

        auto_submit_payments = d.pop("autoSubmitPayments", UNSET)

        auto_submit_journal = d.pop("autoSubmitJournal", UNSET)

        auto_submit_payments_employee = d.pop("autoSubmitPayments_Employee", UNSET)

        auto_submit_payments_hmrc = d.pop("autoSubmitPayments_Hmrc", UNSET)

        auto_submit_payments_deductions = d.pop("autoSubmitPayments_Deductions", UNSET)

        auto_submit_payments_aeos = d.pop("autoSubmitPayments_Aeos", UNSET)

        auto_submit_payments_pensions = d.pop("autoSubmitPayments_Pensions", UNSET)

        employees_without_email_address = d.pop("employeesWithoutEmailAddress", UNSET)

        employees_with_email_address_but_not_auto_sending = d.pop(
            "employeesWithEmailAddressButNotAutoSending", UNSET
        )

        subcontractors_not_auto_sending_statement = d.pop(
            "subcontractorsNotAutoSendingStatement", UNSET
        )

        coding_notices_automatically_applied = d.pop(
            "codingNoticesAutomaticallyApplied", UNSET
        )

        payrun_emails = []
        _payrun_emails = d.pop("payrunEmails", UNSET)
        for payrun_emails_item_data in _payrun_emails or []:
            payrun_emails_item = PayrunEmail.from_dict(payrun_emails_item_data)

            payrun_emails.append(payrun_emails_item)

        automation_settings = cls(
            enable_auto_pilot=enable_auto_pilot,
            auto_pilot_time=auto_pilot_time,
            auto_pilot_offset=auto_pilot_offset,
            enable_auto_open=enable_auto_open,
            auto_submit_fps=auto_submit_fps,
            auto_submit_payments=auto_submit_payments,
            auto_submit_journal=auto_submit_journal,
            auto_submit_payments_employee=auto_submit_payments_employee,
            auto_submit_payments_hmrc=auto_submit_payments_hmrc,
            auto_submit_payments_deductions=auto_submit_payments_deductions,
            auto_submit_payments_aeos=auto_submit_payments_aeos,
            auto_submit_payments_pensions=auto_submit_payments_pensions,
            employees_without_email_address=employees_without_email_address,
            employees_with_email_address_but_not_auto_sending=employees_with_email_address_but_not_auto_sending,
            subcontractors_not_auto_sending_statement=subcontractors_not_auto_sending_statement,
            coding_notices_automatically_applied=coding_notices_automatically_applied,
            payrun_emails=payrun_emails,
        )

        return automation_settings
