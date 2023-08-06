from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportResponse")


@attr.s(auto_attribs=True)
class ReportResponse:
    """Used to encapsulate a response for any of the reports.
    See the Introduction Guide for Reports for more details

        Attributes:
            type (Union[Unset, None, str]): [readonly] The content-type, this would usually be the same as the accept header
                you provided when you requested the report
            content (Union[Unset, None, str]): [readonly] This could contain a link to a PDF file, HTML content or other
                content, depending on the Type value.
            model (Union[Unset, Any]): [readonly] If the type is application.json then this will contain a JSON
                representation of the relevant model
    """

    type: Union[Unset, None, str] = UNSET
    content: Union[Unset, None, str] = UNSET
    model: Union[Unset, Any] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        content = self.content
        model = self.model

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if content is not UNSET:
            field_dict["content"] = content
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        content = d.pop("content", UNSET)

        model = d.pop("model", UNSET)

        report_response = cls(
            type=type,
            content=content,
            model=model,
        )

        return report_response
