import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.p11_detailed_ni_values import P11DetailedNiValues
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11NiAndStatPaymentsLine")


@attr.s(auto_attribs=True)
class P11NiAndStatPaymentsLine:
    """Lines for the NI Contributions and Statutory Payments table in the P11 Detailed Report

    Attributes:
        date (Union[Unset, datetime.date]): [readonly]
        period (Union[Unset, None, str]): [readonly]
        month_number (Union[Unset, None, str]): [readonly]
        week_number (Union[Unset, None, str]): [readonly]
        smp (Union[Unset, float]): [readonly]
        spp (Union[Unset, float]): [readonly]
        sap (Union[Unset, float]): [readonly]
        shpp (Union[Unset, float]): [readonly]
        ssp (Union[Unset, float]): [readonly]
        spbp (Union[Unset, float]): [readonly]
        class1a (Union[Unset, float]): [readonly]
        ni_values (Union[Unset, P11DetailedNiValues]): Forms the NI Summary table in the P11 Detailed report.
        tax_code (Union[Unset, None, str]): [readonly]
    """

    date: Union[Unset, datetime.date] = UNSET
    period: Union[Unset, None, str] = UNSET
    month_number: Union[Unset, None, str] = UNSET
    week_number: Union[Unset, None, str] = UNSET
    smp: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    ssp: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET
    class1a: Union[Unset, float] = UNSET
    ni_values: Union[Unset, P11DetailedNiValues] = UNSET
    tax_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        period = self.period
        month_number = self.month_number
        week_number = self.week_number
        smp = self.smp
        spp = self.spp
        sap = self.sap
        shpp = self.shpp
        ssp = self.ssp
        spbp = self.spbp
        class1a = self.class1a
        ni_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ni_values, Unset):
            ni_values = self.ni_values.to_dict()

        tax_code = self.tax_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if period is not UNSET:
            field_dict["period"] = period
        if month_number is not UNSET:
            field_dict["monthNumber"] = month_number
        if week_number is not UNSET:
            field_dict["weekNumber"] = week_number
        if smp is not UNSET:
            field_dict["smp"] = smp
        if spp is not UNSET:
            field_dict["spp"] = spp
        if sap is not UNSET:
            field_dict["sap"] = sap
        if shpp is not UNSET:
            field_dict["shpp"] = shpp
        if ssp is not UNSET:
            field_dict["ssp"] = ssp
        if spbp is not UNSET:
            field_dict["spbp"] = spbp
        if class1a is not UNSET:
            field_dict["class1a"] = class1a
        if ni_values is not UNSET:
            field_dict["niValues"] = ni_values
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        period = d.pop("period", UNSET)

        month_number = d.pop("monthNumber", UNSET)

        week_number = d.pop("weekNumber", UNSET)

        smp = d.pop("smp", UNSET)

        spp = d.pop("spp", UNSET)

        sap = d.pop("sap", UNSET)

        shpp = d.pop("shpp", UNSET)

        ssp = d.pop("ssp", UNSET)

        spbp = d.pop("spbp", UNSET)

        class1a = d.pop("class1a", UNSET)

        _ni_values = d.pop("niValues", UNSET)
        ni_values: Union[Unset, P11DetailedNiValues]
        if isinstance(_ni_values, Unset):
            ni_values = UNSET
        else:
            ni_values = P11DetailedNiValues.from_dict(_ni_values)

        tax_code = d.pop("taxCode", UNSET)

        p11_ni_and_stat_payments_line = cls(
            date=date,
            period=period,
            month_number=month_number,
            week_number=week_number,
            smp=smp,
            spp=spp,
            sap=sap,
            shpp=shpp,
            ssp=ssp,
            spbp=spbp,
            class1a=class1a,
            ni_values=ni_values,
            tax_code=tax_code,
        )

        return p11_ni_and_stat_payments_line
