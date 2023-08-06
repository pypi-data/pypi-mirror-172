from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UtmInfo")


@attr.s(auto_attribs=True)
class UtmInfo:
    """
    Attributes:
        source (Union[Unset, None, str]):
        medium (Union[Unset, None, str]):
        term (Union[Unset, None, str]):
        content (Union[Unset, None, str]):
        campaign (Union[Unset, None, str]):
    """

    source: Union[Unset, None, str] = UNSET
    medium: Union[Unset, None, str] = UNSET
    term: Union[Unset, None, str] = UNSET
    content: Union[Unset, None, str] = UNSET
    campaign: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        source = self.source
        medium = self.medium
        term = self.term
        content = self.content
        campaign = self.campaign

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if medium is not UNSET:
            field_dict["medium"] = medium
        if term is not UNSET:
            field_dict["term"] = term
        if content is not UNSET:
            field_dict["content"] = content
        if campaign is not UNSET:
            field_dict["campaign"] = campaign

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = d.pop("source", UNSET)

        medium = d.pop("medium", UNSET)

        term = d.pop("term", UNSET)

        content = d.pop("content", UNSET)

        campaign = d.pop("campaign", UNSET)

        utm_info = cls(
            source=source,
            medium=medium,
            term=term,
            content=content,
            campaign=campaign,
        )

        return utm_info
