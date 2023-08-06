from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.p11d_single_item import P11DSingleItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DExpenses")


@attr.s(auto_attribs=True)
class P11DExpenses:
    """
    Attributes:
        trav_and_sub (Union[Unset, P11DSingleItem]):
        ent (Union[Unset, P11DSingleItem]):
        home_tel (Union[Unset, P11DSingleItem]):
        non_qual_rel (Union[Unset, P11DSingleItem]):
        other (Union[Unset, P11DSingleItem]):
        type_letter (Union[Unset, None, str]):
    """

    trav_and_sub: Union[Unset, P11DSingleItem] = UNSET
    ent: Union[Unset, P11DSingleItem] = UNSET
    home_tel: Union[Unset, P11DSingleItem] = UNSET
    non_qual_rel: Union[Unset, P11DSingleItem] = UNSET
    other: Union[Unset, P11DSingleItem] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        trav_and_sub: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trav_and_sub, Unset):
            trav_and_sub = self.trav_and_sub.to_dict()

        ent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ent, Unset):
            ent = self.ent.to_dict()

        home_tel: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.home_tel, Unset):
            home_tel = self.home_tel.to_dict()

        non_qual_rel: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.non_qual_rel, Unset):
            non_qual_rel = self.non_qual_rel.to_dict()

        other: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.other, Unset):
            other = self.other.to_dict()

        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if trav_and_sub is not UNSET:
            field_dict["travAndSub"] = trav_and_sub
        if ent is not UNSET:
            field_dict["ent"] = ent
        if home_tel is not UNSET:
            field_dict["homeTel"] = home_tel
        if non_qual_rel is not UNSET:
            field_dict["nonQualRel"] = non_qual_rel
        if other is not UNSET:
            field_dict["other"] = other
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _trav_and_sub = d.pop("travAndSub", UNSET)
        trav_and_sub: Union[Unset, P11DSingleItem]
        if isinstance(_trav_and_sub, Unset):
            trav_and_sub = UNSET
        else:
            trav_and_sub = P11DSingleItem.from_dict(_trav_and_sub)

        _ent = d.pop("ent", UNSET)
        ent: Union[Unset, P11DSingleItem]
        if isinstance(_ent, Unset):
            ent = UNSET
        else:
            ent = P11DSingleItem.from_dict(_ent)

        _home_tel = d.pop("homeTel", UNSET)
        home_tel: Union[Unset, P11DSingleItem]
        if isinstance(_home_tel, Unset):
            home_tel = UNSET
        else:
            home_tel = P11DSingleItem.from_dict(_home_tel)

        _non_qual_rel = d.pop("nonQualRel", UNSET)
        non_qual_rel: Union[Unset, P11DSingleItem]
        if isinstance(_non_qual_rel, Unset):
            non_qual_rel = UNSET
        else:
            non_qual_rel = P11DSingleItem.from_dict(_non_qual_rel)

        _other = d.pop("other", UNSET)
        other: Union[Unset, P11DSingleItem]
        if isinstance(_other, Unset):
            other = UNSET
        else:
            other = P11DSingleItem.from_dict(_other)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_expenses = cls(
            trav_and_sub=trav_and_sub,
            ent=ent,
            home_tel=home_tel,
            non_qual_rel=non_qual_rel,
            other=other,
            type_letter=type_letter,
        )

        return p11d_expenses
