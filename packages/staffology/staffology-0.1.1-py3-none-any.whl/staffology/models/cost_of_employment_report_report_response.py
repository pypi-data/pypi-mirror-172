from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cost_of_employment_report import CostOfEmploymentReport
from ..types import UNSET, Unset

T = TypeVar("T", bound="CostOfEmploymentReportReportResponse")


@attr.s(auto_attribs=True)
class CostOfEmploymentReportReportResponse:
    """Used to encapsulate a response for any of the reports.
    See the Introduction Guide for Reports for more details

        Attributes:
            type (Union[Unset, None, str]): [readonly] The content-type, this would usually be the same as the accept header
                you provided when you requested the report
            content (Union[Unset, None, str]): [readonly] This could contain a link to a PDF file, HTML content or other
                content, depending on the Type value.
            model (Union[Unset, CostOfEmploymentReport]):
    """

    type: Union[Unset, None, str] = UNSET
    content: Union[Unset, None, str] = UNSET
    model: Union[Unset, CostOfEmploymentReport] = UNSET

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
        model: Union[Unset, CostOfEmploymentReport]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = CostOfEmploymentReport.from_dict(_model)

        cost_of_employment_report_report_response = cls(
            type=type,
            content=content,
            model=model,
        )

        return cost_of_employment_report_report_response
