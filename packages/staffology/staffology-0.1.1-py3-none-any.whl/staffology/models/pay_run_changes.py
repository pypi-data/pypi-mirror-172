from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunChanges")


@attr.s(auto_attribs=True)
class PayRunChanges:
    """
    Attributes:
        pay_run_entries (Union[Unset, None, List[Item]]): A list of PayRunEntries where the PayRunEntry itself has been
            modified and.or the related Employee record was changed
    """

    pay_run_entries: Union[Unset, None, List[Item]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        pay_run_entries: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.pay_run_entries, Unset):
            if self.pay_run_entries is None:
                pay_run_entries = None
            else:
                pay_run_entries = []
                for pay_run_entries_item_data in self.pay_run_entries:
                    pay_run_entries_item = pay_run_entries_item_data.to_dict()

                    pay_run_entries.append(pay_run_entries_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if pay_run_entries is not UNSET:
            field_dict["payRunEntries"] = pay_run_entries

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pay_run_entries = []
        _pay_run_entries = d.pop("payRunEntries", UNSET)
        for pay_run_entries_item_data in _pay_run_entries or []:
            pay_run_entries_item = Item.from_dict(pay_run_entries_item_data)

            pay_run_entries.append(pay_run_entries_item)

        pay_run_changes = cls(
            pay_run_entries=pay_run_entries,
        )

        return pay_run_changes
