from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.report import Report
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportPack")


@attr.s(auto_attribs=True)
class ReportPack:
    """A ReportPack is used to group together a number of reports

    Attributes:
        title (str): The name of this ReportPack
        reports (Union[Unset, None, List[Report]]): The Reports included in this ReportPack
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: str
    reports: Union[Unset, None, List[Report]] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        reports: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.reports, Unset):
            if self.reports is None:
                reports = None
            else:
                reports = []
                for reports_item_data in self.reports:
                    reports_item = reports_item_data.value

                    reports.append(reports_item)

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "title": title,
            }
        )
        if reports is not UNSET:
            field_dict["reports"] = reports
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in _reports or []:
            reports_item = Report(reports_item_data)

            reports.append(reports_item)

        id = d.pop("id", UNSET)

        report_pack = cls(
            title=title,
            reports=reports,
            id=id,
        )

        return report_pack
