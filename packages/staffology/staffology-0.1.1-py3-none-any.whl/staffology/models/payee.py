from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.bank_details import BankDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Payee")


@attr.s(auto_attribs=True)
class Payee:
    """
    Attributes:
        title (str): The name of this Payee
        bank_details (Union[Unset, BankDetails]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: str
    bank_details: Union[Unset, BankDetails] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        bank_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = self.bank_details.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "title": title,
            }
        )
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        _bank_details = d.pop("bankDetails", UNSET)
        bank_details: Union[Unset, BankDetails]
        if isinstance(_bank_details, Unset):
            bank_details = UNSET
        else:
            bank_details = BankDetails.from_dict(_bank_details)

        id = d.pop("id", UNSET)

        payee = cls(
            title=title,
            bank_details=bank_details,
            id=id,
        )

        return payee
