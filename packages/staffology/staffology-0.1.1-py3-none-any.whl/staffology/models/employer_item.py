from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.role import Role
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerItem")


@attr.s(auto_attribs=True)
class EmployerItem:
    """
    Attributes:
        is_owner (Union[Unset, bool]):
        role (Union[Unset, Role]):
        id (Union[Unset, str]):
        name (Union[Unset, None, str]):
        metadata (Union[Unset, Any]):
        url (Union[Unset, None, str]):
    """

    is_owner: Union[Unset, bool] = UNSET
    role: Union[Unset, Role] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    metadata: Union[Unset, Any] = UNSET
    url: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_owner = self.is_owner
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        id = self.id
        name = self.name
        metadata = self.metadata
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_owner is not UNSET:
            field_dict["isOwner"] = is_owner
        if role is not UNSET:
            field_dict["role"] = role
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
        is_owner = d.pop("isOwner", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, Role]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = Role(_role)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        metadata = d.pop("metadata", UNSET)

        url = d.pop("url", UNSET)

        employer_item = cls(
            is_owner=is_owner,
            role=role,
            id=id,
            name=name,
            metadata=metadata,
            url=url,
        )

        return employer_item
