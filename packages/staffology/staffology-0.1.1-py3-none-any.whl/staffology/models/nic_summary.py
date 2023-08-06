from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.item import Item
from ..types import UNSET, Unset

T = TypeVar("T", bound="NicSummary")


@attr.s(auto_attribs=True)
class NicSummary:
    """
    Attributes:
        ni_table (Union[Unset, str]):
        as_director (Union[Unset, bool]):
        gross_earnings_for_nics (Union[Unset, float]):
        earnings_at_lel (Union[Unset, float]):
        earnings_above_lel_to_pt (Union[Unset, float]):
        earnings_above_pt_to_st (Union[Unset, float]):
        earnings_above_pt_to_uap (Union[Unset, float]):
        earnings_above_st_to_uel (Union[Unset, float]):
        earnings_above_st_to_fust (Union[Unset, float]):
        earnings_above_fust_to_uel (Union[Unset, float]):
        earnings_above_uap_to_uel (Union[Unset, float]):
        earnings_above_uel (Union[Unset, float]):
        employee_nics (Union[Unset, float]):
        employee_ni_rebate (Union[Unset, float]):
        employer_nics (Union[Unset, float]):
        employer_ni_rebate (Union[Unset, float]):
        has_values (Union[Unset, bool]):
        employee (Union[Unset, Item]):
    """

    ni_table: Union[Unset, str] = UNSET
    as_director: Union[Unset, bool] = UNSET
    gross_earnings_for_nics: Union[Unset, float] = UNSET
    earnings_at_lel: Union[Unset, float] = UNSET
    earnings_above_lel_to_pt: Union[Unset, float] = UNSET
    earnings_above_pt_to_st: Union[Unset, float] = UNSET
    earnings_above_pt_to_uap: Union[Unset, float] = UNSET
    earnings_above_st_to_uel: Union[Unset, float] = UNSET
    earnings_above_st_to_fust: Union[Unset, float] = UNSET
    earnings_above_fust_to_uel: Union[Unset, float] = UNSET
    earnings_above_uap_to_uel: Union[Unset, float] = UNSET
    earnings_above_uel: Union[Unset, float] = UNSET
    employee_nics: Union[Unset, float] = UNSET
    employee_ni_rebate: Union[Unset, float] = UNSET
    employer_nics: Union[Unset, float] = UNSET
    employer_ni_rebate: Union[Unset, float] = UNSET
    has_values: Union[Unset, bool] = UNSET
    employee: Union[Unset, Item] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ni_table = self.ni_table
        as_director = self.as_director
        gross_earnings_for_nics = self.gross_earnings_for_nics
        earnings_at_lel = self.earnings_at_lel
        earnings_above_lel_to_pt = self.earnings_above_lel_to_pt
        earnings_above_pt_to_st = self.earnings_above_pt_to_st
        earnings_above_pt_to_uap = self.earnings_above_pt_to_uap
        earnings_above_st_to_uel = self.earnings_above_st_to_uel
        earnings_above_st_to_fust = self.earnings_above_st_to_fust
        earnings_above_fust_to_uel = self.earnings_above_fust_to_uel
        earnings_above_uap_to_uel = self.earnings_above_uap_to_uel
        earnings_above_uel = self.earnings_above_uel
        employee_nics = self.employee_nics
        employee_ni_rebate = self.employee_ni_rebate
        employer_nics = self.employer_nics
        employer_ni_rebate = self.employer_ni_rebate
        has_values = self.has_values
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ni_table is not UNSET:
            field_dict["niTable"] = ni_table
        if as_director is not UNSET:
            field_dict["asDirector"] = as_director
        if gross_earnings_for_nics is not UNSET:
            field_dict["grossEarningsForNics"] = gross_earnings_for_nics
        if earnings_at_lel is not UNSET:
            field_dict["earningsAtLel"] = earnings_at_lel
        if earnings_above_lel_to_pt is not UNSET:
            field_dict["earningsAboveLelToPt"] = earnings_above_lel_to_pt
        if earnings_above_pt_to_st is not UNSET:
            field_dict["earningsAbovePtToSt"] = earnings_above_pt_to_st
        if earnings_above_pt_to_uap is not UNSET:
            field_dict["earningsAbovePtToUap"] = earnings_above_pt_to_uap
        if earnings_above_st_to_uel is not UNSET:
            field_dict["earningsAboveStToUel"] = earnings_above_st_to_uel
        if earnings_above_st_to_fust is not UNSET:
            field_dict["earningsAboveStToFust"] = earnings_above_st_to_fust
        if earnings_above_fust_to_uel is not UNSET:
            field_dict["earningsAboveFustToUel"] = earnings_above_fust_to_uel
        if earnings_above_uap_to_uel is not UNSET:
            field_dict["earningsAboveUapToUel"] = earnings_above_uap_to_uel
        if earnings_above_uel is not UNSET:
            field_dict["earningsAboveUel"] = earnings_above_uel
        if employee_nics is not UNSET:
            field_dict["employeeNics"] = employee_nics
        if employee_ni_rebate is not UNSET:
            field_dict["employeeNiRebate"] = employee_ni_rebate
        if employer_nics is not UNSET:
            field_dict["employerNics"] = employer_nics
        if employer_ni_rebate is not UNSET:
            field_dict["employerNiRebate"] = employer_ni_rebate
        if has_values is not UNSET:
            field_dict["hasValues"] = has_values
        if employee is not UNSET:
            field_dict["employee"] = employee

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ni_table = d.pop("niTable", UNSET)

        as_director = d.pop("asDirector", UNSET)

        gross_earnings_for_nics = d.pop("grossEarningsForNics", UNSET)

        earnings_at_lel = d.pop("earningsAtLel", UNSET)

        earnings_above_lel_to_pt = d.pop("earningsAboveLelToPt", UNSET)

        earnings_above_pt_to_st = d.pop("earningsAbovePtToSt", UNSET)

        earnings_above_pt_to_uap = d.pop("earningsAbovePtToUap", UNSET)

        earnings_above_st_to_uel = d.pop("earningsAboveStToUel", UNSET)

        earnings_above_st_to_fust = d.pop("earningsAboveStToFust", UNSET)

        earnings_above_fust_to_uel = d.pop("earningsAboveFustToUel", UNSET)

        earnings_above_uap_to_uel = d.pop("earningsAboveUapToUel", UNSET)

        earnings_above_uel = d.pop("earningsAboveUel", UNSET)

        employee_nics = d.pop("employeeNics", UNSET)

        employee_ni_rebate = d.pop("employeeNiRebate", UNSET)

        employer_nics = d.pop("employerNics", UNSET)

        employer_ni_rebate = d.pop("employerNiRebate", UNSET)

        has_values = d.pop("hasValues", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        nic_summary = cls(
            ni_table=ni_table,
            as_director=as_director,
            gross_earnings_for_nics=gross_earnings_for_nics,
            earnings_at_lel=earnings_at_lel,
            earnings_above_lel_to_pt=earnings_above_lel_to_pt,
            earnings_above_pt_to_st=earnings_above_pt_to_st,
            earnings_above_pt_to_uap=earnings_above_pt_to_uap,
            earnings_above_st_to_uel=earnings_above_st_to_uel,
            earnings_above_st_to_fust=earnings_above_st_to_fust,
            earnings_above_fust_to_uel=earnings_above_fust_to_uel,
            earnings_above_uap_to_uel=earnings_above_uap_to_uel,
            earnings_above_uel=earnings_above_uel,
            employee_nics=employee_nics,
            employee_ni_rebate=employee_ni_rebate,
            employer_nics=employer_nics,
            employer_ni_rebate=employer_ni_rebate,
            has_values=has_values,
            employee=employee,
        )

        return nic_summary
