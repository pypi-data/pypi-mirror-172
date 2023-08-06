from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.analysis_report_line_value import AnalysisReportLineValue
from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisReportLine")


@attr.s(auto_attribs=True)
class AnalysisReportLine:
    """
    Attributes:
        employee (Union[Unset, Item]):
        gross (Union[Unset, float]):
        niable_gross (Union[Unset, float]):
        pensionable_gross (Union[Unset, float]):
        net (Union[Unset, float]):
        take_home (Union[Unset, float]):
        employer_nic (Union[Unset, float]):
        employer_pension (Union[Unset, float]):
        show_qty_column (Union[Unset, bool]):
        lines (Union[Unset, None, List[AnalysisReportLineValue]]):
    """

    employee: Union[Unset, Item] = UNSET
    gross: Union[Unset, float] = UNSET
    niable_gross: Union[Unset, float] = UNSET
    pensionable_gross: Union[Unset, float] = UNSET
    net: Union[Unset, float] = UNSET
    take_home: Union[Unset, float] = UNSET
    employer_nic: Union[Unset, float] = UNSET
    employer_pension: Union[Unset, float] = UNSET
    show_qty_column: Union[Unset, bool] = UNSET
    lines: Union[Unset, None, List[AnalysisReportLineValue]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        gross = self.gross
        niable_gross = self.niable_gross
        pensionable_gross = self.pensionable_gross
        net = self.net
        take_home = self.take_home
        employer_nic = self.employer_nic
        employer_pension = self.employer_pension
        show_qty_column = self.show_qty_column
        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee is not UNSET:
            field_dict["employee"] = employee
        if gross is not UNSET:
            field_dict["gross"] = gross
        if niable_gross is not UNSET:
            field_dict["niableGross"] = niable_gross
        if pensionable_gross is not UNSET:
            field_dict["pensionableGross"] = pensionable_gross
        if net is not UNSET:
            field_dict["net"] = net
        if take_home is not UNSET:
            field_dict["takeHome"] = take_home
        if employer_nic is not UNSET:
            field_dict["employerNic"] = employer_nic
        if employer_pension is not UNSET:
            field_dict["employerPension"] = employer_pension
        if show_qty_column is not UNSET:
            field_dict["showQtyColumn"] = show_qty_column
        if lines is not UNSET:
            field_dict["lines"] = lines

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        gross = d.pop("gross", UNSET)

        niable_gross = d.pop("niableGross", UNSET)

        pensionable_gross = d.pop("pensionableGross", UNSET)

        net = d.pop("net", UNSET)

        take_home = d.pop("takeHome", UNSET)

        employer_nic = d.pop("employerNic", UNSET)

        employer_pension = d.pop("employerPension", UNSET)

        show_qty_column = d.pop("showQtyColumn", UNSET)

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = AnalysisReportLineValue.from_dict(lines_item_data)

            lines.append(lines_item)

        analysis_report_line = cls(
            employee=employee,
            gross=gross,
            niable_gross=niable_gross,
            pensionable_gross=pensionable_gross,
            net=net,
            take_home=take_home,
            employer_nic=employer_nic,
            employer_pension=employer_pension,
            show_qty_column=show_qty_column,
            lines=lines,
        )

        return analysis_report_line
