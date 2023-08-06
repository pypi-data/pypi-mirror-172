from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="Post")


@attr.s(auto_attribs=True)
class Post:
    """
    Attributes:
        title (Union[Unset, None, str]): Title of the Post
        is_primary (Union[Unset, bool]): Set to True if this is Primary post of the Employee
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: Union[Unset, None, str] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        is_primary = self.is_primary
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if is_primary is not UNSET:
            field_dict["isPrimary"] = is_primary
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        is_primary = d.pop("isPrimary", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        post = cls(
            title=title,
            is_primary=is_primary,
            employee=employee,
            id=id,
        )

        return post
