import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="Loan")


@attr.s(auto_attribs=True)
class Loan:
    """Used to represent an Attachment of Earnings Order (AEO)

    Attributes:
        issue_date (Union[Unset, datetime.date]): The date the Loan was made
        reference (Union[Unset, None, str]): An optional reference for this Loan
        pay_code (Union[Unset, None, str]): The Code of the PayCode used for recording payments.
            The PayCode must have a CalculationType of FixedAmount and not be a multiplier code
        loan_amount (Union[Unset, float]): The initial amount that the loan was for
        period_amount (Union[Unset, float]): The amount to deduct per PayPeriod
        amount_repaid (Union[Unset, float]): [readonly] The amount repaid so far due to deductions in Payruns
        previously_paid (Union[Unset, float]): [readonly] Any amount by which to adjust the Balance, perhaps due to
            repayments made elsewhere
        balance (Union[Unset, float]): [readonly] The Balance of the Loan
        is_settled (Union[Unset, bool]): [readonly]
        is_paused (Union[Unset, bool]): If set to true then deductions will not be made
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    issue_date: Union[Unset, datetime.date] = UNSET
    reference: Union[Unset, None, str] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    loan_amount: Union[Unset, float] = UNSET
    period_amount: Union[Unset, float] = UNSET
    amount_repaid: Union[Unset, float] = UNSET
    previously_paid: Union[Unset, float] = UNSET
    balance: Union[Unset, float] = UNSET
    is_settled: Union[Unset, bool] = UNSET
    is_paused: Union[Unset, bool] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_date: Union[Unset, str] = UNSET
        if not isinstance(self.issue_date, Unset):
            issue_date = self.issue_date.isoformat()

        reference = self.reference
        pay_code = self.pay_code
        loan_amount = self.loan_amount
        period_amount = self.period_amount
        amount_repaid = self.amount_repaid
        previously_paid = self.previously_paid
        balance = self.balance
        is_settled = self.is_settled
        is_paused = self.is_paused
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
        if issue_date is not UNSET:
            field_dict["issueDate"] = issue_date
        if reference is not UNSET:
            field_dict["reference"] = reference
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if loan_amount is not UNSET:
            field_dict["loanAmount"] = loan_amount
        if period_amount is not UNSET:
            field_dict["periodAmount"] = period_amount
        if amount_repaid is not UNSET:
            field_dict["amountRepaid"] = amount_repaid
        if previously_paid is not UNSET:
            field_dict["previouslyPaid"] = previously_paid
        if balance is not UNSET:
            field_dict["balance"] = balance
        if is_settled is not UNSET:
            field_dict["isSettled"] = is_settled
        if is_paused is not UNSET:
            field_dict["isPaused"] = is_paused
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
        _issue_date = d.pop("issueDate", UNSET)
        issue_date: Union[Unset, datetime.date]
        if isinstance(_issue_date, Unset):
            issue_date = UNSET
        else:
            issue_date = isoparse(_issue_date).date()

        reference = d.pop("reference", UNSET)

        pay_code = d.pop("payCode", UNSET)

        loan_amount = d.pop("loanAmount", UNSET)

        period_amount = d.pop("periodAmount", UNSET)

        amount_repaid = d.pop("amountRepaid", UNSET)

        previously_paid = d.pop("previouslyPaid", UNSET)

        balance = d.pop("balance", UNSET)

        is_settled = d.pop("isSettled", UNSET)

        is_paused = d.pop("isPaused", UNSET)

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

        loan = cls(
            issue_date=issue_date,
            reference=reference,
            pay_code=pay_code,
            loan_amount=loan_amount,
            period_amount=period_amount,
            amount_repaid=amount_repaid,
            previously_paid=previously_paid,
            balance=balance,
            is_settled=is_settled,
            is_paused=is_paused,
            document_count=document_count,
            documents=documents,
            employee=employee,
            id=id,
        )

        return loan
