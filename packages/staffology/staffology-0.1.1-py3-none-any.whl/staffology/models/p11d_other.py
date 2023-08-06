from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.p11d_desc_other import P11DDescOther
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DOther")


@attr.s(auto_attribs=True)
class P11DOther:
    """
    Attributes:
        class_1a (Union[Unset, None, List[P11DDescOther]]):
        non_class_1a (Union[Unset, None, List[P11DDescOther]]):
        tax_paid (Union[Unset, None, str]):
        type_letter (Union[Unset, None, str]):
    """

    class_1a: Union[Unset, None, List[P11DDescOther]] = UNSET
    non_class_1a: Union[Unset, None, List[P11DDescOther]] = UNSET
    tax_paid: Union[Unset, None, str] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        class_1a: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.class_1a, Unset):
            if self.class_1a is None:
                class_1a = None
            else:
                class_1a = []
                for class_1a_item_data in self.class_1a:
                    class_1a_item = class_1a_item_data.to_dict()

                    class_1a.append(class_1a_item)

        non_class_1a: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.non_class_1a, Unset):
            if self.non_class_1a is None:
                non_class_1a = None
            else:
                non_class_1a = []
                for non_class_1a_item_data in self.non_class_1a:
                    non_class_1a_item = non_class_1a_item_data.to_dict()

                    non_class_1a.append(non_class_1a_item)

        tax_paid = self.tax_paid
        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if class_1a is not UNSET:
            field_dict["class1A"] = class_1a
        if non_class_1a is not UNSET:
            field_dict["nonClass1A"] = non_class_1a
        if tax_paid is not UNSET:
            field_dict["taxPaid"] = tax_paid
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        class_1a = []
        _class_1a = d.pop("class1A", UNSET)
        for class_1a_item_data in _class_1a or []:
            class_1a_item = P11DDescOther.from_dict(class_1a_item_data)

            class_1a.append(class_1a_item)

        non_class_1a = []
        _non_class_1a = d.pop("nonClass1A", UNSET)
        for non_class_1a_item_data in _non_class_1a or []:
            non_class_1a_item = P11DDescOther.from_dict(non_class_1a_item_data)

            non_class_1a.append(non_class_1a_item)

        tax_paid = d.pop("taxPaid", UNSET)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_other = cls(
            class_1a=class_1a,
            non_class_1a=non_class_1a,
            tax_paid=tax_paid,
            type_letter=type_letter,
        )

        return p11d_other
