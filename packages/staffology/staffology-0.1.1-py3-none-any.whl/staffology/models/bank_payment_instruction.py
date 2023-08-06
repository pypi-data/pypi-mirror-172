from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.background_task_status import BackgroundTaskStatus
from ..models.bank_details import BankDetails
from ..models.pay_run_payment import PayRunPayment
from ..types import UNSET, Unset

T = TypeVar("T", bound="BankPaymentInstruction")


@attr.s(auto_attribs=True)
class BankPaymentInstruction:
    """
    Attributes:
        originator (Union[Unset, BankDetails]):
        bank_payments (Union[Unset, None, List[PayRunPayment]]):
        status (Union[Unset, BackgroundTaskStatus]):
        status_message (Union[Unset, None, str]): [readonly] A message to elaborate on the Status
        link (Union[Unset, None, str]): [readonly] If available, a link to the payments in an ExternalDataProvider
        service_user_number (Union[Unset, None, str]): Service user number to be used while sending payment instruction
        bureau_number (Union[Unset, None, str]): Bureau number to be used if available while sending payment instruction
    """

    originator: Union[Unset, BankDetails] = UNSET
    bank_payments: Union[Unset, None, List[PayRunPayment]] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    link: Union[Unset, None, str] = UNSET
    service_user_number: Union[Unset, None, str] = UNSET
    bureau_number: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        originator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.originator, Unset):
            originator = self.originator.to_dict()

        bank_payments: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.bank_payments, Unset):
            if self.bank_payments is None:
                bank_payments = None
            else:
                bank_payments = []
                for bank_payments_item_data in self.bank_payments:
                    bank_payments_item = bank_payments_item_data.to_dict()

                    bank_payments.append(bank_payments_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_message = self.status_message
        link = self.link
        service_user_number = self.service_user_number
        bureau_number = self.bureau_number

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if originator is not UNSET:
            field_dict["originator"] = originator
        if bank_payments is not UNSET:
            field_dict["bankPayments"] = bank_payments
        if status is not UNSET:
            field_dict["status"] = status
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if link is not UNSET:
            field_dict["link"] = link
        if service_user_number is not UNSET:
            field_dict["serviceUserNumber"] = service_user_number
        if bureau_number is not UNSET:
            field_dict["bureauNumber"] = bureau_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _originator = d.pop("originator", UNSET)
        originator: Union[Unset, BankDetails]
        if isinstance(_originator, Unset):
            originator = UNSET
        else:
            originator = BankDetails.from_dict(_originator)

        bank_payments = []
        _bank_payments = d.pop("bankPayments", UNSET)
        for bank_payments_item_data in _bank_payments or []:
            bank_payments_item = PayRunPayment.from_dict(bank_payments_item_data)

            bank_payments.append(bank_payments_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)

        status_message = d.pop("statusMessage", UNSET)

        link = d.pop("link", UNSET)

        service_user_number = d.pop("serviceUserNumber", UNSET)

        bureau_number = d.pop("bureauNumber", UNSET)

        bank_payment_instruction = cls(
            originator=originator,
            bank_payments=bank_payments,
            status=status,
            status_message=status_message,
            link=link,
            service_user_number=service_user_number,
            bureau_number=bureau_number,
        )

        return bank_payment_instruction
