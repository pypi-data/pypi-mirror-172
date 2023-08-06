from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DirectDebitMandate")


@attr.s(auto_attribs=True)
class DirectDebitMandate:
    """
    Attributes:
        is_completed (Union[Unset, bool]):
        mandate_link (Union[Unset, None, str]):
        customer_link (Union[Unset, None, str]):
        bank_name (Union[Unset, None, str]):
        account_number_ending (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    is_completed: Union[Unset, bool] = UNSET
    mandate_link: Union[Unset, None, str] = UNSET
    customer_link: Union[Unset, None, str] = UNSET
    bank_name: Union[Unset, None, str] = UNSET
    account_number_ending: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_completed = self.is_completed
        mandate_link = self.mandate_link
        customer_link = self.customer_link
        bank_name = self.bank_name
        account_number_ending = self.account_number_ending
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_completed is not UNSET:
            field_dict["isCompleted"] = is_completed
        if mandate_link is not UNSET:
            field_dict["mandateLink"] = mandate_link
        if customer_link is not UNSET:
            field_dict["customerLink"] = customer_link
        if bank_name is not UNSET:
            field_dict["bankName"] = bank_name
        if account_number_ending is not UNSET:
            field_dict["accountNumberEnding"] = account_number_ending
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_completed = d.pop("isCompleted", UNSET)

        mandate_link = d.pop("mandateLink", UNSET)

        customer_link = d.pop("customerLink", UNSET)

        bank_name = d.pop("bankName", UNSET)

        account_number_ending = d.pop("accountNumberEnding", UNSET)

        id = d.pop("id", UNSET)

        direct_debit_mandate = cls(
            is_completed=is_completed,
            mandate_link=mandate_link,
            customer_link=customer_link,
            bank_name=bank_name,
            account_number_ending=account_number_ending,
            id=id,
        )

        return direct_debit_mandate
