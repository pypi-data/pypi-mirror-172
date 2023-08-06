from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageBill")


@attr.s(auto_attribs=True)
class UsageBill:
    """
    Attributes:
        year (Union[Unset, int]):
        month (Union[Unset, int]):
        payslip_count (Union[Unset, int]):
        previously_billed_payslip_count (Union[Unset, int]): The number of payslips that appear in the usage, but were
            billed in a previous period
        net_cost (Union[Unset, float]):
        discount (Union[Unset, float]):
        partner_discount_amount (Union[Unset, float]):
        monthly_minimum (Union[Unset, float]):
        total (Union[Unset, float]):
        paid (Union[Unset, bool]):
        usage (Union[Unset, None, List[Item]]):
        accounting_customer_id (Union[Unset, None, str]):
        accounting_invoice_id (Union[Unset, None, str]):
        accounting_invoice_link (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    year: Union[Unset, int] = UNSET
    month: Union[Unset, int] = UNSET
    payslip_count: Union[Unset, int] = UNSET
    previously_billed_payslip_count: Union[Unset, int] = UNSET
    net_cost: Union[Unset, float] = UNSET
    discount: Union[Unset, float] = UNSET
    partner_discount_amount: Union[Unset, float] = UNSET
    monthly_minimum: Union[Unset, float] = UNSET
    total: Union[Unset, float] = UNSET
    paid: Union[Unset, bool] = UNSET
    usage: Union[Unset, None, List[Item]] = UNSET
    accounting_customer_id: Union[Unset, None, str] = UNSET
    accounting_invoice_id: Union[Unset, None, str] = UNSET
    accounting_invoice_link: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        year = self.year
        month = self.month
        payslip_count = self.payslip_count
        previously_billed_payslip_count = self.previously_billed_payslip_count
        net_cost = self.net_cost
        discount = self.discount
        partner_discount_amount = self.partner_discount_amount
        monthly_minimum = self.monthly_minimum
        total = self.total
        paid = self.paid
        usage: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.usage, Unset):
            if self.usage is None:
                usage = None
            else:
                usage = []
                for usage_item_data in self.usage:
                    usage_item = usage_item_data.to_dict()

                    usage.append(usage_item)

        accounting_customer_id = self.accounting_customer_id
        accounting_invoice_id = self.accounting_invoice_id
        accounting_invoice_link = self.accounting_invoice_link
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if year is not UNSET:
            field_dict["year"] = year
        if month is not UNSET:
            field_dict["month"] = month
        if payslip_count is not UNSET:
            field_dict["payslipCount"] = payslip_count
        if previously_billed_payslip_count is not UNSET:
            field_dict["previouslyBilledPayslipCount"] = previously_billed_payslip_count
        if net_cost is not UNSET:
            field_dict["netCost"] = net_cost
        if discount is not UNSET:
            field_dict["discount"] = discount
        if partner_discount_amount is not UNSET:
            field_dict["partnerDiscountAmount"] = partner_discount_amount
        if monthly_minimum is not UNSET:
            field_dict["monthlyMinimum"] = monthly_minimum
        if total is not UNSET:
            field_dict["total"] = total
        if paid is not UNSET:
            field_dict["paid"] = paid
        if usage is not UNSET:
            field_dict["usage"] = usage
        if accounting_customer_id is not UNSET:
            field_dict["accountingCustomerId"] = accounting_customer_id
        if accounting_invoice_id is not UNSET:
            field_dict["accountingInvoiceId"] = accounting_invoice_id
        if accounting_invoice_link is not UNSET:
            field_dict["accountingInvoiceLink"] = accounting_invoice_link
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        year = d.pop("year", UNSET)

        month = d.pop("month", UNSET)

        payslip_count = d.pop("payslipCount", UNSET)

        previously_billed_payslip_count = d.pop("previouslyBilledPayslipCount", UNSET)

        net_cost = d.pop("netCost", UNSET)

        discount = d.pop("discount", UNSET)

        partner_discount_amount = d.pop("partnerDiscountAmount", UNSET)

        monthly_minimum = d.pop("monthlyMinimum", UNSET)

        total = d.pop("total", UNSET)

        paid = d.pop("paid", UNSET)

        usage = []
        _usage = d.pop("usage", UNSET)
        for usage_item_data in _usage or []:
            usage_item = Item.from_dict(usage_item_data)

            usage.append(usage_item)

        accounting_customer_id = d.pop("accountingCustomerId", UNSET)

        accounting_invoice_id = d.pop("accountingInvoiceId", UNSET)

        accounting_invoice_link = d.pop("accountingInvoiceLink", UNSET)

        id = d.pop("id", UNSET)

        usage_bill = cls(
            year=year,
            month=month,
            payslip_count=payslip_count,
            previously_billed_payslip_count=previously_billed_payslip_count,
            net_cost=net_cost,
            discount=discount,
            partner_discount_amount=partner_discount_amount,
            monthly_minimum=monthly_minimum,
            total=total,
            paid=paid,
            usage=usage,
            accounting_customer_id=accounting_customer_id,
            accounting_invoice_id=accounting_invoice_id,
            accounting_invoice_link=accounting_invoice_link,
            id=id,
        )

        return usage_bill
