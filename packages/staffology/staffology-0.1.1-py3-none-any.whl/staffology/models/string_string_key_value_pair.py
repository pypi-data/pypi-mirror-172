from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StringStringKeyValuePair")


@attr.s(auto_attribs=True)
class StringStringKeyValuePair:
    """
    Attributes:
        key (Union[Unset, None, str]):
        value (Union[Unset, None, str]):
    """

    key: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        value = d.pop("value", UNSET)

        string_string_key_value_pair = cls(
            key=key,
            value=value,
        )

        return string_string_key_value_pair
