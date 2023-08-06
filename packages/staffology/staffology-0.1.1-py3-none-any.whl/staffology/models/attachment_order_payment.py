import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.pay_periods import PayPeriods
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentOrderPayment")


@attr.s(auto_attribs=True)
class AttachmentOrderPayment:
    """Used to represent a payment towards an Attachment of Earnings Order (AEO)

    Attributes:
        attachment_order (Union[Unset, Item]):
        tax_year (Union[Unset, TaxYear]):
        pay_period (Union[Unset, PayPeriods]):
        date (Union[Unset, datetime.date]): [readonly] The date this deduction was made
        description (Union[Unset, None, str]): [readonly] Description of deduction, usually the reference from the
            AttachmentOrder
        attachable_pay (Union[Unset, float]): [readonly] The total Attachable pay for the Employee on this PayRun
        protected_pay (Union[Unset, float]): [readonly] The amount of the Attachable Pay that must be protected
        other_attachment_order_deductions (Union[Unset, float]): [readonly] Deductions made on this PayRun for this
            employee due to  other higher priority AttachmentOrders
        desired_deduction (Union[Unset, float]): [readonly] The amount that should be deducted, if arrestable pay is
            available.
            Not including any shortfall
        shortfall (Union[Unset, float]): [readonly] Any shortfall (ie arrears) that existed before this PayRun.
        total_paid (Union[Unset, float]): [readonly] Total amount paid to date, including this deduction.
        resulting_deduction (Union[Unset, float]): [readonly] The actual amount deducted
        resulting_shortfall (Union[Unset, float]): [readonly] The resulting shortfall (including any shortfall from
            previous periods
        admin_fee (Union[Unset, float]): [readonly] Any admin fee charged
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    attachment_order: Union[Unset, Item] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    description: Union[Unset, None, str] = UNSET
    attachable_pay: Union[Unset, float] = UNSET
    protected_pay: Union[Unset, float] = UNSET
    other_attachment_order_deductions: Union[Unset, float] = UNSET
    desired_deduction: Union[Unset, float] = UNSET
    shortfall: Union[Unset, float] = UNSET
    total_paid: Union[Unset, float] = UNSET
    resulting_deduction: Union[Unset, float] = UNSET
    resulting_shortfall: Union[Unset, float] = UNSET
    admin_fee: Union[Unset, float] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        attachment_order: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.attachment_order, Unset):
            attachment_order = self.attachment_order.to_dict()

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        description = self.description
        attachable_pay = self.attachable_pay
        protected_pay = self.protected_pay
        other_attachment_order_deductions = self.other_attachment_order_deductions
        desired_deduction = self.desired_deduction
        shortfall = self.shortfall
        total_paid = self.total_paid
        resulting_deduction = self.resulting_deduction
        resulting_shortfall = self.resulting_shortfall
        admin_fee = self.admin_fee
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if attachment_order is not UNSET:
            field_dict["attachmentOrder"] = attachment_order
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if date is not UNSET:
            field_dict["date"] = date
        if description is not UNSET:
            field_dict["description"] = description
        if attachable_pay is not UNSET:
            field_dict["attachablePay"] = attachable_pay
        if protected_pay is not UNSET:
            field_dict["protectedPay"] = protected_pay
        if other_attachment_order_deductions is not UNSET:
            field_dict[
                "otherAttachmentOrderDeductions"
            ] = other_attachment_order_deductions
        if desired_deduction is not UNSET:
            field_dict["desiredDeduction"] = desired_deduction
        if shortfall is not UNSET:
            field_dict["shortfall"] = shortfall
        if total_paid is not UNSET:
            field_dict["totalPaid"] = total_paid
        if resulting_deduction is not UNSET:
            field_dict["resultingDeduction"] = resulting_deduction
        if resulting_shortfall is not UNSET:
            field_dict["resultingShortfall"] = resulting_shortfall
        if admin_fee is not UNSET:
            field_dict["adminFee"] = admin_fee
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _attachment_order = d.pop("attachmentOrder", UNSET)
        attachment_order: Union[Unset, Item]
        if isinstance(_attachment_order, Unset):
            attachment_order = UNSET
        else:
            attachment_order = Item.from_dict(_attachment_order)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        description = d.pop("description", UNSET)

        attachable_pay = d.pop("attachablePay", UNSET)

        protected_pay = d.pop("protectedPay", UNSET)

        other_attachment_order_deductions = d.pop(
            "otherAttachmentOrderDeductions", UNSET
        )

        desired_deduction = d.pop("desiredDeduction", UNSET)

        shortfall = d.pop("shortfall", UNSET)

        total_paid = d.pop("totalPaid", UNSET)

        resulting_deduction = d.pop("resultingDeduction", UNSET)

        resulting_shortfall = d.pop("resultingShortfall", UNSET)

        admin_fee = d.pop("adminFee", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        attachment_order_payment = cls(
            attachment_order=attachment_order,
            tax_year=tax_year,
            pay_period=pay_period,
            date=date,
            description=description,
            attachable_pay=attachable_pay,
            protected_pay=protected_pay,
            other_attachment_order_deductions=other_attachment_order_deductions,
            desired_deduction=desired_deduction,
            shortfall=shortfall,
            total_paid=total_paid,
            resulting_deduction=resulting_deduction,
            resulting_shortfall=resulting_shortfall,
            admin_fee=admin_fee,
            employee=employee,
            id=id,
        )

        return attachment_order_payment
