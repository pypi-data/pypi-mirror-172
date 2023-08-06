import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.bank_details import BankDetails
from ..models.item import Item
from ..models.pay_method import PayMethod
from ..models.payee_type import PayeeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunPayment")


@attr.s(auto_attribs=True)
class PayRunPayment:
    """
    Attributes:
        type (Union[Unset, PayeeType]):
        payee (Union[Unset, Item]):
        date (Union[Unset, datetime.date]): [readonly] The date the payment is to be made
        method (Union[Unset, PayMethod]):
        amount (Union[Unset, float]): [readonly] The amount to pay
        reference (Union[Unset, None, str]): [readonly] The period the payment is for
        bank_details (Union[Unset, BankDetails]):
        bacs_hash (Union[Unset, None, str]): [readonly] if paying by Credit and you've enabled BacsHash then this will
            contain the BacsHash included on the FPS
        bacs_sub_reference (Union[Unset, None, str]): [readonly] if paying by Credit and you've enabled BacsHash then
            this will contain the BacsSubReference included on the FPS
    """

    type: Union[Unset, PayeeType] = UNSET
    payee: Union[Unset, Item] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    method: Union[Unset, PayMethod] = UNSET
    amount: Union[Unset, float] = UNSET
    reference: Union[Unset, None, str] = UNSET
    bank_details: Union[Unset, BankDetails] = UNSET
    bacs_hash: Union[Unset, None, str] = UNSET
    bacs_sub_reference: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        payee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.payee, Unset):
            payee = self.payee.to_dict()

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        method: Union[Unset, str] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        amount = self.amount
        reference = self.reference
        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        bacs_hash = self.bacs_hash
        bacs_sub_reference = self.bacs_sub_reference

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if payee is not UNSET:
            field_dict["payee"] = payee
        if date is not UNSET:
            field_dict["date"] = date
        if method is not UNSET:
            field_dict["method"] = method
        if amount is not UNSET:
            field_dict["amount"] = amount
        if reference is not UNSET:
            field_dict["reference"] = reference
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if bacs_hash is not UNSET:
            field_dict["bacsHash"] = bacs_hash
        if bacs_sub_reference is not UNSET:
            field_dict["bacsSubReference"] = bacs_sub_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PayeeType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PayeeType(_type)

        _payee = d.pop("payee", UNSET)
        payee: Union[Unset, Item]
        if isinstance(_payee, Unset):
            payee = UNSET
        else:
            payee = Item.from_dict(_payee)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        _method = d.pop("method", UNSET)
        method: Union[Unset, PayMethod]
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = PayMethod(_method)

        amount = d.pop("amount", UNSET)

        reference = d.pop("reference", UNSET)

        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details, Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)

        bacs_hash = d.pop("bacsHash", UNSET)

        bacs_sub_reference = d.pop("bacsSubReference", UNSET)

        pay_run_payment = cls(
            type=type,
            payee=payee,
            date=date,
            method=method,
            amount=amount,
            reference=reference,
            bank_details=bank_details,
            bacs_hash=bacs_hash,
            bacs_sub_reference=bacs_sub_reference,
        )

        return pay_run_payment
