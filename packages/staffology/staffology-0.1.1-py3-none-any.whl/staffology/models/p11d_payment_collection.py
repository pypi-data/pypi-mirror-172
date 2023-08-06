from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.p11d_desc_other import P11DDescOther
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DPaymentCollection")


@attr.s(auto_attribs=True)
class P11DPaymentCollection:
    """
    Attributes:
        payment (Union[Unset, None, List[P11DDescOther]]):
        tax (Union[Unset, None, str]):
        type_letter (Union[Unset, None, str]):
    """

    payment: Union[Unset, None, List[P11DDescOther]] = UNSET
    tax: Union[Unset, None, str] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payment: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.payment, Unset):
            if self.payment is None:
                payment = None
            else:
                payment = []
                for payment_item_data in self.payment:
                    payment_item = payment_item_data.to_dict()

                    payment.append(payment_item)

        tax = self.tax
        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if payment is not UNSET:
            field_dict["payment"] = payment
        if tax is not UNSET:
            field_dict["tax"] = tax
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payment = []
        _payment = d.pop("payment", UNSET)
        for payment_item_data in _payment or []:
            payment_item = P11DDescOther.from_dict(payment_item_data)

            payment.append(payment_item)

        tax = d.pop("tax", UNSET)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_payment_collection = cls(
            payment=payment,
            tax=tax,
            type_letter=type_letter,
        )

        return p11d_payment_collection
