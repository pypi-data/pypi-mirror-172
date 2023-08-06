from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.employer_template_type import EmployerTemplateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayrunEmail")


@attr.s(auto_attribs=True)
class PayrunEmail:
    """PayrunEmails are sent automatically when a payrun has been finalised

    Attributes:
        name (str): Only used for reference, not included in the email
        recipient_address (str): The address to which the email should be sent
        is_active (Union[Unset, bool]): If false then this email won't be sent
        template_type (Union[Unset, EmployerTemplateType]):
        pdf_password (Union[Unset, None, str]): If a value is provided, then all PDFs attached to the email will be
            encrypted using this password
        attach_payslips (Union[Unset, bool]): If set to true then Payslips will be attached to the email
        payslips_unemailed (Union[Unset, bool]): If AttachPayslips is true and this property is also true then only
            payslips that haven't already been sent directly to employees will be attached.
        payslips_single_file (Union[Unset, bool]): If AttachPayslips is true and this property is also true then the
            payslips will be attached as a single file rather than as separate PDFs,
        attach_payment_summary (Union[Unset, bool]): If set to True then the PaymentSummary report will be attached to
            the Email
        attach_p32 (Union[Unset, bool]): If set to True then the P32 report will be attached to the email
        attach_p30 (Union[Unset, bool]): If set to True then the P30 report will be attached to the email
        attach_gross_to_net (Union[Unset, bool]): If set to True then the GrossToNet report will be attached to the
            email
        attach_pension_contributions (Union[Unset, bool]): If set to True then the Pensions Contributions report will be
            attached to the email
        attach_cost_analysis (Union[Unset, bool]): If set to True then the Cost Analysis report will be attached to the
            email
        attach_cost_of_employment (Union[Unset, bool]): If set to True then the Cost of Employment report will be
            attached to the email
        attach_full_summary_of_pay (Union[Unset, bool]): If set to True then the Full Summary Of Payment report will be
            attached to the email
        attach_bank_payments (Union[Unset, bool]): If set to True then the Bank Payments CSV file will be attached to
            the email
        custom_subject (Union[Unset, None, str]): If TemplateType is null then you can provide a subject line here to be
            used for the email
        custom_body (Union[Unset, None, str]): If TemplateType is null then you can provide the body text here to be
            used for the email
        custom_body_is_html (Union[Unset, bool]): If the CustomBody is in HTML format, set this to true.
        child_id (Union[Unset, str]): This is nothing but the UniqueId of the model.
    """

    name: str
    recipient_address: str
    is_active: Union[Unset, bool] = UNSET
    template_type: Union[Unset, EmployerTemplateType] = UNSET
    pdf_password: Union[Unset, None, str] = UNSET
    attach_payslips: Union[Unset, bool] = UNSET
    payslips_unemailed: Union[Unset, bool] = UNSET
    payslips_single_file: Union[Unset, bool] = UNSET
    attach_payment_summary: Union[Unset, bool] = UNSET
    attach_p32: Union[Unset, bool] = UNSET
    attach_p30: Union[Unset, bool] = UNSET
    attach_gross_to_net: Union[Unset, bool] = UNSET
    attach_pension_contributions: Union[Unset, bool] = UNSET
    attach_cost_analysis: Union[Unset, bool] = UNSET
    attach_cost_of_employment: Union[Unset, bool] = UNSET
    attach_full_summary_of_pay: Union[Unset, bool] = UNSET
    attach_bank_payments: Union[Unset, bool] = UNSET
    custom_subject: Union[Unset, None, str] = UNSET
    custom_body: Union[Unset, None, str] = UNSET
    custom_body_is_html: Union[Unset, bool] = UNSET
    child_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        recipient_address = self.recipient_address
        is_active = self.is_active
        template_type: Union[Unset, str] = UNSET
        if not isinstance(self.template_type, Unset):
            template_type = self.template_type.value

        pdf_password = self.pdf_password
        attach_payslips = self.attach_payslips
        payslips_unemailed = self.payslips_unemailed
        payslips_single_file = self.payslips_single_file
        attach_payment_summary = self.attach_payment_summary
        attach_p32 = self.attach_p32
        attach_p30 = self.attach_p30
        attach_gross_to_net = self.attach_gross_to_net
        attach_pension_contributions = self.attach_pension_contributions
        attach_cost_analysis = self.attach_cost_analysis
        attach_cost_of_employment = self.attach_cost_of_employment
        attach_full_summary_of_pay = self.attach_full_summary_of_pay
        attach_bank_payments = self.attach_bank_payments
        custom_subject = self.custom_subject
        custom_body = self.custom_body
        custom_body_is_html = self.custom_body_is_html
        child_id = self.child_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "recipientAddress": recipient_address,
            }
        )
        if is_active is not UNSET:
            field_dict["isActive"] = is_active
        if template_type is not UNSET:
            field_dict["templateType"] = template_type
        if pdf_password is not UNSET:
            field_dict["pdfPassword"] = pdf_password
        if attach_payslips is not UNSET:
            field_dict["attachPayslips"] = attach_payslips
        if payslips_unemailed is not UNSET:
            field_dict["payslips_Unemailed"] = payslips_unemailed
        if payslips_single_file is not UNSET:
            field_dict["payslips_SingleFile"] = payslips_single_file
        if attach_payment_summary is not UNSET:
            field_dict["attachPaymentSummary"] = attach_payment_summary
        if attach_p32 is not UNSET:
            field_dict["attachP32"] = attach_p32
        if attach_p30 is not UNSET:
            field_dict["attachP30"] = attach_p30
        if attach_gross_to_net is not UNSET:
            field_dict["attachGrossToNet"] = attach_gross_to_net
        if attach_pension_contributions is not UNSET:
            field_dict["attachPensionContributions"] = attach_pension_contributions
        if attach_cost_analysis is not UNSET:
            field_dict["attachCostAnalysis"] = attach_cost_analysis
        if attach_cost_of_employment is not UNSET:
            field_dict["attachCostOfEmployment"] = attach_cost_of_employment
        if attach_full_summary_of_pay is not UNSET:
            field_dict["attachFullSummaryOfPay"] = attach_full_summary_of_pay
        if attach_bank_payments is not UNSET:
            field_dict["attachBankPayments"] = attach_bank_payments
        if custom_subject is not UNSET:
            field_dict["customSubject"] = custom_subject
        if custom_body is not UNSET:
            field_dict["customBody"] = custom_body
        if custom_body_is_html is not UNSET:
            field_dict["customBody_IsHtml"] = custom_body_is_html
        if child_id is not UNSET:
            field_dict["childId"] = child_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        recipient_address = d.pop("recipientAddress")

        is_active = d.pop("isActive", UNSET)

        _template_type = d.pop("templateType", UNSET)
        template_type: Union[Unset, EmployerTemplateType]
        if isinstance(_template_type, Unset):
            template_type = UNSET
        else:
            template_type = EmployerTemplateType(_template_type)

        pdf_password = d.pop("pdfPassword", UNSET)

        attach_payslips = d.pop("attachPayslips", UNSET)

        payslips_unemailed = d.pop("payslips_Unemailed", UNSET)

        payslips_single_file = d.pop("payslips_SingleFile", UNSET)

        attach_payment_summary = d.pop("attachPaymentSummary", UNSET)

        attach_p32 = d.pop("attachP32", UNSET)

        attach_p30 = d.pop("attachP30", UNSET)

        attach_gross_to_net = d.pop("attachGrossToNet", UNSET)

        attach_pension_contributions = d.pop("attachPensionContributions", UNSET)

        attach_cost_analysis = d.pop("attachCostAnalysis", UNSET)

        attach_cost_of_employment = d.pop("attachCostOfEmployment", UNSET)

        attach_full_summary_of_pay = d.pop("attachFullSummaryOfPay", UNSET)

        attach_bank_payments = d.pop("attachBankPayments", UNSET)

        custom_subject = d.pop("customSubject", UNSET)

        custom_body = d.pop("customBody", UNSET)

        custom_body_is_html = d.pop("customBody_IsHtml", UNSET)

        child_id = d.pop("childId", UNSET)

        payrun_email = cls(
            name=name,
            recipient_address=recipient_address,
            is_active=is_active,
            template_type=template_type,
            pdf_password=pdf_password,
            attach_payslips=attach_payslips,
            payslips_unemailed=payslips_unemailed,
            payslips_single_file=payslips_single_file,
            attach_payment_summary=attach_payment_summary,
            attach_p32=attach_p32,
            attach_p30=attach_p30,
            attach_gross_to_net=attach_gross_to_net,
            attach_pension_contributions=attach_pension_contributions,
            attach_cost_analysis=attach_cost_analysis,
            attach_cost_of_employment=attach_cost_of_employment,
            attach_full_summary_of_pay=attach_full_summary_of_pay,
            attach_bank_payments=attach_bank_payments,
            custom_subject=custom_subject,
            custom_body=custom_body,
            custom_body_is_html=custom_body_is_html,
            child_id=child_id,
        )

        return payrun_email
