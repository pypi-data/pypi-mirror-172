from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldModification")


@attr.s(auto_attribs=True)
class FieldModification:
    """
    Attributes:
        field_name (Union[Unset, None, str]):
        is_significant (Union[Unset, bool]):
        old_value (Union[Unset, None, str]):
        new_value (Union[Unset, None, str]):
    """

    field_name: Union[Unset, None, str] = UNSET
    is_significant: Union[Unset, bool] = UNSET
    old_value: Union[Unset, None, str] = UNSET
    new_value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_name = self.field_name
        is_significant = self.is_significant
        old_value = self.old_value
        new_value = self.new_value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if field_name is not UNSET:
            field_dict["fieldName"] = field_name
        if is_significant is not UNSET:
            field_dict["isSignificant"] = is_significant
        if old_value is not UNSET:
            field_dict["oldValue"] = old_value
        if new_value is not UNSET:
            field_dict["newValue"] = new_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_name = d.pop("fieldName", UNSET)

        is_significant = d.pop("isSignificant", UNSET)

        old_value = d.pop("oldValue", UNSET)

        new_value = d.pop("newValue", UNSET)

        field_modification = cls(
            field_name=field_name,
            is_significant=is_significant,
            old_value=old_value,
            new_value=new_value,
        )

        return field_modification
