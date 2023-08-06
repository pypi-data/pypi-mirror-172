from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.hmrc_liability import HmrcLiability
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="P32")


@attr.s(auto_attribs=True)
class P32:
    """
    Attributes:
        is_quarterly (Union[Unset, bool]): [readonly]
        hmrc_liabilities (Union[Unset, None, List[HmrcLiability]]): [readonly]
        report (Union[Unset, Report]):
        tax_year (Union[Unset, TaxYear]):
    """

    is_quarterly: Union[Unset, bool] = UNSET
    hmrc_liabilities: Union[Unset, None, List[HmrcLiability]] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_quarterly = self.is_quarterly
        hmrc_liabilities: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.hmrc_liabilities, Unset):
            if self.hmrc_liabilities is None:
                hmrc_liabilities = None
            else:
                hmrc_liabilities = []
                for hmrc_liabilities_item_data in self.hmrc_liabilities:
                    hmrc_liabilities_item = hmrc_liabilities_item_data.to_dict()

                    hmrc_liabilities.append(hmrc_liabilities_item)

        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_quarterly is not UNSET:
            field_dict["isQuarterly"] = is_quarterly
        if hmrc_liabilities is not UNSET:
            field_dict["hmrcLiabilities"] = hmrc_liabilities
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_quarterly = d.pop("isQuarterly", UNSET)

        hmrc_liabilities = []
        _hmrc_liabilities = d.pop("hmrcLiabilities", UNSET)
        for hmrc_liabilities_item_data in _hmrc_liabilities or []:
            hmrc_liabilities_item = HmrcLiability.from_dict(hmrc_liabilities_item_data)

            hmrc_liabilities.append(hmrc_liabilities_item)

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

        p32 = cls(
            is_quarterly=is_quarterly,
            hmrc_liabilities=hmrc_liabilities,
            report=report,
            tax_year=tax_year,
        )

        return p32
