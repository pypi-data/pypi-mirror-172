from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BankDetails")


@attr.s(auto_attribs=True)
class BankDetails:
    """
    Attributes:
        bank_name (Union[Unset, None, str]):
        bank_branch (Union[Unset, None, str]):
        bank_reference (Union[Unset, None, str]):
        account_name (Union[Unset, None, str]):
        account_number (Union[Unset, None, str]):
        sort_code (Union[Unset, None, str]):
        note (Union[Unset, None, str]):
    """

    bank_name: Union[Unset, None, str] = UNSET
    bank_branch: Union[Unset, None, str] = UNSET
    bank_reference: Union[Unset, None, str] = UNSET
    account_name: Union[Unset, None, str] = UNSET
    account_number: Union[Unset, None, str] = UNSET
    sort_code: Union[Unset, None, str] = UNSET
    note: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        bank_name = self.bank_name
        bank_branch = self.bank_branch
        bank_reference = self.bank_reference
        account_name = self.account_name
        account_number = self.account_number
        sort_code = self.sort_code
        note = self.note

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if bank_name is not UNSET:
            field_dict["bankName"] = bank_name
        if bank_branch is not UNSET:
            field_dict["bankBranch"] = bank_branch
        if bank_reference is not UNSET:
            field_dict["bankReference"] = bank_reference
        if account_name is not UNSET:
            field_dict["accountName"] = account_name
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bank_name = d.pop("bankName", UNSET)

        bank_branch = d.pop("bankBranch", UNSET)

        bank_reference = d.pop("bankReference", UNSET)

        account_name = d.pop("accountName", UNSET)

        account_number = d.pop("accountNumber", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        note = d.pop("note", UNSET)

        bank_details = cls(
            bank_name=bank_name,
            bank_branch=bank_branch,
            bank_reference=bank_reference,
            account_name=account_name,
            account_number=account_number,
            sort_code=sort_code,
            note=note,
        )

        return bank_details
