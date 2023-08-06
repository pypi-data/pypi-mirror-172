from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeNIlettersAndValues")


@attr.s(auto_attribs=True)
class FpsEmployeeNIlettersAndValues:
    """
    Attributes:
        n_iletter (Union[Unset, None, str]):
        gross_earnings_for_ni_cs_in_pd (Union[Unset, None, str]):
        gross_earnings_for_ni_cs_ytd (Union[Unset, None, str]):
        at_lelytd (Union[Unset, None, str]):
        le_lto_ptytd (Union[Unset, None, str]):
        p_tto_uelytd (Union[Unset, None, str]):
        total_emp_nic_in_pd (Union[Unset, None, str]):
        total_emp_nicytd (Union[Unset, None, str]):
        empee_contribns_in_pd (Union[Unset, None, str]):
        empee_contribns_ytd (Union[Unset, None, str]):
    """

    n_iletter: Union[Unset, None, str] = UNSET
    gross_earnings_for_ni_cs_in_pd: Union[Unset, None, str] = UNSET
    gross_earnings_for_ni_cs_ytd: Union[Unset, None, str] = UNSET
    at_lelytd: Union[Unset, None, str] = UNSET
    le_lto_ptytd: Union[Unset, None, str] = UNSET
    p_tto_uelytd: Union[Unset, None, str] = UNSET
    total_emp_nic_in_pd: Union[Unset, None, str] = UNSET
    total_emp_nicytd: Union[Unset, None, str] = UNSET
    empee_contribns_in_pd: Union[Unset, None, str] = UNSET
    empee_contribns_ytd: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        n_iletter = self.n_iletter
        gross_earnings_for_ni_cs_in_pd = self.gross_earnings_for_ni_cs_in_pd
        gross_earnings_for_ni_cs_ytd = self.gross_earnings_for_ni_cs_ytd
        at_lelytd = self.at_lelytd
        le_lto_ptytd = self.le_lto_ptytd
        p_tto_uelytd = self.p_tto_uelytd
        total_emp_nic_in_pd = self.total_emp_nic_in_pd
        total_emp_nicytd = self.total_emp_nicytd
        empee_contribns_in_pd = self.empee_contribns_in_pd
        empee_contribns_ytd = self.empee_contribns_ytd

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if n_iletter is not UNSET:
            field_dict["nIletter"] = n_iletter
        if gross_earnings_for_ni_cs_in_pd is not UNSET:
            field_dict["grossEarningsForNICsInPd"] = gross_earnings_for_ni_cs_in_pd
        if gross_earnings_for_ni_cs_ytd is not UNSET:
            field_dict["grossEarningsForNICsYTD"] = gross_earnings_for_ni_cs_ytd
        if at_lelytd is not UNSET:
            field_dict["atLELYTD"] = at_lelytd
        if le_lto_ptytd is not UNSET:
            field_dict["leLtoPTYTD"] = le_lto_ptytd
        if p_tto_uelytd is not UNSET:
            field_dict["pTtoUELYTD"] = p_tto_uelytd
        if total_emp_nic_in_pd is not UNSET:
            field_dict["totalEmpNICInPd"] = total_emp_nic_in_pd
        if total_emp_nicytd is not UNSET:
            field_dict["totalEmpNICYTD"] = total_emp_nicytd
        if empee_contribns_in_pd is not UNSET:
            field_dict["empeeContribnsInPd"] = empee_contribns_in_pd
        if empee_contribns_ytd is not UNSET:
            field_dict["empeeContribnsYTD"] = empee_contribns_ytd

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        n_iletter = d.pop("nIletter", UNSET)

        gross_earnings_for_ni_cs_in_pd = d.pop("grossEarningsForNICsInPd", UNSET)

        gross_earnings_for_ni_cs_ytd = d.pop("grossEarningsForNICsYTD", UNSET)

        at_lelytd = d.pop("atLELYTD", UNSET)

        le_lto_ptytd = d.pop("leLtoPTYTD", UNSET)

        p_tto_uelytd = d.pop("pTtoUELYTD", UNSET)

        total_emp_nic_in_pd = d.pop("totalEmpNICInPd", UNSET)

        total_emp_nicytd = d.pop("totalEmpNICYTD", UNSET)

        empee_contribns_in_pd = d.pop("empeeContribnsInPd", UNSET)

        empee_contribns_ytd = d.pop("empeeContribnsYTD", UNSET)

        fps_employee_n_iletters_and_values = cls(
            n_iletter=n_iletter,
            gross_earnings_for_ni_cs_in_pd=gross_earnings_for_ni_cs_in_pd,
            gross_earnings_for_ni_cs_ytd=gross_earnings_for_ni_cs_ytd,
            at_lelytd=at_lelytd,
            le_lto_ptytd=le_lto_ptytd,
            p_tto_uelytd=p_tto_uelytd,
            total_emp_nic_in_pd=total_emp_nic_in_pd,
            total_emp_nicytd=total_emp_nicytd,
            empee_contribns_in_pd=empee_contribns_in_pd,
            empee_contribns_ytd=empee_contribns_ytd,
        )

        return fps_employee_n_iletters_and_values
