from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DetailedNiValues")


@attr.s(auto_attribs=True)
class P11DetailedNiValues:
    """Forms the NI Summary table in the P11 Detailed report.

    Attributes:
        table (Union[Unset, None, str]): [readonly]
        earnings_at_lel (Union[Unset, float]): [readonly]
        earnings_above_lel_to_pt (Union[Unset, float]): [readonly]
        earnings_above_pt_to_uap (Union[Unset, float]): [readonly]
        earnings_above_uap_to_uel (Union[Unset, float]): [readonly]
        earnings_above_pt_to_uel (Union[Unset, float]): [readonly]
        employee_nics (Union[Unset, float]): [readonly]
        employer_nics (Union[Unset, float]): [readonly]
        employee_and_employer_nics (Union[Unset, float]): [readonly]
    """

    table: Union[Unset, None, str] = UNSET
    earnings_at_lel: Union[Unset, float] = UNSET
    earnings_above_lel_to_pt: Union[Unset, float] = UNSET
    earnings_above_pt_to_uap: Union[Unset, float] = UNSET
    earnings_above_uap_to_uel: Union[Unset, float] = UNSET
    earnings_above_pt_to_uel: Union[Unset, float] = UNSET
    employee_nics: Union[Unset, float] = UNSET
    employer_nics: Union[Unset, float] = UNSET
    employee_and_employer_nics: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        table = self.table
        earnings_at_lel = self.earnings_at_lel
        earnings_above_lel_to_pt = self.earnings_above_lel_to_pt
        earnings_above_pt_to_uap = self.earnings_above_pt_to_uap
        earnings_above_uap_to_uel = self.earnings_above_uap_to_uel
        earnings_above_pt_to_uel = self.earnings_above_pt_to_uel
        employee_nics = self.employee_nics
        employer_nics = self.employer_nics
        employee_and_employer_nics = self.employee_and_employer_nics

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if table is not UNSET:
            field_dict["table"] = table
        if earnings_at_lel is not UNSET:
            field_dict["earningsAtLel"] = earnings_at_lel
        if earnings_above_lel_to_pt is not UNSET:
            field_dict["earningsAboveLelToPt"] = earnings_above_lel_to_pt
        if earnings_above_pt_to_uap is not UNSET:
            field_dict["earningsAbovePtToUap"] = earnings_above_pt_to_uap
        if earnings_above_uap_to_uel is not UNSET:
            field_dict["earningsAboveUapToUel"] = earnings_above_uap_to_uel
        if earnings_above_pt_to_uel is not UNSET:
            field_dict["earningsAbovePtToUel"] = earnings_above_pt_to_uel
        if employee_nics is not UNSET:
            field_dict["employeeNics"] = employee_nics
        if employer_nics is not UNSET:
            field_dict["employerNics"] = employer_nics
        if employee_and_employer_nics is not UNSET:
            field_dict["employeeAndEmployerNics"] = employee_and_employer_nics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table = d.pop("table", UNSET)

        earnings_at_lel = d.pop("earningsAtLel", UNSET)

        earnings_above_lel_to_pt = d.pop("earningsAboveLelToPt", UNSET)

        earnings_above_pt_to_uap = d.pop("earningsAbovePtToUap", UNSET)

        earnings_above_uap_to_uel = d.pop("earningsAboveUapToUel", UNSET)

        earnings_above_pt_to_uel = d.pop("earningsAbovePtToUel", UNSET)

        employee_nics = d.pop("employeeNics", UNSET)

        employer_nics = d.pop("employerNics", UNSET)

        employee_and_employer_nics = d.pop("employeeAndEmployerNics", UNSET)

        p11_detailed_ni_values = cls(
            table=table,
            earnings_at_lel=earnings_at_lel,
            earnings_above_lel_to_pt=earnings_above_lel_to_pt,
            earnings_above_pt_to_uap=earnings_above_pt_to_uap,
            earnings_above_uap_to_uel=earnings_above_uap_to_uel,
            earnings_above_pt_to_uel=earnings_above_pt_to_uel,
            employee_nics=employee_nics,
            employer_nics=employer_nics,
            employee_and_employer_nics=employee_and_employer_nics,
        )

        return p11_detailed_ni_values
