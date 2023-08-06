from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.p11d_loan import P11DLoan
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DLoanCollection")


@attr.s(auto_attribs=True)
class P11DLoanCollection:
    """
    Attributes:
        loan (Union[Unset, None, List[P11DLoan]]):
        type_letter (Union[Unset, None, str]):
    """

    loan: Union[Unset, None, List[P11DLoan]] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        loan: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.loan, Unset):
            if self.loan is None:
                loan = None
            else:
                loan = []
                for loan_item_data in self.loan:
                    loan_item = loan_item_data.to_dict()

                    loan.append(loan_item)

        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if loan is not UNSET:
            field_dict["loan"] = loan
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        loan = []
        _loan = d.pop("loan", UNSET)
        for loan_item_data in _loan or []:
            loan_item = P11DLoan.from_dict(loan_item_data)

            loan.append(loan_item)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_loan_collection = cls(
            loan=loan,
            type_letter=type_letter,
        )

        return p11d_loan_collection
