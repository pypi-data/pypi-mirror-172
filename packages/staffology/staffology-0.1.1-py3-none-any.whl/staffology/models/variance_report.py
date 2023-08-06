from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.gross_to_net_report import GrossToNetReport
from ..models.gross_to_net_report_line import GrossToNetReportLine
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="VarianceReport")


@attr.s(auto_attribs=True)
class VarianceReport:
    """
    Attributes:
        show_difference_as_percentage (Union[Unset, bool]):
        minimum_change_percentage (Union[Unset, float]):
        primary (Union[Unset, GrossToNetReport]):
        secondary (Union[Unset, GrossToNetReport]):
        joiners (Union[Unset, None, List[GrossToNetReportLine]]):
        leavers (Union[Unset, None, List[GrossToNetReportLine]]):
        has_departments (Union[Unset, bool]):
        common_lines (Union[Unset, None, List[GrossToNetReportLine]]):
        has_variances (Union[Unset, bool]):
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
    """

    show_difference_as_percentage: Union[Unset, bool] = UNSET
    minimum_change_percentage: Union[Unset, float] = UNSET
    primary: Union[Unset, GrossToNetReport] = UNSET
    secondary: Union[Unset, GrossToNetReport] = UNSET
    joiners: Union[Unset, None, List[GrossToNetReportLine]] = UNSET
    leavers: Union[Unset, None, List[GrossToNetReportLine]] = UNSET
    has_departments: Union[Unset, bool] = UNSET
    common_lines: Union[Unset, None, List[GrossToNetReportLine]] = UNSET
    has_variances: Union[Unset, bool] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        show_difference_as_percentage = self.show_difference_as_percentage
        minimum_change_percentage = self.minimum_change_percentage
        primary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.primary, Unset):
            primary = self.primary.to_dict()

        secondary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.secondary, Unset):
            secondary = self.secondary.to_dict()

        joiners: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.joiners, Unset):
            if self.joiners is None:
                joiners = None
            else:
                joiners = []
                for joiners_item_data in self.joiners:
                    joiners_item = joiners_item_data.to_dict()

                    joiners.append(joiners_item)

        leavers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.leavers, Unset):
            if self.leavers is None:
                leavers = None
            else:
                leavers = []
                for leavers_item_data in self.leavers:
                    leavers_item = leavers_item_data.to_dict()

                    leavers.append(leavers_item)

        has_departments = self.has_departments
        common_lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.common_lines, Unset):
            if self.common_lines is None:
                common_lines = None
            else:
                common_lines = []
                for common_lines_item_data in self.common_lines:
                    common_lines_item = common_lines_item_data.to_dict()

                    common_lines.append(common_lines_item)

        has_variances = self.has_variances
        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if show_difference_as_percentage is not UNSET:
            field_dict["showDifferenceAsPercentage"] = show_difference_as_percentage
        if minimum_change_percentage is not UNSET:
            field_dict["minimumChangePercentage"] = minimum_change_percentage
        if primary is not UNSET:
            field_dict["primary"] = primary
        if secondary is not UNSET:
            field_dict["secondary"] = secondary
        if joiners is not UNSET:
            field_dict["joiners"] = joiners
        if leavers is not UNSET:
            field_dict["leavers"] = leavers
        if has_departments is not UNSET:
            field_dict["hasDepartments"] = has_departments
        if common_lines is not UNSET:
            field_dict["commonLines"] = common_lines
        if has_variances is not UNSET:
            field_dict["hasVariances"] = has_variances
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        show_difference_as_percentage = d.pop("showDifferenceAsPercentage", UNSET)

        minimum_change_percentage = d.pop("minimumChangePercentage", UNSET)

        _primary = d.pop("primary", UNSET)
        primary: Union[Unset, GrossToNetReport]
        if isinstance(_primary, Unset):
            primary = UNSET
        else:
            primary = GrossToNetReport.from_dict(_primary)

        _secondary = d.pop("secondary", UNSET)
        secondary: Union[Unset, GrossToNetReport]
        if isinstance(_secondary, Unset):
            secondary = UNSET
        else:
            secondary = GrossToNetReport.from_dict(_secondary)

        joiners = []
        _joiners = d.pop("joiners", UNSET)
        for joiners_item_data in _joiners or []:
            joiners_item = GrossToNetReportLine.from_dict(joiners_item_data)

            joiners.append(joiners_item)

        leavers = []
        _leavers = d.pop("leavers", UNSET)
        for leavers_item_data in _leavers or []:
            leavers_item = GrossToNetReportLine.from_dict(leavers_item_data)

            leavers.append(leavers_item)

        has_departments = d.pop("hasDepartments", UNSET)

        common_lines = []
        _common_lines = d.pop("commonLines", UNSET)
        for common_lines_item_data in _common_lines or []:
            common_lines_item = GrossToNetReportLine.from_dict(common_lines_item_data)

            common_lines.append(common_lines_item)

        has_variances = d.pop("hasVariances", UNSET)

        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = Report(_report)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        variance_report = cls(
            show_difference_as_percentage=show_difference_as_percentage,
            minimum_change_percentage=minimum_change_percentage,
            primary=primary,
            secondary=secondary,
            joiners=joiners,
            leavers=leavers,
            has_departments=has_departments,
            common_lines=common_lines,
            has_variances=has_variances,
            report=report,
            tax_year=tax_year,
        )

        return variance_report
