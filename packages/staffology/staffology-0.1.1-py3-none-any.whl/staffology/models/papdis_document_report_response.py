from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.papdis_document import PapdisDocument
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisDocumentReportResponse")


@attr.s(auto_attribs=True)
class PapdisDocumentReportResponse:
    """Used to encapsulate a response for any of the reports.
    See the Introduction Guide for Reports for more details

        Attributes:
            type (Union[Unset, None, str]): [readonly] The content-type, this would usually be the same as the accept header
                you provided when you requested the report
            content (Union[Unset, None, str]): [readonly] This could contain a link to a PDF file, HTML content or other
                content, depending on the Type value.
            model (Union[Unset, PapdisDocument]): PAPDIS stands for 'Payroll and Pension Data Interface Standard'.
                It is an industry standard for exchanging data between payroll software and pension providers.
                Our system provides an export of data in this standard and these models are used to represent the data.
                Whilst the relevant reporting API endpoint can provide this data as a JSON entity, it is usually represented in
                CSV or XML format which our API also provides.
    """

    type: Union[Unset, None, str] = UNSET
    content: Union[Unset, None, str] = UNSET
    model: Union[Unset, PapdisDocument] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        content = self.content
        model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

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

        _model = d.pop("model", UNSET)
        model: Union[Unset, PapdisDocument]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = PapdisDocument.from_dict(_model)

        papdis_document_report_response = cls(
            type=type,
            content=content,
            model=model,
        )

        return papdis_document_report_response
