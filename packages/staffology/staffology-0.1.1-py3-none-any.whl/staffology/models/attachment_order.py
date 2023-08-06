import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.attachment_order_payment import AttachmentOrderPayment
from ..models.attachment_order_type import AttachmentOrderType
from ..models.bank_details import BankDetails
from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentOrder")


@attr.s(auto_attribs=True)
class AttachmentOrder:
    """Used to represent an Attachment of Earnings Order (AEO)

    Attributes:
        type (Union[Unset, AttachmentOrderType]):
        carry_forward_shortfall (Union[Unset, bool]): [ReadOnly] Whether or not shortfalls should be carried forward
        allow_protected_earnings (Union[Unset, bool]): [ReadOnly] Whether or not shortfalls should be carried forward
        auto_deduction (Union[Unset, bool]): [readonly] Whether or not the amount to be deducted is automatically
            calculated
        reference (Union[Unset, None, str]): The reference which appeared on the court paperwork
        issue_date (Union[Unset, datetime.date]): The date of issue for this Order
        apply_from (Union[Unset, datetime.date]): The date from which to apply this Order
        apply_until (Union[Unset, None, datetime.date]): An optional date on which to stop applying this order
        deduction_is_percentage (Union[Unset, bool]): Whether or not the amount given for Deduction is a percentage
            rather than a fixed amount
        deduction (Union[Unset, float]): The percentage or amount (depending on DeductionIsPercentage) to deduct
        protected_earnings_is_percentage (Union[Unset, bool]): Whether or not the amount for ProtectedEarnings is a
            percentage rather than a fixed amount.
        protected_earnings (Union[Unset, float]): The percentage or amount or percentage (depending on
            ProtectedEarningsIsPercentage) to protect
        charge_admin_fee (Union[Unset, bool]): Whether or not a £1 admin fee should be deducted for this order
        shortfall (Union[Unset, float]): Any shortfall that is being carried forward
        stop_when_total_paid (Union[Unset, bool]): Whether or not this order should be stopped once a total amount has
            been paid
        total_amount_to_pay (Union[Unset, float]): The Total amount that needs to be paid for this Order
        amount_previously_paid (Union[Unset, float]): Any amount that has previously been paid towards this Order
        stopped (Union[Unset, bool]): [readonly] Whether or not this Order has been stopped.
            This is set automatically when either it's paid in full or the ApplyUntil date has been reached.
        notes (Union[Unset, None, str]): A free-form text field to record any comments
        include_bank_details (Union[Unset, bool]):
        bank_details (Union[Unset, BankDetails]):
        payments (Union[Unset, None, List[AttachmentOrderPayment]]): [readonly] Payments made towards this order. Only
            populated when viewed as a report.
        payee (Union[Unset, None, str]): The Id of the Payee, if any, that deductions are to be paid to.
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    type: Union[Unset, AttachmentOrderType] = UNSET
    carry_forward_shortfall: Union[Unset, bool] = UNSET
    allow_protected_earnings: Union[Unset, bool] = UNSET
    auto_deduction: Union[Unset, bool] = UNSET
    reference: Union[Unset, None, str] = UNSET
    issue_date: Union[Unset, datetime.date] = UNSET
    apply_from: Union[Unset, datetime.date] = UNSET
    apply_until: Union[Unset, None, datetime.date] = UNSET
    deduction_is_percentage: Union[Unset, bool] = UNSET
    deduction: Union[Unset, float] = UNSET
    protected_earnings_is_percentage: Union[Unset, bool] = UNSET
    protected_earnings: Union[Unset, float] = UNSET
    charge_admin_fee: Union[Unset, bool] = UNSET
    shortfall: Union[Unset, float] = UNSET
    stop_when_total_paid: Union[Unset, bool] = UNSET
    total_amount_to_pay: Union[Unset, float] = UNSET
    amount_previously_paid: Union[Unset, float] = UNSET
    stopped: Union[Unset, bool] = UNSET
    notes: Union[Unset, None, str] = UNSET
    include_bank_details: Union[Unset, bool] = UNSET
    bank_details: Union[Unset, BankDetails] = UNSET
    payments: Union[Unset, None, List[AttachmentOrderPayment]] = UNSET
    payee: Union[Unset, None, str] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        carry_forward_shortfall = self.carry_forward_shortfall
        allow_protected_earnings = self.allow_protected_earnings
        auto_deduction = self.auto_deduction
        reference = self.reference
        issue_date: Union[Unset, str] = UNSET
        if not isinstance(self.issue_date, Unset):
            issue_date = self.issue_date.isoformat()

        apply_from: Union[Unset, str] = UNSET
        if not isinstance(self.apply_from, Unset):
            apply_from = self.apply_from.isoformat()

        apply_until: Union[Unset, None, str] = UNSET
        if not isinstance(self.apply_until, Unset):
            apply_until = self.apply_until.isoformat() if self.apply_until else None

        deduction_is_percentage = self.deduction_is_percentage
        deduction = self.deduction
        protected_earnings_is_percentage = self.protected_earnings_is_percentage
        protected_earnings = self.protected_earnings
        charge_admin_fee = self.charge_admin_fee
        shortfall = self.shortfall
        stop_when_total_paid = self.stop_when_total_paid
        total_amount_to_pay = self.total_amount_to_pay
        amount_previously_paid = self.amount_previously_paid
        stopped = self.stopped
        notes = self.notes
        include_bank_details = self.include_bank_details
        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        payments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.payments, Unset):
            if self.payments is None:
                payments = None
            else:
                payments = []
                for payments_item_data in self.payments:
                    payments_item = payments_item_data.to_dict()

                    payments.append(payments_item)

        payee = self.payee
        document_count = self.document_count
        documents: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            if self.documents is None:
                documents = None
            else:
                documents = []
                for documents_item_data in self.documents:
                    documents_item = documents_item_data.to_dict()

                    documents.append(documents_item)

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if carry_forward_shortfall is not UNSET:
            field_dict["carryForwardShortfall"] = carry_forward_shortfall
        if allow_protected_earnings is not UNSET:
            field_dict["allowProtectedEarnings"] = allow_protected_earnings
        if auto_deduction is not UNSET:
            field_dict["autoDeduction"] = auto_deduction
        if reference is not UNSET:
            field_dict["reference"] = reference
        if issue_date is not UNSET:
            field_dict["issueDate"] = issue_date
        if apply_from is not UNSET:
            field_dict["applyFrom"] = apply_from
        if apply_until is not UNSET:
            field_dict["applyUntil"] = apply_until
        if deduction_is_percentage is not UNSET:
            field_dict["deductionIsPercentage"] = deduction_is_percentage
        if deduction is not UNSET:
            field_dict["deduction"] = deduction
        if protected_earnings_is_percentage is not UNSET:
            field_dict[
                "protectedEarningsIsPercentage"
            ] = protected_earnings_is_percentage
        if protected_earnings is not UNSET:
            field_dict["protectedEarnings"] = protected_earnings
        if charge_admin_fee is not UNSET:
            field_dict["chargeAdminFee"] = charge_admin_fee
        if shortfall is not UNSET:
            field_dict["shortfall"] = shortfall
        if stop_when_total_paid is not UNSET:
            field_dict["stopWhenTotalPaid"] = stop_when_total_paid
        if total_amount_to_pay is not UNSET:
            field_dict["totalAmountToPay"] = total_amount_to_pay
        if amount_previously_paid is not UNSET:
            field_dict["amountPreviouslyPaid"] = amount_previously_paid
        if stopped is not UNSET:
            field_dict["stopped"] = stopped
        if notes is not UNSET:
            field_dict["notes"] = notes
        if include_bank_details is not UNSET:
            field_dict["includeBankDetails"] = include_bank_details
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if payments is not UNSET:
            field_dict["payments"] = payments
        if payee is not UNSET:
            field_dict["payee"] = payee
        if document_count is not UNSET:
            field_dict["documentCount"] = document_count
        if documents is not UNSET:
            field_dict["documents"] = documents
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, AttachmentOrderType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AttachmentOrderType(_type)

        carry_forward_shortfall = d.pop("carryForwardShortfall", UNSET)

        allow_protected_earnings = d.pop("allowProtectedEarnings", UNSET)

        auto_deduction = d.pop("autoDeduction", UNSET)

        reference = d.pop("reference", UNSET)

        _issue_date = d.pop("issueDate", UNSET)
        issue_date: Union[Unset, datetime.date]
        if isinstance(_issue_date, Unset):
            issue_date = UNSET
        else:
            issue_date = isoparse(_issue_date).date()

        _apply_from = d.pop("applyFrom", UNSET)
        apply_from: Union[Unset, datetime.date]
        if isinstance(_apply_from, Unset):
            apply_from = UNSET
        else:
            apply_from = isoparse(_apply_from).date()

        _apply_until = d.pop("applyUntil", UNSET)
        apply_until: Union[Unset, None, datetime.date]
        if _apply_until is None:
            apply_until = None
        elif isinstance(_apply_until, Unset):
            apply_until = UNSET
        else:
            apply_until = isoparse(_apply_until).date()

        deduction_is_percentage = d.pop("deductionIsPercentage", UNSET)

        deduction = d.pop("deduction", UNSET)

        protected_earnings_is_percentage = d.pop("protectedEarningsIsPercentage", UNSET)

        protected_earnings = d.pop("protectedEarnings", UNSET)

        charge_admin_fee = d.pop("chargeAdminFee", UNSET)

        shortfall = d.pop("shortfall", UNSET)

        stop_when_total_paid = d.pop("stopWhenTotalPaid", UNSET)

        total_amount_to_pay = d.pop("totalAmountToPay", UNSET)

        amount_previously_paid = d.pop("amountPreviouslyPaid", UNSET)

        stopped = d.pop("stopped", UNSET)

        notes = d.pop("notes", UNSET)

        include_bank_details = d.pop("includeBankDetails", UNSET)

        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details, Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)

        payments = []
        _payments = d.pop("payments", UNSET)
        for payments_item_data in _payments or []:
            payments_item = AttachmentOrderPayment.from_dict(payments_item_data)

            payments.append(payments_item)

        payee = d.pop("payee", UNSET)

        document_count = d.pop("documentCount", UNSET)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = Item.from_dict(documents_item_data)

            documents.append(documents_item)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        attachment_order = cls(
            type=type,
            carry_forward_shortfall=carry_forward_shortfall,
            allow_protected_earnings=allow_protected_earnings,
            auto_deduction=auto_deduction,
            reference=reference,
            issue_date=issue_date,
            apply_from=apply_from,
            apply_until=apply_until,
            deduction_is_percentage=deduction_is_percentage,
            deduction=deduction,
            protected_earnings_is_percentage=protected_earnings_is_percentage,
            protected_earnings=protected_earnings,
            charge_admin_fee=charge_admin_fee,
            shortfall=shortfall,
            stop_when_total_paid=stop_when_total_paid,
            total_amount_to_pay=total_amount_to_pay,
            amount_previously_paid=amount_previously_paid,
            stopped=stopped,
            notes=notes,
            include_bank_details=include_bank_details,
            bank_details=bank_details,
            payments=payments,
            payee=payee,
            document_count=document_count,
            documents=documents,
            employee=employee,
            id=id,
        )

        return attachment_order
