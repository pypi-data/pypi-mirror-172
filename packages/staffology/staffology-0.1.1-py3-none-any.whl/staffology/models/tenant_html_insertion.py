from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.html_insertion_point import HtmlInsertionPoint
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantHtmlInsertion")


@attr.s(auto_attribs=True)
class TenantHtmlInsertion:
    """
    Attributes:
        insertion_point (Union[Unset, HtmlInsertionPoint]):
        content (Union[Unset, None, str]):
    """

    insertion_point: Union[Unset, HtmlInsertionPoint] = UNSET
    content: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        insertion_point: Union[Unset, str] = UNSET
        if not isinstance(self.insertion_point, Unset):
            insertion_point = self.insertion_point.value

        content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if insertion_point is not UNSET:
            field_dict["insertionPoint"] = insertion_point
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _insertion_point = d.pop("insertionPoint", UNSET)
        insertion_point: Union[Unset, HtmlInsertionPoint]
        if isinstance(_insertion_point, Unset):
            insertion_point = UNSET
        else:
            insertion_point = HtmlInsertionPoint(_insertion_point)

        content = d.pop("content", UNSET)

        tenant_html_insertion = cls(
            insertion_point=insertion_point,
            content=content,
        )

        return tenant_html_insertion
