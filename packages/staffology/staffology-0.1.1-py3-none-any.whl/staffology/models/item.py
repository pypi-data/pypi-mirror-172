from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Item")


@attr.s(auto_attribs=True)
class Item:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, None, str]):
        metadata (Union[Unset, Any]):
        url (Union[Unset, None, str]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    url: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        metadata = self.metadata
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        metadata = d.pop("metadata", UNSET)

        url = d.pop("url", UNSET)

        item = cls(
            id=id,
            name=name,
            metadata=metadata,
            url=url,
        )

        return item
